#!/usr/local/bin/sage -python

# Checks number of colorings given the k := the amount of colors which have to be used 
# (no less and no more colors can be used)

# IMPORTANT: the function output is different than the amount of k-colorings by standard definition
# standard definition consideres also colorings which use less colors (surjectivity not required)

# IMPORTS

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import number_of_n_colorings


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
def compute_chromatic_polynomial(solid_edges : list[tuple]):
    G = Graph(solid_edges)
    poly = G.chromatic_polynomial()
    return poly

# processes all solids and loads corresponding data to the dict
def get_chrom_polys_dict(solid_edges : dict):
    solid_computed_data = {}
    for solid_name in solid_edges.keys():
        solid_computed_data[solid_name] = str(compute_chromatic_polynomial(solid_edges[solid_name]))
    return solid_computed_data

# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    platonic_edges = sdp.get_platonic_edges_dict()
    platonic_data = get_chrom_polys_dict(platonic_edges)
    mdp.print_solid_one_col_data(platonic_data,sdp.PLATONIC_FOLDER_NAME)
    
    archimedean_edges = sdp.get_archimedean_edges_dict()
    archimedean_data = get_chrom_polys_dict(archimedean_edges)
    mdp.print_solid_one_col_data(archimedean_data,sdp.ARCHIMEDEAN_FOLDER_NAME)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()