from sage.all import Graph
from sage.all import PolynomialRing, ZZ

# Computes orbital chromatic polynomial of the given graph
# method for calculation can be found here: https://webspace.maths.qmul.ac.uk/p.j.cameron/csgnotes/countcols.pdf

def orbital_chromatic_polynomial(g : Graph):  

    R = PolynomialRing(ZZ, 'x') # create a polynomial ring of integers where the resulting polynomial will live
    p = R(0)

    A = g.automorphism_group()

    for a in A:
        cycles = a.cycle_tuples()
        valid_cycles = True
        merged = g.copy()
        for c in cycles:
            if not g.is_independent_set(c): # if any two vertices on a cycle are connected by an edge in the original graph, then this automorphism has empty fixed point
                valid_cycles = False
                break
            merged.merge_vertices(c) # all the vertices on the cycle must have same color so we can simulate this by merging them
        if not valid_cycles:
            continue
        p += merged.chromatic_polynomial()

    p = p / A.order()
    return p
    


