#!/usr/local/bin/sage -python

# Draws all colorings using up to max_clrs colors and merges the drawings into a single collage
# The colorings are generated iteratively as all 0 colorings, 1 colorings, ... , max_clrs colorings

# IMPORTANT: the i-colorings can only use i colors and cannot use the rest of (max_clrs - i) colors so we get fewer
# results than what the chromatic polynomial tells us for that many colors

# IMPORTS

import solids_prep.solids_dict_prep as sdp
import solids_prep.solids_layout_prep as slp

import tempfile
import math

import svgutils.compose as svgc 

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import all_graph_colorings

from collections.abc import Callable

# OUTPUT SETTING
output_path = "Code/Plots/"
filename_base = "res"
collage_name = "icosahedron_non-aut-4-clrings"
MAX_DIMS_RATIO = 5

# PLOT_SETTINGS
VERTEX_LABEL = False
EDGE_LABELS = False
COLORS_TO_USE = ["#FF0000","#00FF00","#0000FF","#FFFF00","#FF00FF","#00FFFF"]

# SOLID SETTINGS
SOLID_NAME = "icosahedron"
NUM_CLRS = 4

# INPUT SETTINGS
G = Graph(slp.get_labeled_neighbor_dict(SOLID_NAME))
POSITIONS = slp.get_pos_dict(SOLID_NAME)
STYLES = slp.get_labeled_edge_styles(SOLID_NAME)

# uncomment following to use edge colors
# colors = slp.get_labeled_edge_clrs(SOLID_NAME)


# BEGIN: IMAGE HANDLING

# creates separate images for all the colorings
# the colorings must be passed as a list of lists where each list is an ordered list of color values for the given vertices
# positions is a dict where keys are the vertex indices and values are (x,y) coordinate tuples
# styles is a dict where keys are edge labels and values are strings in format 'solid', 'dotted' etc.
def create_images_svg(graph : Graph, positions : dict[int,tuple], styles : dict[int,str], clrings : list[list], collage_max_dims_ratio : float) -> None:
    svgs = []
    temp_paths = []

    for c in get_dictionarized(clrings):
        graphic = graph.plot(vertex_labels=VERTEX_LABEL,edge_labels=EDGE_LABELS,pos=positions,vertex_colors=c,edge_styles=styles)
        # store each image in temporary file and then create corresponding PIL image
        with tempfile.NamedTemporaryFile(suffix=".svg",delete=False) as tmp:
            graphic.save(tmp.name)
            temp_paths.append(tmp.name)
            img_file = svgc.SVG(tmp.name)
            svgs.append(img_file)

    merge_images_svg(svgs,collage_max_dims_ratio) # by now, the tempfiles still have to exist, otherwise, the svg contents will be erased

    for path in temp_paths: # now we can remove the tempfiles
        os.remove(path)

