#!/usr/local/bin/sage -python

# Displays a given graph using the planar layout of SageMath
# The displayed graph is stored in the file named: POLYHEDRON + ".png"

# IMPORTS

import solids_prep.solids_dict_prep as sdp
import os
from PIL import Image
import math

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import all_graph_colorings

# OUTPUT SETTING
output_path = "Code/Plots/"
filename_base = "res"

# INPUT SETTINGS
max_clrs = 3
g = graphs.CycleGraph(4)


def create_images(graph, max_clrs):
    for num_clrs in range(max_clrs+1):
        clrings = all_graph_colorings(graph,num_clrs,hex_colors=True)
        for i,c in enumerate(clrings):
            graph.plot(vertex_colors=c).save(f"{output_path}{filename_base}_{num_clrs}crls_{i}.png")

def merge_images():
    filenames = os.listdir(output_path)
    images = [Image.open(os.path.join(output_path, img)) for img in filenames]
    print(images[0].size)

print("generating colorings...")

create_images(g,max_clrs)
merge_images()