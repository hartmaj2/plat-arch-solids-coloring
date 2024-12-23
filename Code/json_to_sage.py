#!/usr/local/bin/sage -python

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number, edge_coloring
import json
import os

NAME_COL_SIZE : int = 30
CHROM_NO_COL_SIZE : int = 9

def get_solid_edges(folder_name: str, solid_filename : str):
    with open(f"Code/JsonGraphs/{folder_name}/{solid_filename}","r") as file:
        graph_data = json.load(file)
        edges = graph_data["edges"]
        return [tuple(edge) for edge in edges]

def print_chromatic_number(folder_name : str, solid_filename : str):
    g = Graph(get_solid_edges(folder_name,solid_filename))
    solid_name = solid_filename.split(sep=".")[0]
    print(f"| {solid_name:^{NAME_COL_SIZE}} | {chromatic_number(g):^{CHROM_NO_COL_SIZE}} | {edge_coloring(g,value_only=True):^{CHROM_NO_COL_SIZE}} |")

def process_solids(folder_name : str, solid_names : list[str]):
    with open(f"Code/sage_graphs.txt","w") as output_file:
        print(f"| {folder_name:^{NAME_COL_SIZE}} | {"X(G)":^{CHROM_NO_COL_SIZE}} | {"X'(G)":^{CHROM_NO_COL_SIZE}} |")
        print(f"| {"-":-^{NAME_COL_SIZE}} | {"-":-^{CHROM_NO_COL_SIZE}} | {"-":-^{CHROM_NO_COL_SIZE}} |")
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


        