# merges the svgs provided in the list into a single svg collage
def merge_images_svg(svgs : list[svgc.SVG], max_dims_ratio : float):

    print(f"merging {len(svgs)} images...")

    imgs_per_row,images_per_column = find_collage_dimensions(len(svgs),max_dims_ratio)
    ref_svg = svgs[0]

    svg_width = ref_svg.width
    svg_height = ref_svg.height

    if not isinstance(svg_width,float) or not isinstance(svg_height,float):
        return

    # this is a constant by which I have to scale both dimensions to get pt value from px
    # probably the width and height parameters return px value which is greater and has to be reduced by 20% to get pt size
    PADDING_COMPENSATION = 0.8

    svg_width *= PADDING_COMPENSATION
    svg_height *= PADDING_COMPENSATION

    img_padding_size = 50

    collage_width = svg_width * imgs_per_row + img_padding_size * (imgs_per_row - 1)
    collage_height = svg_height * images_per_column + img_padding_size * (images_per_column - 1)

    for i,img in enumerate(svgs):
        col = (i % imgs_per_row)
        x = col * (svg_width + img_padding_size)
        row = (i // imgs_per_row)
        y = row * (svg_height + img_padding_size)
        img.move(x,y)

    # xmlns='http://www.w3.org/2000/svg' defines a xml namespace to be the namespace for SVG defomed by the W3C, the World Wide Web Consortium
    # 2000 there means that the namespace was defined in year 2000 by W3C
    background_svg_str = (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{collage_width}pt' height='{collage_height}pt'>"
        f"<rect width='100%' height='100%' fill='white'/></svg>"
    )

    with tempfile.NamedTemporaryFile(suffix=".svg", delete=True, mode="w", encoding="utf-8") as bgfile:
        bgfile.write(background_svg_str)
        bgfile.flush() # important, otherwise the changes are not seen by SVG constructor
        bgfile_path = bgfile.name
        background = svgc.SVG(bgfile_path)

        fig = svgc.Figure(f"{collage_width}pt",f"{collage_height}pt",background,*svgs)
        fig.save(f"{output_path}{collage_name}.svg")

# finds nice dimensions for the collage of n images
# tries to decompose number n into i and j s.t. i * j = n and i and j are not more that k multiples of each other
def find_collage_dimensions(num_figures : int, max_ratio : float) -> tuple:

    i = math.floor(math.sqrt(num_figures))
    if i * i == num_figures:
        return i,i
    i = math.floor(i)
    j = i
    while j * max_ratio >= i:
      i += 1
      j = num_figures // i
      if num_figures % i == 0:
          return i,j
    i = math.ceil(math.sqrt(num_figures))
    j = math.ceil(num_figures / i)
    return i,j

# END: IMAGE HANDLING

# BEGIN: COLORING STANDARDIZATION BY FINGERPRIT

# fingerprint stores information about sizes of independent sets of the colorings
# contains tuples in format (count_of_vtces,clr_val)
def get_fprnt(coloring_list : list[int]) -> list[tuple]:
    num_clrs = max(coloring_list) + 1 # there is one more colors than what is the label of the greatest valued color
    fingerprint = [[0,clr] for clr in range(num_clrs)] # stores a pair in format (count_of_vertices,color_value)
    for clr in coloring_list:
        fingerprint[clr][0] += 1 # increase the count component of the pair
    return [tuple(pair) for pair in fingerprint]

# sorts the fingerprint based on the counts of the colors
# i.e. sorts the independent sets based on their sizes
# note that originally they are sorted by values of the colors
def stdize_fprnt(fingerprint: list[tuple]) -> list[tuple]:
    return sorted(fingerprint,key=lambda pair : pair[0])

# makes a string out of the fingerprint where each number is encoded as a letter from the alphabet
# this will later allow for lexicographic sorting of the fingerprints after they are ordered
def stringify_fprnt_counts(fingerprint : list[tuple]) -> str:
    return "".join([chr(count) for (count,clr) in fingerprint]) # join the result into one string

# like the above but uses the color values to stringify
def stringify_fprnt_clr_vals(fingerprint : list[tuple]) -> str:
    return "".join([chr(clr) for (count,clr) in fingerprint]) # join the result into one string

# returns list of fingerprinted colorings where each fingerprinted coloring is a tuple in form (clring as list, fingerprint)
def get_fprnted_clrings(colorings_as_list : list[list]) -> list[tuple]:
    return [(clring,stdize_fprnt(get_fprnt(clring))) for clring in colorings_as_list]

# END: COLORING STANDARDIZATION BY FINGERPRIT

# BEGIN: COLORING INDEP SET POSITIONS STANDARDIZATION

# function that receives two colorings and a graph and returns automorphism and relabeling by which they can be unified or None
def get_unification_proof(c1 : list[int], c2 : list[int], g : Graph): # -> automorphism, relabeling
    ...
    # TODO: implement function body

# END: COLORING INDEP SET POSITIONS STANDARDIZATION

# BEGIN: ALL COLORINGS CONVERSION AND WRAPPER FUNCTIONS

# returns a MathSage all colorings where each coloring is a list indexed by vertex and containing the value of the color at each position
def all_graph_colorings_list(g : Graph, num_clrs : int, *args) -> list[list]:
    colorings = all_graph_colorings(g,num_clrs,*args) # coloring is represented as dict in format: color -> list of vertices with that color (color is an int)
    clrings_list = []
    for coloring in colorings:
        clrings_list.append(get_coloring_list(coloring))
    return clrings_list

# converts the coloring in dict format to list format
def get_coloring_list(clring_as_dict : dict[int,list]) -> list[int]:
    num_vertices = len(reduce(lambda x,y: x + y,clring_as_dict.values(),[])) # reduce is equivalent of foldl in functional programming languages
    clring_as_list = [0 for _ in range(num_vertices)]
    for color in clring_as_dict.keys():
        for vtx in clring_as_dict[color]:
            clring_as_list[vtx] = color
    return clring_as_list

# converts a coloring given as list of colors for each vertex to a dict where key is color string in format '#FFFFFF' and value contains vtx indices of that color
def get_coloring_dict(clring_as_list : list[int]) -> dict[str,list]:
    clring_dict = {}
    for i,c_ind in enumerate(clring_as_list):
        clr = COLORS_TO_USE[c_ind]
        if clr not in clring_dict:
            clring_dict[clr] = []
        clring_dict[clr].append(i)
    return clring_dict

# converts the colorings to dictionary form
# each coloring is a dict where: key = color string, value = list of indices of vertices of that color
def get_dictionarized(clrings : list[list]) -> list[dict]:
    return [get_coloring_dict(clring) for clring in clrings]

# END: ALL COLORINGS CONVERSION AND WRAPPER FUNCTIONS


# BEGIN: COLORINGS AUTOMORPHISM AND RELABELING EQUIVALENCY CHECKING

# checks if two colorings are equivalent up to automorphism while also trying if the colors are not just permuted
# the alg works by trying to construct a mapping from colors of the first coloring to colors of the second coloring
def check_equiv_under_automorph_and_permutation(c1 : list[int], c2 : list[int], automorphism_cycles : list[tuple]) -> bool:
    f = {} # possible mapping that is being constructed on the fly
    f_inv = {} # inverse of the mapping to be able to check if somebody has mapped to the image we want earlier
    for cycle in automorphism_cycles:
        k = len(cycle)
        for i in range(k):
            b1 = c1[cycle[i]]
            b2 = c2[cycle[(i+1)%k]]
            if b1 in f: # color b1 is already mapped to some other color
                if f[b1] != b2:
                    return False
            else:
                if b2 in f_inv: # some other color has already mapped to this color
                    return False
                else:
                    f[b1] = b2
                    f[b2] = b1
    return True

# END: COLORINGS AUTOMORPHISM AND RELABELING EQUIVALENCY CHECKING


# BEGIN: COLORINGS AUTOMORPHISM EQUIVALENCY CHECKING

# check if two colorings (represented as list) equivalent under given automorphism (represented as list of cycles)
def check_eqiv_under_automorph(c1 : list[int], c2 : list[int], automorphism_cycles : list[tuple]) -> bool:
    for cycle in automorphism_cycles:
        k = len(cycle)
        for i in range(k):
            if c1[cycle[i]] != c2[cycle[(i+1)%k]]:
                return False
    return True

# function to prune colorings
# 1. prepare a list of indicators if the coloring still has no lower indexed match
# 2. go through all colorings while considering only the ones that still have no lower match
# 3. for no match coloring -> check all other higher indexed colorings and if I can get to them by any automorphism, if yes, then mark it at matched
def get_non_automorphic(g : Graph, clrings : list[list], equiv_comparer : Callable[[list,list,list],bool] = check_eqiv_under_automorph) -> list[list]:

    still_unique = [True for _ in clrings]
    automorphisms_as_cycles = [a.cycle_tuples(singletons=True) for a in g.automorphism_group()]

    # mark colorings which are not unique (only mark from the lower index to the greater one)
    for i in range(len(clrings)):
        if not still_unique: # the coloring already has a lower indexed partner in the same automorphism class (orbit)
            continue
        for j in range(i+1,len(clrings)):
            for a_cycles in automorphisms_as_cycles:
                if equiv_comparer(clrings[i],clrings[j],a_cycles):
                    still_unique[j] = False

    # return the colorings that remained unique
    unique_clrings = []
    for i,clring in enumerate(clrings):
        if still_unique[i]:
            unique_clrings.append(clring)

    return unique_clrings

# END: COLORINGS AUTOMORPHISM EQUIVALENCY CHECKING


# BEGIN: COLORINGS RELABELING EQUIVALENCY CHECKING

# removes non canonic colorings out of the list of colorings
def get_canonized(clrings : list[list]) -> list[list]:
    return [c for c in filter(is_in_canonic_form,clrings)]

# checks if coloring is in canonic form, the canonic form represents all colorings with the same structure but different permutation of color values
# canonic form is following: for the given coloring, it must have the colors ordered from lowest to highest when going from left to right through the coloring list
# assumes that colors are numbers from 0 ... k
def is_in_canonic_form(coloring : list[int]) -> bool:
    count = 0
    for clr in coloring:
        if clr > count:
            return False
        if clr == count:
            count += 1
    return True

# END: COLORINGS RELABELING EQUIVALENCY CHECKING
def get_encountered_fingerprints(fingerprinted_colorings : list[tuple]) -> set[tuple]:
    unique_fingerprints = set()
    for fprnt in [tuple([size for (size,clr) in fprint]) for (clring,fprint) in fingerprinted_colorings]:
        unique_fingerprints.add(fprnt)
    return unique_fingerprints

# BEGIN: ENCOUNTERED FINGERPRINT STATISTICS

# END: ENCOUNTERED FINGERPRINT STATISTICS

# IMPORTANT: below pick the function to use here
# colorings = all_graph_colorings_list(G,NUM_CLRS) # all colorings as usual
# colorings = get_canonized(all_graph_colorings_list(G,NUM_CLRS)) # colorings up to permutations of colors (but not up to rotations and reflections)
colorings = get_non_automorphic(G,all_graph_colorings_list(G,NUM_CLRS)) # colorings up to rotations/reflections but not up to permutation
# colorings = get_non_automorphic(G,all_graph_colorings_list(G,NUM_CLRS),check_equiv_under_automorph_and_permutation)

# BEGIN: USE ORDERING BY FINGERPRINT

# the ordering makes sure that structurally similar colorings appear next to each other in the collage
# e.g. for colorings with indep set sizes (1,3,4) appear before ones with indep set sizes (2,2,4)
# also the colorings with same set sizes vector are ordered lexicographically using the color values of the corresponding independent sets

# fingerprinted coloring is a tuple (coloring,fingerprint)
fingerprinted = get_fprnted_clrings(colorings) # gets standardized fingerprints (standardized fingerprint is a list of sizes of independent sets together with their color values ordered by their size)
fingerprinted.sort(key= lambda fprnted: stringify_fprnt_clr_vals(fprnted[1])) # sort lexicographically based on standardized fingerprint independent set color values
fingerprinted.sort(key=lambda fprnted : stringify_fprnt_counts(fprnted[1])) # sort lexicographically based on standardized fingerprint independent set sizes

print("encountered following fingerprints:")
print(get_encountered_fingerprints(fingerprinted))

colorings = [clring for (clring,fprint) in fingerprinted]

# END: USE ORDERING BY FINGERPRINT

print("generating coloring images...")
# colorings = CLRING_FUNCTION(g,NUM_CLRS) 
images = create_images_svg(G,POSITIONS,STYLES,colorings,MAX_DIMS_RATIO)