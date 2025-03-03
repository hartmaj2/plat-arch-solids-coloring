#!/usr/local/bin/sage -python

# On input we have graphs in json format retrieved from: https://polyhedra.tessera.li/
# The json file can be obtained by clicking on desired polyhedron and then on Info section on the toolbar
# e.g https://polyhedra.tessera.li/tetrahedron/info (the download link is then on the bottom)

# Chromatic number is calculated using sage `chromatic_number` function. See: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html#sage.graphs.graph_coloring.chromatic_number
# Chromatic index (edge chromatic number) -||- `edge_coloring` function. See: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html#sage.graphs.graph_coloring.edge_coloring

# IMPORTS

from sage.all import Graph
from sage.graphs.graph_coloring import chromatic_number, edge_coloring
from sage.graphs.line_graph import line_graph

import md_table_printing as printing
import solids_dict_prep as sdp
import graph_conversions as gc

# CONSTANT RENAME FOR CONVENIENCE
VERTICES = sdp.JSON_VERTICES
EDGES = sdp.JSON_EDGES
NAME = sdp.JSON_NAME

# OUTPUT TABLE SETTINGS
DATA_HEADERS_MD = ["X(G)","X'(G)","X''(G)"]
DATA_HEADERS_LATEX = [r"$\chi(G)$",r"$\chi'(G)$",r"$\chi''(G)$"]
data_headers = DATA_HEADERS_MD

# uncomment following to use latex data headers
# data_headers = DATA_HEADERS_LATEX 

PLAT_CAPTION = "Vertex and edge chromatic numbers of Platonic graphs"
PLAT_LABEL = "tab:platonic-chrom-nums"
ARCH_CAPTION = "Vertex and edge chromatic numbers of Archimedean graphs"
ARCH_LABEL = "tab:archimedean-chrom-nums"


# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
# output_file = open(ROOT_FOLDER + "/output_sage.md","w")
# output_type = output_file

import sys
output_type = sys.stdout

# calculates vertex chromatic number using sage chromatic_number() function
def calculate_vtx_chrom_num(solid_data : dict[list]) -> int:
    g = Graph(solid_data[EDGES])
    return chromatic_number(g)

# calculates edge chromatic number using sage edge_coloring()
def calculate_edg_chrom_num(solid_data : dict[list]) -> int:
    g = Graph(solid_data[EDGES])
    return edge_coloring(g,value_only=True)

# # calculates edge chromatic number using SAGE conversion to line graph
def calculate_edg_chrom_num_sage_lg(solid_data : dict[list]) -> int:
    g = Graph(solid_data[EDGES])
    l = g.line_graph()
    return chromatic_number(l)

# calculates edge chromatic number using conversion to line graph
def calculate_edg_chrom_num_lg(solid_data : dict[list]) -> int:
    line_graph = gc.create_line_graph(solid_data)
    l = Graph(line_graph[EDGES])
    return chromatic_number(l)  

# calculates total chromatic number using conversion to total graph
def calculate_tot_chrom_num(solid_data : dict[str,list]) -> int:
    tot_graph = gc.create_total_graph(solid_data)
    tg = Graph(tot_graph[EDGES])
    return chromatic_number(tg)

# processes all solids and loads corresponding data to the dict
def get_chrom_nums_dict(solid_data : dict[dict]):
    solid_computed_data = {}
    for solid_name in solid_data.keys():
        vtx_chrom_num = calculate_vtx_chrom_num(solid_data[solid_name])
        edg_chrom_num = calculate_edg_chrom_num_lg(solid_data[solid_name])
        tot_chrom_num = calculate_tot_chrom_num(solid_data[solid_name])
        solid_computed_data[solid_name] = vtx_chrom_num, edg_chrom_num, tot_chrom_num
    return solid_computed_data

# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    platonic_edges = sdp.get_platonic_solid_dict()
    platonic_data = get_chrom_nums_dict(platonic_edges)
    printing.print_solid_mult_col_data(platonic_data,sdp.PLATONIC_FOLDER,data_headers,caption=PLAT_CAPTION,label=PLAT_LABEL,output_type=output_type)
    
    archimedean_edges = sdp.get_archimedean_solid_dict()
    archimedean_data = get_chrom_nums_dict(archimedean_edges)
    printing.print_solid_mult_col_data(archimedean_data,sdp.ARCHIMEDEAN_FOLDER,data_headers,caption=ARCH_CAPTION,label=ARCH_LABEL,output_type=output_type)

if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()