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

# OUTPUT SETTING
output_path = "Code/Plots/"
filename_base = "res"
collage_name = "test"

# PLOT_SETTINGS
VERTEX_LABEL = False
EDGE_LABELS = False
COLORS_TO_USE = ["#FF0000","#00FF00","#0000FF","#FFFF00","#FF00FF","#00FFFF"]

# SOLID SETTINGS
SOLID_NAME = "cube"
NUM_CLRS = 2

# INPUT SETTINGS
edges = sdp.get_all_solids_dict()[SOLID_NAME][sdp.JSON_EDGES]
g = Graph(slp.get_labeled_neighbor_dict(SOLID_NAME))
positions = slp.get_pos_dict(SOLID_NAME)
styles = slp.get_labeled_edge_styles(SOLID_NAME)

# uncomment following to use edge colors
# colors = slp.get_labeled_edge_clrs(SOLID_NAME)

# clrings = all_graph_colorings(graph,num_clrs,hex_colors=True)

# creates separate images for all the colorings
# the colorings must be passed as a list of dicts
# each dict corresponds to one coloring, key is color string and value is list of indices of vertices of that color
def create_images(graph : Graph, clrings : list[dict]) -> list[Image.Image]:
    images = []

    for c in clrings:
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
    img_padding_size = 100

    collage_width = image_width * imgs_per_row + img_padding_size * (imgs_per_row - 1)
    collage = Image.new("RGB",(collage_width,collage_width),(255,255,255))

    for i,img in enumerate(images):
        col = (i % imgs_per_row)
        x = col * (image_width + img_padding_size)
        row = (i // imgs_per_row)
        y = row * (image_width + img_padding_size)
        collage.paste(img,(x,y))

    collage.save(f"{output_path}{collage_name}.png")

# wrapper for all colorings function that replaces the preset colors with mine
def all_graph_colorings2(g : Graph, num_clrs : int, *args) -> list[dict]:
    colorings = all_graph_colorings(g,num_clrs,*args)
    new_colorings = []
    for clring in colorings:
        new_clring = {}
        for i,clr in enumerate(clring.keys()):
            new_clring[COLORS_TO_USE[i]] = clring[clr]
        new_colorings.append(new_clring)
    return new_colorings

# converts a MathSage coloring into a list indexed by vertex and containing the value of the color at each position
def all_graph_colorings_as_lists(g : Graph, num_clrs : int, *args):
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
def check_eqiv_under_automorph(c1 : list[int], c2 : list[int], automorphism_cycles : list[tuple]):
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

def all_non_automorph_colorings(g : Graph, num_clrs: int, *args):
    clrings = all_graph_colorings_as_lists(g,num_clrs,*args)
    still_unique = [True for _ in clrings]
    automorphisms_as_cycles = [a.cycle_tuples(singletons=True) for a in g.automorphism_group()]

    # mark colorings which are not unique (only mark from the lower index to the greater one)
    for i in range(len(clrings)):
        if not still_unique: # the coloring already has a lower indexed partner in the same automorphism class (orbit)
            continue
        for j in range(i+1,len(clrings)):
            for a_cycles in automorphisms_as_cycles:
                if check_eqiv_under_automorph(clrings[i],clrings[j],a_cycles):
                    still_unique[j] = False

    # return the colorings that remained unique
    unique_clrings = []
    for i,clring in enumerate(clrings):
        if still_unique[i]:
            unique_clrings.append(clring)

    coloring_dicts = [get_coloring_dict(c) for c in unique_clrings] # convert colorings from lists to dicts

    return coloring_dicts 

# converts a coloring given as list of colors for each vertex to a dict where key is color string in format '#FFFFFF' and value contains vtx indices of that color
def get_coloring_dict(clrings_as_list : list[int]) -> dict[str,list]:
    clring_dict = {}
    for i,c_ind in enumerate(clrings_as_list):
        clr = COLORS_TO_USE[c_ind]
        if clr not in clring_dict:
            clring_dict[clr] = []
        clring_dict[clr].append(i)
    return clring_dict

# IMPORTANT: below pick the function to use here
CLRING_FUNCTION = all_graph_colorings2
# CLRING_FUNCTION = all_non_automorph_colorings

print("generating coloring images...")
clrings = CLRING_FUNCTION(g,NUM_CLRS) 
images = create_images(g,clrings)
print("merging images...")
merge_images(images)