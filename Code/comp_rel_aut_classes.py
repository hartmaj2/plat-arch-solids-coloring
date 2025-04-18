#!/usr/local/bin/sage -python
# Compute number of colorings up to symmetries and relabeling of the color classes

import solids_prep.solids_layout_prep as slp

import itertools
import timing.timing as tmng

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import all_graph_colorings

from collections.abc import Callable

# BEGIN: GETTING ALL COLORINGS AS LIST
# converts the coloring in dict format to list format
def get_coloring_list(clring_as_dict : dict[int,list]) -> list[int]:
    num_vertices = len(reduce(lambda x,y: x + y,clring_as_dict.values(),[])) # reduce is equivalent of foldl in functional programming languages
    clring_as_list = [0 for _ in range(num_vertices)]
    for color in clring_as_dict.keys():
        for vtx in clring_as_dict[color]:
            clring_as_list[vtx] = color
    return clring_as_list

# returns a MathSage all colorings where each coloring is a list indexed by vertex and containing the value of the color at each position
def all_graph_colorings_list(g : Graph, num_clrs : int, *args) -> list[list]:
    colorings = all_graph_colorings(g,num_clrs,*args) # coloring is represented as dict in format: color -> list of vertices with that color (color is an int)
    clrings_list = []
    for coloring in colorings:
        clrings_list.append(get_coloring_list(coloring))
    return clrings_list
# END: GETTING ALL COLORINGS AS LIST


# BEGIN: REMOVING COLORINGS SAME UP TO RELABELING OF THE COLORS
# checks if coloring is in canonic form, the canonic form represents all colorings with the same structure but different permutation of color values
# canonic form is following: for the given coloring, it must have the colors ordered from lowest to highest when going from left to right through the coloring list
# assumes that colors are numbers from 0 ... k
def is_in_canonic_form(coloring : list[int]) -> bool:
    count = 0
    for clr in coloring:
        if clr > count:
            return False
        if clr == count:
            count += 1
    return True

# removes non canonic colorings out of the list of colorings
def get_canonized(clrings : list[list]) -> list[list]:
    return [c for c in filter(is_in_canonic_form,clrings)]
# END: REMOVING COLORINGS SAME UP TO RELABELING OF THE COLORS


# BEGIN: FINDING REPRESENTATIVES OF AUTOMORPHISM EQUIVALENCE CLASSES
# to be properly unified, the for all vertices, the color must be the same as the relabeled color on the permuted graph
# the relabel is a permutation given as tuple, if val at position i is j, it means that color i is permuted to j
def can_unify_using_relabel_and_aut(c1 : list[int], c2 : list[int], a : list[tuple], relabel : tuple) -> bool:
    for cycle in a:
        k = len(cycle)
        for i in range(k):
            vtx_preim = cycle[i]
            vtx_img = cycle[(i+1)%k]
            b1 = relabel[c1[vtx_preim]]
            b2 = c2[vtx_img]
            if b1 != b2:
                return False
    return True

# tries to unify colorings using automorphism a by also applying some permutation of colors (now I can just try looping through all possible color permutations)
# returns the permutation for which this automorphism is equivalent or None 
# finds the relabeling using a brute force through all permutations of colors (for our purposes we have at most 4 clrs so there will be only 4!=24 of those)
def try_unify_by_aut(c1 : list[int], c2 : list[int], a : list[tuple], num_clrs : int) -> tuple | None:
    for p in itertools.permutations(range(num_clrs)):
        if can_unify_using_relabel_and_aut(c1,c2,a,p):
            return p
    return None

# tries to unify two colorings by building a permutation of colors on the fly
# the permutation has to be valid and all vertices have to be checked
# permutation is invalid if two colors try to map to the same color or if one color tries to map to multiple colors
# permutation will be represented by two lists: img and preimg
def try_unify_by_aut2(c1 : list[int], c2 : list[int], a : list[tuple], num_clrs : int) -> tuple | None:
    img = [-1] * num_clrs # -1 means mapped to no color yet
    preimg = [-1] * num_clrs # -1 means no color mapped to this yet
    for cycle in a:
        k = len(cycle)
        for i in range(k):
            vtx_preim = cycle[i]
            vtx_img = cycle[(i+1)%k]
            b1 = c1[vtx_preim]
            b2 = c2[vtx_img]
            if img[b1] == -1: # b1 not mapped to anything yet
                if preimg[b2] != -1: # some other color has already mapped to b2
                    return None
                else: # we can map b1 -> b2
                    img[b1] = b2
                    preimg[b2] = b1
            else:
                if img[b1] != b2: # we have already mapped to some other color so we cannot map to this one as well
                    return None
    return tuple(img)

