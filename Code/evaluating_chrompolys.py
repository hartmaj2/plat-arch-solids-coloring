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
TOO_LARGE_NUM_LIMIT = 10_000_000
THIN_RULE = r"\specialrule{0.2pt}{0.65ex}{0.65ex}"

data_headers = [str(x) for x in range(2,EVAL_NUM_LIMIT+1)]

PLAT_CAPTION = f"Evaluated chromatic polynomial and orbital chromatic polynomial for platonic solids at points 2 to {EVAL_NUM_LIMIT}. For each solid, top row is the chromatic polynomial, bottom row is the orbital chromatic polynoial."
PLAT_LABEL = "tab:platonic-polys-evals"
HEADER = "solid name"

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
output_file = open(ROOT_FOLDER + "/Results/poly_evals.md","w")
output_type = output_file

# import sys
# output_type = sys.stdout

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

chrompolys = get_platonic_poly_dict(ocp.chromatic_polynomial2)
orbchrompolys = get_platonic_poly_dict(ocp.orbital_chromatic_polynomial2)

# evaluates the polynomials from 2 to k (start at 2 because obviously no graph can be 1 colored as long as it has some edge)
def get_plat_poly_evaluations(poly_calc_func : Callable[[Graph],Any], k : int) -> dict [str,tuple]:
    polys = get_platonic_poly_dict(poly_calc_func)
    evals = {}
    for name,poly in zip(polys.keys(),polys.values()):
        vals = tuple([poly(i) for i in range(2,k+1)])
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
        new[key] = tuple(new_vals)
    return new

# takes a list of dicts where each dict has the same key set and then appends the rows in the dicts to create multiple rows for each key
def create_mult_row_dict(dicts : list[dict]):
    new = {}
    for key in dicts[0].keys():
        new[key] = []
        for dict in dicts:
            new[key].append(dict[key])
    return new

dicts = [get_plat_poly_evaluations(ocp.chromatic_polynomial2,EVAL_NUM_LIMIT),get_plat_poly_evaluations(ocp.orbital_chromatic_polynomial2,EVAL_NUM_LIMIT)]
preprocessed_dicts = [preprocess_for_print(d,TOO_LARGE_NUM_LIMIT) for d in dicts]

mult_row_dict = create_mult_row_dict(preprocessed_dicts)

tp.print_solid_mult_row_data(mult_row_dict,HEADER,data_headers,caption=PLAT_CAPTION,label=PLAT_LABEL,transform=wrap_with_dollars,row_cluster_sep=THIN_RULE)



