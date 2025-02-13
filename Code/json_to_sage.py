#!/usr/local/bin/sage -python

# On input we have graphs in json format retrieved from: https://polyhedra.tessera.li/
# The json file can be obtained by clicking on desired polyhedron and then on Info section on the toolbar
# e.g https://polyhedra.tessera.li/tetrahedron/info (the download link is then on the bottom)


# IMPORTS

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number, edge_coloring
import json
import sys
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

GRAPH_JSONS_PATH = f"{os.getcwd()}/{INPUT_FOLDER_PATH}"
GRAPH_JSONS_FOLDERS = os.listdir(GRAPH_JSONS_PATH)

JSON_NAME_PROPERTY_KEY_NAME = "name"
JSON_EDGES_PROPERTY_KEY_NAME = "edges"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
# output_file = open(ROOT_FOLDER + "/output.txt","w")
# output_type = output_file

output_type = sys.stdout

# retrieves data from json files necessary to create sage graphs
def get_solid_data(folder_name: str, solid_filename : str) -> tuple[str,list]:
    with open(f"{INPUT_FOLDER_PATH}/{folder_name}/{solid_filename}","r") as file:
        graph_data : dict = json.load(file)
        edges = graph_data[JSON_EDGES_PROPERTY_KEY_NAME]
        name = graph_data[JSON_NAME_PROPERTY_KEY_NAME]
        return name,[tuple(edge) for edge in edges] # convert: list of lists -> list of tuples

# calls sage code on given data
def calculate_chromatic_numbers(solid_edges : list[tuple]) -> tuple[int,int] :
    g = Graph(solid_edges)
    vtx_chrom_num : int = chromatic_number(g)
    edge_chrom_num : int = edge_coloring(g,value_only=True)
    return vtx_chrom_num, edge_chrom_num

# processes all solids and prints output to terminal
def process_solids(folder_name : str, solid_names : list[str]):

    header_line_string = f"{TABLE_COLS_SEPARATOR} {folder_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {VTX_CHROM_NUM_HEADER:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {EDG_CHROM_NUM_HEADER:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
    header_separator_string = f"{TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
    print(header_line_string,file=output_type)
    print(header_separator_string,file=output_type)
    for solid_filename in solid_names:
        solid_name, solid_edges = get_solid_data(folder_name,solid_filename)
        vtx_chrom_num, edge_chrom_num = calculate_chromatic_numbers(solid_edges)
        table_entry_row = f"{TABLE_COLS_SEPARATOR} {solid_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {vtx_chrom_num:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {edge_chrom_num:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
        print(table_entry_row,file=output_type)
    print(file=output_type)

# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    for folder in GRAPH_JSONS_FOLDERS:
        solid_names = os.listdir(GRAPH_JSONS_PATH + '/' + folder) # retrieves solid names in current folder
        process_solids(folder,solid_names)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()

# SOLID NAMES

# platonic_solids = ["tetrahedron","cube","octahedron","dodecahedron","icosahedron"]
# archimedean_solids = ["truncated icosidodecahedron","truncated cube","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","truncated octahedron","snub cube","truncated cuboctahedron","truncated tetrahedron","cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron",] 