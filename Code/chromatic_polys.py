#!/usr/local/bin/sage -python

# Computes chromatic polynomials using SageMath function here: https://github.com/sagemath/sage/blob/develop/src/sage/graphs/chrompoly.pyx
# Can compute also orbital chromatic polynomials using my function from graph_utils

# IMPORTS

from sage.all import Graph
from sage.all import *

import t_printing.latex_table_printing as printing
import t_printing.poly_printing as pp
import solids_prep.solids_dict_prep as sdp
import graph_utils.orbital_chrompoly as orbchrom

import re

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

## ALL SOLIDS PRINTING
CHROMPOLY_DATA_HEADER = ["Chromatic polynomial"]
ORBCHROMPOLY_DATA_HEADER = ["Orbital chromatic polynomial"]

NOT_COMPUTED_SYMBOL = r'\dag'

PLAT_CAPTION = "Chromatic polynomials of Platonic graphs."
PLAT_LABEL = "tab:platonic-chrom-polys"

ARCH_CAPTION = f"Chromatic polynomials of Archimedean graphs. The ${NOT_COMPUTED_SYMBOL}$ symbol means the computation took too much time. This comes from the fact, that the time complexity increases with amount of edges of the graph."
ARCH_LABEL = "tab:archimedean-chrom-polys"

## SELECTION OF SOLIDS PRINTING

TEXT_COLUMN_HEADER = "Solid"

CAPTION_CHROMPOLY = "Chromatic polynomial of selected solids. For other solids, the polynomial coefficients were too large and would not print nicely."
LABEL_CHROMPOLY = "tab:selected-chrom-polys"

CAPTION_ORBCHROMPOLY = "Orbital chromatic polynomial of selected solids. For other solids, the polynomial coefficients were too large and would not print nicely."
LABEL_ORBCHROMPOLY = "tab:selected-orbital-chrom-polys"

selected_solids = ["cube","octahedron","tetrahedron"]


# uncomment following 2 lines to output to a folder
output_file = open(ROOT_FOLDER + "/Results/chrom_polys2.md","w")
# output_file = open(ROOT_FOLDER + "/Results/orbital_chrom_polys.md","w")
output_type = output_file

# import sys
# output_type = sys.stdout

# DEBUG

polys_to_skip = ["truncated icosidodecahedron","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","snub cube","truncated cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron"]

LINEWIDTH_ALIGNMENT_RATIO = 0.7
ROW_SPACING_RATIO = 2.0
# ALIGNMENT_PAR_STYLE_WRAP = r"p{0.5\linewidth}"
ALIGNMENT_PAR_STYLE_WRAP = f"p{{{LINEWIDTH_ALIGNMENT_RATIO}\\linewidth}}"

# calls sage code on given data
def compute_chromatic_polynomial(solid_edges : list[tuple]):
    G = Graph(solid_edges)
    poly = G.chromatic_polynomial()
    return poly

def compute_orbital_chromatic_polynomial(solid_edges : list[tuple]):
    G = Graph(solid_edges)
    poly = orbchrom.orbital_chromatic_polynomial(G)
    return poly

# processes all solids and loads corresponding data to the dict
def get_chrom_polys_dict(solid_dict : dict, chrom_poly_function) -> dict[str,list]:
    solid_computed_data = {}
    for solid_name in solid_dict.keys():
        if solid_name in polys_to_skip:
            solid_computed_data[solid_name] = [NOT_COMPUTED_SYMBOL] # IMPORTANT: needs to be packed in a list in order for the printing to work propertly
            print(f"skipping chromial of {solid_name}")
        else:
            print(f"calculating chromial of {solid_name}")
            solid_computed_data[solid_name] = [chrom_poly_function(solid_dict[solid_name][sdp.JSON_EDGES])] # IMPORTANT: needs to be packed in a list in order for the printing to work propertly 
    return solid_computed_data

def print_orbital_chrom_poly_table(solids : dict[str,dict]):
    solid_data = get_chrom_polys_dict(solids,compute_orbital_chromatic_polynomial)
    printing.print_solid_mult_col_data(solid_data,TEXT_COLUMN_HEADER,ORBCHROMPOLY_DATA_HEADER,CAPTION_ORBCHROMPOLY,LABEL_ORBCHROMPOLY,output_type,pp.poly_to_latex,ALIGNMENT_PAR_STYLE_WRAP,ROW_SPACING_RATIO)

def print_chrom_poly_table(solids : dict[str,dict]):
    solid_data = get_chrom_polys_dict(solids,compute_chromatic_polynomial)
    printing.print_solid_mult_col_data(solid_data,TEXT_COLUMN_HEADER,CHROMPOLY_DATA_HEADER,CAPTION_CHROMPOLY,LABEL_CHROMPOLY,output_type,pp.poly_to_latex,ALIGNMENT_PAR_STYLE_WRAP)

# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    solids = sdp.get_selected_solids_dict(selected_solids)
    print_chrom_poly_table(solids)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()