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

PARTITIONS_BOUNDS_CAPTION = f"Upper and lower bounds for the number of equivalence classes of the $\\righleftharpoons$ relation based on the number of equivalence classes of the $\\leftrightarrow$ relation."
PARTITIONS_BOUNDS_LABEL = f"tab:bounds-exactn-n-partitions"

ORBITAL_BOUNDS_CAPTION = f"Upper and lower bounds for the number of equivalence classes of the $\\righleftharpoons$ relation based on the number of equivalence classes of the $\\sim$ relation."
ORBITAL_BOUNDS_LABEL = f"tab:bounds-orbital"

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
# output_file = open(ROOT_FOLDER + "/Results/poly_evals.md","w")
# output_type = output_file

import sys
output_type = sys.stdout

# returns some polynomial of the solids whose names are given by the solid_names dictionary
def get_solids_poly_dict(poly_calc_func : Callable[[Graph],Any], solid_names : list[str]) -> dict[str,Any]:
    solids = sdp.get_selected_solids_dict(solid_names)
    plat_polys = {}
    for name,solid in zip(solids.keys(),solids.values()):
        edges = solid[sdp.JSON_EDGES]
        g = Graph(edges)
        poly = poly_calc_func(g)
        plat_polys[name] = poly
    return plat_polys

# evaluates the polynomials from STARTING_NUM to k (start at 2 because obviously no graph can be 1 colored as long as it has some edge)
def get_solids_poly_evaluations(poly_calc_func : Callable[[Graph],Any], k : int, solid_names) -> dict [str,list]:
    polys = get_solids_poly_dict(poly_calc_func,solid_names)
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

# preprocess one big number for printing
def preprocess_big_number_for_print(val : int, too_large_num_start : int) -> str:
    if val >= too_large_num_start:
        return get_approx_string(val)
    else:
        return str(val)

# preprocesses the value so that all vals that are at least scientific_start get stored in scientific notation
def preprocess_big_numbers_for_print(d : dict, too_large_num_start : int) -> dict:
    new = {}
    for key,tup in zip(d.keys(),d.values()):
        new[key] = [preprocess_big_number_for_print(val,too_large_num_start) for val in tup]
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


# BEGIN: COMPUTING BOUNDS ON NUMBER OF RELABELING-AUTOMORPHISM EQUIVALENCE CLASSES

# receives vector with numbers of equivalence classes of the relabeling relation and uses it to compute bounds on the number of equivalence classes of the relabeling-automorphism relation
def calculate_relabeling_class_bounds(n_partitions_dict : dict[str,list[int]]) -> dict[str,list[tuple]]:
    relabeling_bounds_dict = {}
    platonic = sdp.get_platonic_solid_dict()
    for key,n_partition_nums in zip(n_partitions_dict.keys(),n_partitions_dict.values()):
        edges = platonic[key][sdp.JSON_EDGES]
        g = Graph(edges)
        num_auts = ocp.num_automorphisms(g)
        relabeling_bounds_dict[key] = get_relabeling_bounds_from_list(n_partition_nums,num_auts)
    return relabeling_bounds_dict

# calculates the bounds from the vector of numbers of n partitions and the number of automorphisms of the graph
def get_relabeling_bounds_from_list(n_partitions_list: list[int], num_automotphisms : int) -> list[tuple[int,int]]:
    bounds = []
    for i in range(len(n_partitions_list)):
        lower = math.ceil(n_partitions_list[i] / num_automotphisms)
        upper = n_partitions_list[i]
        bounds.append((lower,upper))
    return bounds

# receives vector with numbers of equivalence classes of the automorphism relation and uses it to compute bounds on the number of equivalence classes of the relabeling-automorphism relation
def calculate_automorphism_class_bounds(orbital_exacts_dict : dict[str,list[int]]) -> dict[str,list[tuple]]:
    automorphism_bounds_dict = {}
    for key,orbital_exacts in zip(orbital_exacts_dict.keys(),orbital_exacts_dict.values()):
        automorphism_bounds_dict[key] = get_automorphism_bounds_from_list(orbital_exacts)
    return automorphism_bounds_dict

# calculates the bounds from the vector of numbers of equiv classes of the ~ relation
def get_automorphism_bounds_from_list(exact_orbital_list : list[int]) -> list[tuple[int,int]]:
    bounds = []
    for i in range(len(exact_orbital_list)):
        n = i + STARTING_NUM
        lower = math.ceil(exact_orbital_list[i] / math.factorial(n))
        upper = exact_orbital_list[i]
        bounds.append((lower,upper))
    return bounds

# preprocesses the bound tuples to interval strings for latex
def preprocess_bound_tuples_from_dict(n_partitions_dict : dict[str,list[tuple]],tlnl : int) -> dict[str,list[str]]:
    preprocessed_dict = {}
    for solid_name,list_tuples in zip(n_partitions_dict.keys(),n_partitions_dict.values()):
        preprocessed_dict[solid_name] = []
        preprocessed_dict[solid_name].append([f"{preprocess_big_number_for_print(upper,tlnl)}" for (lower,upper) in list_tuples])
        preprocessed_dict[solid_name].append([f"{preprocess_big_number_for_print(lower,tlnl)}" for (lower,upper) in list_tuples])
    return preprocessed_dict

# END: COMPUTING BOUNDS ON NUMBER OF RELABELING-AUTOMORPHISM EQUIVALENCE CLASSES


