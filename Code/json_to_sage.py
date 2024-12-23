#!/usr/local/bin/sage -python

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number
import json
import os

def get_solid_edges(folder_name: str, solid_filename : str):
    with open(f"Code/JsonGraphs/{folder_name}/{solid_filename}","r") as file:
        graph_data = json.load(file)
        edges = graph_data["edges"]
        return [tuple(edge) for edge in edges]

def print_chromatic_number(folder_name : str, solid_filename : str):
    g = Graph(get_solid_edges(folder_name,solid_filename))
    solid_name = solid_filename.split(sep=".")[0]
    print(f"{solid_name + ":":<30}{chromatic_number(g):>5}")

def process_solids(folder_name : str, solid_names : list[str]):
    with open(f"Code/sage_graphs.txt","w") as output_file:
        print(f"{"X(G)":-^30}")
        for solid_filename in solid_names:
            command_str = f"G = Graph({get_solid_edges(folder_name,solid_filename)}); G.plot(layout='planar').show(); chromatic_number(G)"
            solid_name = solid_filename.split(sep=".")[0]
            output_file.write(f"{solid_name}: {command_str}\n")
            print_chromatic_number(folder_name,solid_filename)
        print()


solids = ["tetrahedron","cube","octahedron","dodecahedron","icosahedron"]

graph_jsons_path = f"{os.getcwd()}/Code/JsonGraphs"

graph_jsons_folders = os.listdir(graph_jsons_path)

for folder in graph_jsons_folders:
    solid_names = os.listdir(graph_jsons_path + '/' + folder)
    process_solids(folder,solid_names)


        