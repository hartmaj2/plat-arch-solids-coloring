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
collage_name = "octahedron_3-clrings"

VERTEX_LABEL = False
EDGE_LABELS = False

# INPUT SETTINGS
max_clrs = 3
solid_name = "octahedron"
edges = sdp.get_all_solids_dict()[solid_name][sdp.JSON_EDGES]
g = Graph(slp.get_labeled_neighbor_dict(solid_name))
positions = slp.get_pos_dict(solid_name)
styles = slp.get_labeled_edge_styles(solid_name)
# colors = slp.get_labeled_edge_clrs(solid_name)

# creates separate images for all the colorings
def create_images(graph : Graph, max_clrs : int) -> list[Image.Image]:
    images = []

    for num_clrs in range(max_clrs+1):
        clrings = all_graph_colorings(graph,num_clrs,hex_colors=True)

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

# converts a MathSage coloring into a list indexed by vertex and containing the value of the color at each position
def all_graph_colorings2(g : Graph, num_clrs : int, *args):
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
def check_eqiv_under_automorph(c1 : list[int], c2 : list[int], a : list[tuple]):
    for cycle in a:
        k = len(cycle)
        for i in range(k):
            if c1[cycle[i]] != c2[cycle[(i+1)%k]]:
                return False
    return True


# TODO: make the following into a function
solid_name = "octahedron"
g = Graph(slp.get_labeled_neighbor_dict(solid_name))
clrings = all_graph_colorings2(g,5)
is_first_of_kind = [True for _ in clrings]

for i in range(len(clrings)):
    for j in range(i+1,len(clrings)):
        c1 = clrings[i]
        c2 = clrings[j]
        is_equiv = False
        for cycle in [a.cycle_tuples(singletons=True) for a in g.automorphism_group()]: # important to set singletons to True!
            if check_eqiv_under_automorph(c1,c2,cycle):
                is_equiv = True
                is_first_of_kind[j] = False

# TODO: add function to prune colorings

print(f"Uniqueness vector: {is_first_of_kind}")
print(f"Eqivalence classes: {is_first_of_kind.count(True)}")

# print("generating coloring images...")
# images = create_images(g,max_clrs)
# print("merging images...")
# merge_images(images)