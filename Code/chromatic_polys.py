#!/usr/local/bin/sage -python

# Computes chromatic polynomials using SageMath function here: https://github.com/sagemath/sage/blob/develop/src/sage/graphs/chrompoly.pyx

# IMPORTS

from sage.all import Graph
from sage.all import *

import t_printing.md_table_printing as printing
import solids_prep.solids_dict_prep as sdp

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

DATA_COLUMN_HEADER = "chromatic polynomial"

# uncomment following 2 lines to output to a folder
output_file = open(ROOT_FOLDER + "/Results/chrom_polys.md","w")
output_type = output_file

# import sys
# output_type = sys.stdout

# DEBUG

polys_to_skip = ["truncated icosidodecahedron","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","snub cube","truncated cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron"]


# calls sage code on given data
def compute_chromatic_polynomial(solid_edges : list[tuple]):
    G = Graph(solid_edges)
    poly = G.chromatic_polynomial()
    return poly

# processes all solids and loads corresponding data to the dict
def get_chrom_polys_dict(solid_edges : dict):
    solid_computed_data = {}
    for solid_name in solid_edges.keys():
        if solid_name in polys_to_skip:
            solid_computed_data[solid_name] = None
            print(f"skipping chromial of {solid_name}")
        else:
            print(f"calculating chromial of {solid_name}")
            solid_computed_data[solid_name] = compute_chromatic_polynomial(solid_edges[solid_name])
    return solid_computed_data

# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    platonic_edges = sdp.get_platonic_edges_dict()
    platonic_data = get_chrom_polys_dict(platonic_edges)
    printing.print_solid_one_col_poly(platonic_data,sdp.PLATONIC_FOLDER,data_col_name=DATA_COLUMN_HEADER,output_type=output_type)
    
    archimedean_edges = sdp.get_archimedean_edges_dict()
    archimedean_data = get_chrom_polys_dict(archimedean_edges)
    printing.print_solid_one_col_poly(archimedean_data,sdp.ARCHIMEDEAN_FOLDER,data_col_name=DATA_COLUMN_HEADER,output_type=output_type)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()