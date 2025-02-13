#!/usr/local/bin/sage -python

# On input we have graphs in json format retrieved from: https://polyhedra.tessera.li/
# The json file can be obtained by clicking on desired polyhedron and then on Info section on the toolbar
# e.g https://polyhedra.tessera.li/tetrahedron/info (the download link is then on the bottom)


# IMPORTS

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number, edge_coloring
import json
import os

# TABLE VISUALS

NAME_COL_SIZE : int = 30
CHROM_NO_COL_SIZE : int = 9

VTX_CHROM_NUM_HEADER = "X(G)"
EDG_CHROM_NUM_HEADER = "X'(G)"

TABLE_COLS_SEPARATOR = "|"
TABLE_ROWS_SEPARATOR = "="

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"
INPUT_FOLDER_PATH = ROOT_FOLDER + "/JsonGraphs"
OUTPUT_DEBUG_FILE_PATH = ROOT_FOLDER + "/sage_graphs.txt"
JSON_EDGES_PROPERTY_KEY_NAME = "edges"

def get_solid_edges(folder_name: str, solid_filename : str):
    with open(f"{INPUT_FOLDER_PATH}/{folder_name}/{solid_filename}","r") as file:
        graph_data = json.load(file)
        edges = graph_data[JSON_EDGES_PROPERTY_KEY_NAME]
        return [tuple(edge) for edge in edges]

def print_chromatic_number(folder_name : str, solid_filename : str):
    g = Graph(get_solid_edges(folder_name,solid_filename))
    solid_name = solid_filename.split(sep=".")[0]
    print(f"{TABLE_COLS_SEPARATOR} {solid_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {chromatic_number(g):^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {edge_coloring(g,value_only=True):^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}")

def process_solids(folder_name : str, solid_names : list[str]):
    print(f"{TABLE_COLS_SEPARATOR} {folder_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {VTX_CHROM_NUM_HEADER:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {EDG_CHROM_NUM_HEADER:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}")
    print(f"{TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}")
    for solid_filename in solid_names:
        print_chromatic_number(folder_name,solid_filename)
    print()

graph_jsons_path = f"{os.getcwd()}/{INPUT_FOLDER_PATH}"

graph_jsons_folders = os.listdir(graph_jsons_path)

for folder in graph_jsons_folders:
    solid_names = os.listdir(graph_jsons_path + '/' + folder)
    process_solids(folder,solid_names)



# SOLID NAMES

# platonic_solids = ["tetrahedron","cube","octahedron","dodecahedron","icosahedron"]
# archimedean_solids = ["truncated icosidodecahedron","truncated cube","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","truncated octahedron","snub cube","truncated cuboctahedron","truncated tetrahedron","cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron",] 