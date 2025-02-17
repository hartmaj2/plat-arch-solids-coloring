#!/usr/local/bin/sage -python

# On input we have graphs in json format retrieved from: https://polyhedra.tessera.li/
# The json file can be obtained by clicking on desired polyhedron and then on Info section on the toolbar
# e.g https://polyhedra.tessera.li/tetrahedron/info (the download link is then on the bottom)

# Chromatic number is calculated using sage `chromatic_number` function. See: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html#sage.graphs.graph_coloring.chromatic_number
# Chromatic index (edge chromatic number) -||- `edge_coloring` function. See: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html#sage.graphs.graph_coloring.edge_coloring

# IMPORTS

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number, edge_coloring
import json
import os

import latex_table_printing as latex_table_printing

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
output_file = open(ROOT_FOLDER + "/output_sage.md","w")
output_type = output_file

# output_type = sys.stdout

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

# processes all solids and loads corresponding data to the dict
def process_solids(folder_name : str, solid_names : list[str], solids_dict : dict):
    for solid_filename in solid_names:
        solid_name, solid_edges = get_solid_data(folder_name,solid_filename)
        solids_dict[solid_name] = calculate_chromatic_numbers(solid_edges)


# dictionaries to store graph data
platonic = {}
archimedean = {}

# main loop over folders with different solid types (Platonic, Archimedean)
def main():

    solid_names = os.listdir(GRAPH_JSONS_PATH + '/' + latex_table_printing.PLATONIC_FOLDER_NAME) # retrieves solid names in current folder
    process_solids(latex_table_printing.PLATONIC_FOLDER_NAME,solid_names,platonic)
    latex_table_printing.print_solids(platonic,latex_table_printing.PLATONIC_FOLDER_NAME,output_type)
    
    solid_names = os.listdir(GRAPH_JSONS_PATH + '/' + latex_table_printing.ARCHIMEDEAN_FOLDER_NAME) # retrieves solid names in current folder
    process_solids(latex_table_printing.ARCHIMEDEAN_FOLDER_NAME,solid_names,archimedean)
    latex_table_printing.print_solids(archimedean,latex_table_printing.ARCHIMEDEAN_FOLDER_NAME,output_type)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()