# function that receives two colorings and a graph and returns automorphism (as list of cycles) and relabeling by which they can be unified or None
# result means that we can get from c1 to c2 using automorphism a and relabel r in the returned (a,r) tuple 
def get_unification_proof(c1 : list[int], c2 : list[int], auts_as_cycles : list[list[tuple]], num_clrs : int, unification_func: Callable[[list[int],list[int],list[tuple],int],tuple | None]) -> tuple[list[tuple],tuple] | None: # -> (automorphism, relabeling) or None
    for aut in auts_as_cycles:
        res_relabel = unification_func(c1,c2,aut,num_clrs)
        if res_relabel is not None:
            return aut,res_relabel
    return None

# returns a dictionary where keys are the representative colorings and the values are lists of colorings that are relaut eqivalent to it
def get_classified_by_relaut_eqiv_class(clrings : list[list[int]], g : Graph, num_clrs : int, unification_func: Callable[[list[int],list[int],list[tuple],int],tuple | None]) -> dict[tuple,list[list[int]]]:
    classified : dict[tuple,list[list[int]]] = {} 
    auts_as_cycles = [a.cycle_tuples(singletons=True) for a in g.automorphism_group()]
    for c_curr in clrings:
        for c_repr in classified.keys():
            uni_proof = get_unification_proof(c_curr,list(c_repr),auts_as_cycles,num_clrs,unification_func)
            if uni_proof is None: # the coloring is not automorph+relabel equivalent to the c_repr representant
                continue
            else:
                classified[c_repr].append(c_curr)
                break # we don't want to check for more ways to transform this coloring to the same representant
        else : # there was no representant to which we can rel+automorph
            hashable_curr = tuple(c_curr)
            classified[hashable_curr] = [c_curr] # set this coloring as a representant

    return classified


# BEGIN: FINDING REPRESENTATIVES OF AUTOMORPHISM EQUIVALENCE CLASSES


# SOLID SETTINGS
SOLID_NAME = "icosahedron"
NUM_CLRS = 5

# GRAPH DATA
G = Graph(slp.get_labeled_neighbor_dict(SOLID_NAME))

def run_alg_using(unification_func: Callable[[list[int],list[int],list[tuple],int],tuple | None]):
    colorings,time1 = tmng.run_and_get_time(all_graph_colorings_list,G,NUM_CLRS)
    canonized,time2 = tmng.run_and_get_time(get_canonized,colorings)
    classified,time3 = tmng.run_and_get_time(get_classified_by_relaut_eqiv_class,canonized,G,NUM_CLRS,unification_func)
    print_results(colorings,time1,canonized,time2,classified,time3)

def print_results(clrings : list[list[int]], t1 : float, cnnized : list[list[int]], t2 : float, clssfied : dict[tuple,list[list[int]]], t3 : float):
    c1_size = 20
    c2_size = 10
    print(f"{"Solid:":{c1_size}}{SOLID_NAME}\n{"Num clrs:":{c1_size}}{NUM_CLRS}\n{"Equiv classes:":{c1_size}}{len(clssfied.keys())}")
    print()
    print(f"{"All colorings:":{c1_size}}{len(clrings):<{c2_size}}{t1:.3}\n{"Canonization:":{c1_size}}{len(cnnized):<{c2_size}}{t2:.3}\n{"Classification:":{c1_size}}{len(clssfied.keys()):<{c2_size}}{t3:.3}")

print(50*"-")
print("RUN 1")
run_alg_using(try_unify_by_aut)
print(50*"-")
print()
print("RUN 2")
run_alg_using(try_unify_by_aut2)
print(50*"-")