# BEGIN: PRINTING EVALUATED POLYNOMIALS OR EXACT N-COLORINGS
# dicts = [get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT),get_plat_poly_evaluations(ocp.orbital_chromatic_polynomial2,EVAL_NUM_LIMIT)]
# dicts = [get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT)),get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.orbital_chromatic_polynomial2,EVAL_NUM_LIMIT))]
# preprocessed_dicts = [preprocess_for_print(d,TOO_LARGE_NUM_LIMIT) for d in dicts]

# mult_row_dict = create_mult_row_dict(preprocessed_dicts)

# tp.print_solid_mult_row_data(mult_row_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,caption=EVALS_CAPTION,label=EVALS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5,row_cluster_sep=THIN_RULE)
# tp.print_solid_mult_row_data(mult_row_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,caption=EXACTS_CAPTION,label=EXACTS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5,row_cluster_sep=THIN_RULE)
# END: PRINTING EVALUATED POLYNOMIALS OR EXACT N-COLORINGS


# BEGIN: PRINTING EXACT N-PARTITIONS
# dict = get_n_partition_counts_dict(get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT)))
# preprocessed_dict = preprocess_big_numbers_for_print(dict,TOO_LARGE_NUM_LIMIT)
# tp.print_solid_mult_col_data(preprocessed_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,EXACT_PARTITIONS_CAPTION,EXACT_PARTITIONS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5)
# END: PRINTING EXACT N-PARTITIONS



# BEGIN: EXACT N-PARTITIONS BASED BOUND PRINTING
# dict = calculate_relabeling_class_bounds(get_n_partition_counts_dict(get_exact_n_colors_dict(get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT))))
# preprocessed_dict = preprocess_bound_tuples_from_dict(dict,TOO_LARGE_NUM_LIMIT)
# tp.print_solid_mult_row_data(preprocessed_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,EXACT_PARTITIONS_BOUNDS_CAPTION,EXACT_PARTITIONS_BOUNDS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5,row_cluster_sep=THIN_RULE)
# END: EXACT N-PARTITIONS BASED BOUND PRINTING


# BEGIN : EXACT ORBITAL EVALS BASED BOUND PRINTING
# dict = calculate_automorphism_class_bounds(get_exact_n_colors_dict(get_solids_poly_evaluations(ocp.orbital_chromatic_polynomial2,EVAL_NUM_LIMIT,tp.STD_PLAT_TABLE_ORDER)))
# preprocessed_dict = preprocess_bound_tuples_from_dict(dict,TOO_LARGE_NUM_LIMIT)
# tp.print_solid_mult_row_data(preprocessed_dict,tp.STD_PLAT_TABLE_ORDER,HEADER,data_headers,ORBITAL_BOUNDS_CAPTION,ORBITAL_BOUNDS_LABEL,transform=wrap_with_dollars,output_type=output_type,first_col_horiz_space=0.5,row_cluster_sep=THIN_RULE)
# END : EXACT ORBITAL EVALS BASED BOUND PRINTING


# BEGIN : PRINTING EVALUATIONS FOR SELECTED SOLIDS
REDUCED_ARCH_TABLE_ORDER = ['truncated tetrahedron', 'cuboctahedron', 'truncated cube', 'truncated octahedron']

CHROMPOLY_ONLY_EVALS_PLATS_CAPTION = f"Evaluated chromatic polynomial of Platonic solids at points {STARTING_NUM} to {EVAL_NUM_LIMIT}."
CHROMPOLY_ONLY_EVALS_PLATS_LABEL = "tab:platonic-chrompolys-evals"
HEADER_PLAT = "Platonic solid"

arch_eval_lim_offset = -1
CHROMPOLY_ONLY_EVALS_ARCH_CAPTION = f"Evaluated chromatic polynomial of Archimedean solids at points {STARTING_NUM} to {EVAL_NUM_LIMIT+arch_eval_lim_offset}."
CHROMPOLY_ONLY_EVALS_ARCH_LABEL = "tab:archimedean-chrompolys-evals"
HEADER_ARCH = "Archimedean solid"

platonic = preprocess_big_numbers_for_print(get_solids_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT,tp.STD_PLAT_TABLE_ORDER),TOO_LARGE_NUM_LIMIT)
tp.print_solid_mult_col_data(platonic,tp.STD_PLAT_TABLE_ORDER,HEADER_PLAT,data_headers,CHROMPOLY_ONLY_EVALS_PLATS_CAPTION,CHROMPOLY_ONLY_EVALS_PLATS_LABEL,output_type=output_type,transform=wrap_with_dollars,first_col_horiz_space=0.5)

archimedean = preprocess_big_numbers_for_print(get_solids_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT+arch_eval_lim_offset,REDUCED_ARCH_TABLE_ORDER),TOO_LARGE_NUM_LIMIT)
tp.print_solid_mult_col_data(archimedean,REDUCED_ARCH_TABLE_ORDER,HEADER_ARCH,data_headers[:arch_eval_lim_offset],CHROMPOLY_ONLY_EVALS_ARCH_CAPTION,CHROMPOLY_ONLY_EVALS_ARCH_LABEL,output_type=output_type,transform=wrap_with_dollars,first_col_horiz_space=0.5)
# END : PRINTING POLY EVALUATIONS FOR SELECTED SOLIDS