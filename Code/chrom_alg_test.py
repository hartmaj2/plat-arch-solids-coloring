#!/usr/local/bin/sage -python
# Tests speed of various algorithms for calculation orbital chrom polys

import graph_utils.orbital_chrompoly as orb
import timing.timing as tmng
import solids_prep.solids_dict_prep as sdp
import t_printing.md_table_printing as mdp
# from sage.all import Graph
from sage.all import *

solids = sdp.get_all_solids_dict()

# selected = ["cube","tetrahedron","octahedron"]
selected = ["truncated octahedron","truncated cube","rhombicuboctahedron"]

# adapter function fot the chromatic poly function
def chromatic_poly(g : Graph):
    return g.chromatic_polynomial()

func_to_test = [chromatic_poly,orb.orbital_chromatic_polynomial, orb.orbital_chromatic_polynomial2]

headers = ["chrom poly","orb chrom poly","orb chrom poly 2","orb chrom poly 3"]

def calculate_times(selected : list[str]):
    results = {}
    for name in selected:
        g = Graph(solids[name][sdp.JSON_EDGES])
        times = tuple([time for (_,time) in map(lambda func : tmng.run_and_get_time(func,g),func_to_test)])
        results[name] = times
    return results

results = calculate_times(selected)
mdp.print_solid_mult_col_data(results,"Solids",headers,20,transform=lambda d : round(d,5))