#!/usr/local/bin/sage -python
# Tests speed of various algorithms for calculation orbital chrom polys

import graph_utils.orbital_chrompoly as orb
import timing.timing as tmng
import solids_prep.solids_dict_prep as sdp
import t_printing.md_table_printing as mdp
import t_printing.poly_printing as pp
# from sage.all import Graph
from sage.all import *
import sys

filepath = ""
out_file = open("Code/Results/chrom_poly_sel.md","w")
output = out_file

solids = sdp.get_all_solids_dict()

selected = ["cube","tetrahedron","octahedron","truncated tetrahedron","cuboctahedron","dodecahedron","icosahedron"]
# selected = ["cube"]

# adapter function fot the chromatic poly function
def chromatic_poly(g : Graph):
    return g.chromatic_polynomial()

headers = ["orb chrompoly"]

def get_desmos_polys(selected : list[str]):
    results = {}
    id = 0
    for name in selected:
        g = Graph(solids[name][sdp.JSON_EDGES])
        result = [pp.named_poly_for_desmos(orb.orbital_chromatic_polynomial2(g),"p",id)]
        results[name] = result
        id += 1
    return results

results = get_desmos_polys(selected)
mdp.print_solid_mult_col_data(results,"Solids",headers,output_type=out_file)

out_file.close()