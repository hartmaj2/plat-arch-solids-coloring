#!/usr/local/bin/sage -python

import solids_prep.solids_dict_prep as sdp
import graph_utils.orbital_chrompoly as ocp
import t_printing.latex_table_printing as tp

import math

from sage.all import *

from collections.abc import Callable
from typing import Any

# CONSTANT RENAME FOR CONVENIENCE
VERTICES = sdp.JSON_VERTICES
EDGES = sdp.JSON_EDGES
NAME = sdp.JSON_NAME

# OUTPUT TABLE SETTINGS
EVAL_NUM_LIMIT = 8
STARTING_NUM = 2
TOO_LARGE_NUM_LIMIT = 10_000_000
THIN_RULE = r"\specialrule{0.2pt}{0.65ex}{0.65ex}"

data_headers = [str(x) for x in range(STARTING_NUM,EVAL_NUM_LIMIT+1)]

EVALS_CAPTION = f"Evaluated chromatic polynomial and orbital chromatic polynomial for platonic solids at points {STARTING_NUM} to {EVAL_NUM_LIMIT}. For each solid, the top row contains the chromatic polynomial, the bottom row contains the orbital chromatic polynoial."
EVALS_LABEL = "tab:platonic-polys-evals"
HEADER = "Platonic solid"

EXACTS_CAPTION = f"Numbers of colorings using exactly {STARTING_NUM} to {EVAL_NUM_LIMIT} colors. For each solid, the top row contains the value when counting also symmetric colorings as different. The bottom row takes two colorings as different only if they cannot be identified using some automorphism."
EXACTS_LABEL = f"tab:platonic-exactly-n-clrs"

EXACT_PARTITIONS_CAPTION = f"Numbers of of possible partitions of vertices of the graphs into $n$ independent sets."
EXACT_PARTITIONS_LABEL = f"tab:platonic-exact-n-partitions"

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
# output_file = open(ROOT_FOLDER + "/Results/poly_evals.md","w")
# output_type = output_file

import sys
output_type = sys.stdout

# returns some polynomial of platonic solids
def get_platonic_poly_dict(poly_calc_func : Callable[[Graph],Any]) -> dict[str,Any]:
    platonic = sdp.get_platonic_solid_dict()
    plat_polys = {}
    for name,solid in zip(platonic.keys(),platonic.values()):
        edges = solid[sdp.JSON_EDGES]
        g = Graph(edges)
        poly = poly_calc_func(g)
        plat_polys[name] = poly
    return plat_polys

# evaluates the polynomials from STARTING_NUM to k (start at 2 because obviously no graph can be 1 colored as long as it has some edge)
def get_plat_poly_evaluations(poly_calc_func : Callable[[Graph],Any], k : int) -> dict [str,list]:
    polys = get_platonic_poly_dict(poly_calc_func)
    evals = {}
    for name,poly in zip(polys.keys(),polys.values()):
        vals = [poly(i) for i in range(STARTING_NUM,k+1)]
        evals[name] = vals
    return evals

# for nicer look of the table if the value is 1_234_332 just replaces with >= 10^6
def get_approx_string(val : int):
    return f"\\approx 10^{{{int(math.log10(val))}}}"

# for latex printing
def wrap_with_dollars(s : str):
    return "$" + s + "$"

# preprocesses the value so that all vals that are at least scientific_start get stored in scientific notation
def preprocess_for_print(d : dict, too_large_num_start : int) -> dict:
    new = {}
    for key,tup in zip(d.keys(),d.values()):
        new_vals = []
        for val in tup:
            if val >= too_large_num_start:
                new_vals.append(get_approx_string(val))
            else:
                new_vals.append(str(val))
        new[key] = new_vals
    return new

# takes a list of dicts where each dict has the same key set and then appends the rows in the dicts to create multiple rows for each key
def create_mult_row_dict(dicts : list[dict]):
    new = {}
    for key in dicts[0].keys():
        new[key] = []
        for dict in dicts:
            new[key].append(dict[key])
    return new

# takes a list corresponding to evaluations of chromatic polynomial at points STARTING_NUM,...,k and generates a list of number of colorings using exactly STARTING_NUM,...,k colors
def convert_to_exactly_n_colrs(evaluations : list[int]) -> list[int]:
    evals = [0 for _ in range(STARTING_NUM)] + evaluations # pad the evaluations so each index corresponds to the number of colors to use
    exacts = [0 for _ in range(evals.count(0))] # the zero entries will be same
    first_nonzero_pos = len(exacts)
    exacts.append(evals[first_nonzero_pos]) # first nonzero entry is also identic
    for n in range(first_nonzero_pos+1,len(evals)):
        num_clrings = evals[n]
        for i in range(first_nonzero_pos,n):
            num_clrings -= math.comb(n,i) * exacts[i]
        exacts.append(num_clrings)
    exacts = exacts[2:] # remove the padding
    return exacts

# takes dictionary of chromatic polynomial evaluations and returns dictionary containing counts for colorings using exactly n-colors
def get_exact_n_colors_dict(evaluations : dict[str,list]) -> dict[str,list]:
    exacts = {}
    for key,evals in zip(evaluations.keys(),evaluations.values()):
        exacts[key] = convert_to_exactly_n_colrs(evals)
    return exacts


# BEGIN: COMPUTING EXACT N-PARTITIONS
# takes a list of number corresponding to number of colorings using exactly n-colors and returns a list 
# of numbers corresponding to number of partitions into n independent sets irrespective of the possible labels we could give the partitions
def divide_by_possible_relabelings(exacts: list[int]) -> list[int]:
    partitions_counts = []# the zero entries will be same
    for n in range(len(exacts)):
        partitions_counts.append(exacts[n] // math.factorial(n+STARTING_NUM))
    return partitions_counts

# takes dictionary of lists of numbers of colorings using exactly n-colors and returns a dictionary with lists of counts of n-partitions
def get_n_partition_counts_dict(exacts_dict : dict[str,list]) -> dict[str,list]:
    n_partitions_dict = {}
    for key,exacts in zip(exacts_dict.keys(),exacts_dict.values()):
        n_partitions_dict[key] = divide_by_possible_relabelings(exacts)
    return n_partitions_dict

# END: COMPUTING EXACT N-PARTITIONS


# BEGIN: PRINTING EVALUATED POLYNOMIALS OR EXACT N-COLORINGS
# dicts = [get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT),get_plat_poly_evaluations(ocp.orbital_chromatic_polynomial2,EVAL_NUM_LIMIT)]
# dicts = [get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT)),get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.orbital_chromatic_polynomial2,EVAL_NUM_LIMIT))]
# preprocessed_dicts = [preprocess_for_print(d,TOO_LARGE_NUM_LIMIT) for d in dicts]

# mult_row_dict = create_mult_row_dict(preprocessed_dicts)

# tp.print_solid_mult_row_data(mult_row_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,caption=EVALS_CAPTION,label=EVALS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5,row_cluster_sep=THIN_RULE)
# tp.print_solid_mult_row_data(mult_row_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,caption=EXACTS_CAPTION,label=EXACTS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5,row_cluster_sep=THIN_RULE)
# END: PRINTING EVALUATED POLYNOMIALS OR EXACT N-COLORINGS


# BEGIN: PRINTING EXACT N-PARTITIONS
dict = get_n_partition_counts_dict(get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT)))
preprocessed_dict = preprocess_for_print(dict,TOO_LARGE_NUM_LIMIT)
tp.print_solid_mult_col_data(preprocessed_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,EXACT_PARTITIONS_CAPTION,EXACT_PARTITIONS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5)
# END: PRINTING EXACT N-PARTITIONS