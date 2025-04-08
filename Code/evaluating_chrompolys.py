#!/usr/local/bin/sage -python

import solids_prep.solids_dict_prep as sdp
import graph_utils.orbital_chrompoly as ocp

from sage.all import *

from collections.abc import Callable
from typing import Any

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

print(get_plat_poly_evaluations(ocp.chromatic_polynomial2,4))


