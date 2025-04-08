from sage.all import Graph
from sage.all import PolynomialRing, ZZ

# Computes orbital chromatic polynomial of the given graph
# method for calculation can be found here: https://webspace.maths.qmul.ac.uk/p.j.cameron/csgnotes/countcols.pdf

# version with for-else control flow structure
def orbital_chromatic_polynomial(g : Graph):  
    R = PolynomialRing(ZZ, 'x') # create a polynomial ring of integers where the resulting polynomial will live
    p = R(0)
    A = g.automorphism_group()
    for a in A:
        cycles = a.cycle_tuples()
        merged = g.copy()
        for c in cycles:
            if not g.is_independent_set(c): # if any two vertices on a cycle are connected by an edge in the original graph, then this automorphism has empty fixed point
                break
            merged.merge_vertices(c) # all the vertices on the cycle must have same color so we can simulate this by merging them
        else:
            p += merged.chromatic_polynomial()
    p = p / A.order()
    return p

# less verbose version of the algorithm
def orbital_chromatic_polynomial2(g : Graph):  
    R = PolynomialRing(ZZ, 'x') # create a polynomial ring of integers where the resulting polynomial will live
    p = R(0)
    A = g.automorphism_group()
    for a in A:
        cycles = a.cycle_tuples()
        if not all([g.is_independent_set(c) for c in cycles]): # if for some cycle, any two vertices are connected by an edge in the original graph, then no coloring can be fixed
            continue
        merged = g.copy()
        for c in cycles:
            merged.merge_vertices(c) # all the vertices on the cycle must have same color so we can simulate this by merging them
        p += merged.chromatic_polynomial()
    p = p / A.order()
    return p

# adapter for chromatic polynomial function to have the same API as orbital chromatic polynomial
def chromatic_polynomial2(g : Graph):
    return g.chromatic_polynomial()