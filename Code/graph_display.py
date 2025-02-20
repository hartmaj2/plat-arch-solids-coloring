#!/usr/local/bin/sage -python

# Displays a given graph using the planar layout of SageMath
# The displayed graph is stored in the file named: POLYHEDRON + ".png"

# IMPORTS

from sage.all import Graph
from sage.all import *
import json

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"
INPUT_FOLDER_PATH = ROOT_FOLDER + "/JsonGraphs"
POLYHEDRON_CATEGORY = "/Platonic"
POLYHEDRON = "dodecahedron"

with open(INPUT_FOLDER_PATH + POLYHEDRON_CATEGORY + "/" + POLYHEDRON + ".json") as file:
    graph_data = json.load(file) # load json file content as dictionary
    edges = graph_data["edges"]
    G = Graph(edges)
    G_layout = G.layout(layout='planar') # compute layout (positions for the vertices to be drawn at)
    G.plot(pos=G_layout).save(POLYHEDRON + ".png") # plot the graph given the computed layout and save the result to file