#!/usr/local/bin/sage -python

# On input we have graphs in json format retrieved from: https://polyhedra.tessera.li/
# The json file can be obtained by clicking on desired polyhedron and then on Info section on the toolbar
# e.g https://polyhedra.tessera.li/tetrahedron/info (the download link is then on the bottom)

# Chromatic number is calculated using sage `chromatic_number` function. See: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html#sage.graphs.graph_coloring.chromatic_number
# Chromatic index (edge chromatic number) -||- `edge_coloring` function. See: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html#sage.graphs.graph_coloring.edge_coloring

# IMPORTS

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number, edge_coloring

import md_table_printing as mdp
import solids_dict_prep as sdp

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
output_file = open(ROOT_FOLDER + "/output_sage.md","w")
output_type = output_file

# output_type = sys.stdout

# calls sage code on given data
def calculate_chromatic_numbers(solid_edges : list[tuple]) -> tuple[int,int] :
    g = Graph(solid_edges)
    vtx_chrom_num : int = chromatic_number(g)
    edge_chrom_num : int = edge_coloring(g,value_only=True)
    return vtx_chrom_num, edge_chrom_num

# processes all solids and loads corresponding data to the dict
def process_solids(solid_edges : dict, solids_dict : dict):
    for solid_name in solid_edges.keys():
        solids_dict[solid_name] = calculate_chromatic_numbers(solid_edges[solid_name])


# dictionaries to store graph data
platonic_data = {}
archimedean_data = {}

# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    platonic_edges = sdp.get_platonic_edges_dict()
    process_solids(platonic_edges,platonic_data)
    mdp.print_solids(platonic_data,sdp.PLATONIC_FOLDER_NAME)
    
    archimedean_edges = sdp.get_archimedean_edges_dict()
    process_solids(archimedean_edges,archimedean_data)
    mdp.print_solids(archimedean_data,sdp.ARCHIMEDEAN_FOLDER_NAME)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()