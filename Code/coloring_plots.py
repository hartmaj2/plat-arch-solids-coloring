#!/usr/local/bin/sage -python

# Draws all colorings using up to max_clrs colors and merges the drawings into a single collage
# The colorings are generated iteratively as all 0 colorings, 1 colorings, ... , max_clrs colorings

# IMPORTANT: the i-colorings can only use i colors and cannot use the rest of (max_clrs - i) colors so we get fewer
# results than what the chromatic polynomial tells us for that many colors

# IMPORTS

import solids_prep.solids_dict_prep as sdp
import solids_prep.solids_layout_prep as slp

import tempfile
from PIL import Image
import math

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import all_graph_colorings

from collections.abc import Callable

# OUTPUT SETTING
output_path = "Code/Plots/"
filename_base = "res"
collage_name = "icosahedron_4-clrings"

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

# creates separate images for all the colorings
# the colorings must be passed as a list of lists where each list is an ordered list of color values for the given vertices
# positions is a dict where keys are the vertex indices and values are (x,y) coordinate tuples
# styles is a dict where keys are edge labels and values are strings in format 'solid', 'dotted' etc.
def create_images(graph : Graph, positions : dict[int,tuple], styles : dict[int,str], clrings : list[list]) -> list[Image.Image]:
    images = []

    for c in get_dictionarized(clrings):
        graphic = graph.plot(vertex_labels=VERTEX_LABEL,edge_labels=EDGE_LABELS,pos=positions,vertex_colors=c,edge_styles=styles)
        # store each image in temporary file and then create corresponding PIL image
        with tempfile.NamedTemporaryFile(suffix=".png",delete=True) as tmp:
            graphic.save(tmp.name)
            img_file = Image.open(tmp.name)
            images.append(img_file.copy())
            img_file.close()

    return images

# merges the images of the colorings in the directory into a single square-like collage
def merge_images(images : list[Image.Image]):
    print(f"merging {len(images)} images")

    imgs_per_row = math.ceil(math.sqrt(len(images)))
    image_width = images[0].size[0]
    image_height = images[0].size[1]
    img_padding_size = 100

    collage_width = image_width * imgs_per_row + img_padding_size * (imgs_per_row - 1)
    collage_height = image_height * imgs_per_row + img_padding_size * (imgs_per_row - 1)
    collage = Image.new("RGB",(collage_width,collage_height),(255,255,255))

    for i,img in enumerate(images):
        col = (i % imgs_per_row)
        x = col * (image_width + img_padding_size)
        row = (i // imgs_per_row)
        y = row * (image_height + img_padding_size)
        collage.paste(img,(x,y))

    collage.save(f"{output_path}{collage_name}.png")

# returns a MathSage all colorings where each coloring is a list indexed by vertex and containing the value of the color at each position
def all_graph_colorings_list(g : Graph, num_clrs : int, *args) -> list[list]:
    n = len(g.vertices())
    colorings = all_graph_colorings(g,num_clrs,*args) # coloring is represented as dict in format: color -> list of vertices with that color
    clrings_list = []
    for i,coloring in enumerate(colorings):
        clring_as_list = [0 for _ in range(n)]
        for color in coloring:
            for vtx in coloring[color]:
                clring_as_list[vtx] = color
        clrings_list.append(clring_as_list)
    return clrings_list

# check if two colorings (represented as list) equivalent under given automorphism (represented as list of cycles)
def check_eqiv_under_automorph(c1 : list[int], c2 : list[int], automorphism_cycles : list[tuple]) -> bool:
    for cycle in automorphism_cycles:
        k = len(cycle)
        for i in range(k):
            if c1[cycle[i]] != c2[cycle[(i+1)%k]]:
                return False
    return True

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

# IMPORTANT: below pick the function to use here
# colorings = all_graph_colorings_list(G,NUM_CLRS) # all colorings as usual
# colorings = get_canonized(all_graph_colorings_list(G,NUM_CLRS)) # colorings up to permutations of colors (but not up to rotations and reflections)
# colorings = get_non_automorphic(G,all_graph_colorings_list(G,NUM_CLRS)) # colorings up to rotations/reflections but not up to permutation
colorings = get_non_automorphic(G,all_graph_colorings_list(G,NUM_CLRS),check_equiv_under_automorph_and_permutation)

print("generating coloring images...")
# colorings = CLRING_FUNCTION(g,NUM_CLRS) 
images = create_images(G,POSITIONS,STYLES,colorings)
print("merging images...")
merge_images(images)