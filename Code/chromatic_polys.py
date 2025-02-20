#!/usr/local/bin/sage -python

# Checks number of colorings given the k := the amount of colors which have to be used 
# (no less and no more colors can be used)

# IMPORTANT: the function output is different than the amount of k-colorings by standard definition
# standard definition consideres also colorings which use less colors (surjectivity not required)

# IMPORTS

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import number_of_n_colorings
import json
import os

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"
INPUT_FOLDER_PATH = ROOT_FOLDER + "/JsonGraphs"
POLYHEDRON_CATEGORY = "/Platonic"
POLYHEDRON = "octahedron"

k = 4

def empty_graph_k_colorings(k):
    G = graphs.EmptyGraph()
    vertices = 4
    for i in range(vertices):
        G.add_vertex()
    G.plot().save("empty.png")
    num_k_colorings = number_of_n_colorings(G,k)
    print(f"empty on {vertices} vertices has {num_k_colorings} {k}-colorings")

with open(INPUT_FOLDER_PATH + POLYHEDRON_CATEGORY + "/" + POLYHEDRON + ".json") as file:
    graph_data = json.load(file)
    edges = graph_data["edges"]
    G = Graph(edges)
    num_k_colorings = number_of_n_colorings(G,k)
    print(f"{POLYHEDRON} has {num_k_colorings} {k}-colorings")
