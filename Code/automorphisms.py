#!/usr/local/bin/sage -python

# Prints a table that shows how many automorphisms the platonic and archimedean solids have

import solids_prep.solids_dict_prep as sdp
import t_printing.latex_table_printing as tp

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

PLATONIC_HEADER = "Platonic"
PLATONIC_CAPTION = "Sizes of automorphism groups of graphs of Platonic solids."
PLATONIC_LABEL = "tab:plat-automorphisms"

ARCHIMEDEAN_HEADER = "Archimedean"
ARCHIMEDEAN_CAPTION = "Sizes of automorphism groups of graphs of Archimedean solids."
ARCHIMEDEAN_LABEL = "tab:arch-automorphisms"

# OUTPUT TABLE HEADERS
LATEX_COL_HEADERS = [r"$\abs{\Aut(G)}$"]
MD_COL_HEADERS = ["automorphisms"]
column_headers = LATEX_COL_HEADERS

# OUTPUT FOLDER 
ROOT_FOLDER = "Code"
# output_file = open(ROOT_FOLDER + "/Results/automorphisms.md","w")
# output_type = output_file

import sys
output_type = sys.stdout

COL_SIZE = 20

for solid_name in platonic.keys():
    solid = platonic[solid_name]
    g = Graph(solid[EDGES])
    G = g.automorphism_group()
    order = G.order()
    plat_data[solid_name] = [order]

for solid_name in archimedean.keys():
    solid = archimedean[solid_name]
    g = Graph(solid[EDGES])
    G = g.automorphism_group()
    order = G.order()
    arch_data[solid_name] = [order]

tp.print_solid_mult_col_data(plat_data,tp.STD_PLAT_TABLE_ORDER,PLATONIC_HEADER,column_headers,PLATONIC_CAPTION,PLATONIC_LABEL,output_type)
tp.print_solid_mult_col_data(arch_data,tp.STD_ARCH_TABLE_ORDER,ARCHIMEDEAN_HEADER,column_headers,ARCHIMEDEAN_CAPTION,ARCHIMEDEAN_LABEL,output_type)

