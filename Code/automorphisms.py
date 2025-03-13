#!/usr/local/bin/sage -python

import solids_prep.solids_dict_prep as sdp
import t_printing.md_table_printing as printing

from sage.all import Graph

# INPUT
VERTICES = sdp.JSON_VERTICES
EDGES = sdp.JSON_EDGES
NAME = sdp.JSON_NAME

platonic = sdp.get_platonic_solid_dict()
archimedean = sdp.get_archimedean_solid_dict()

# OUTPUT 
plat_data = {}
arch_data = {}

PLATONIC_HEADER = "platonic"
ARCHIMEDEAN_HEADER = "archimedean"
COLUMN_HEADERS = ["automorphisms"]

COL_SIZE = 20

print("Platonic solids automorphisms: ")
for solid_name in platonic.keys():
    solid = platonic[solid_name]
    g = Graph(solid[EDGES])
    G = g.automorphism_group()
    order = G.order()
    plat_data[solid_name] = [order]
    # print(f"{solid_name:30} {order}")

print()
print("Archimedean solids automorphisms: ")
for solid_name in archimedean.keys():
    solid = archimedean[solid_name]
    g = Graph(solid[EDGES])
    G = g.automorphism_group()
    order = G.order()
    arch_data[solid_name] = [order]
    # print(f"{solid_name:30} {G.order()}") 

printing.print_solid_mult_col_data(plat_data,PLATONIC_HEADER,COLUMN_HEADERS,COL_SIZE)
printing.print_solid_mult_col_data(arch_data,ARCHIMEDEAN_HEADER,COLUMN_HEADERS,COL_SIZE)

# print(f"{platonic[solid_key]}")

