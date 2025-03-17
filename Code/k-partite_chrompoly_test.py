#!/usr/local/bin/sage -python

# Tests the formula from the bachelor thesis for computing chromatic polynomials of complete k-partite graphs with partitions of size 2

# IMPORTS

from sage.all import Graph
from sage.all import *

import math

# calls sage code on given data
def compute_chromatic_polynomial(solid_edges : list[tuple]):
    G = Graph(solid_edges)
    poly = G.chromatic_polynomial()
    return poly

# computation of the chromatic polynomial using the chromatic polynomial function straight away
def direct_computation(n):
    G = graphs.CompleteMultipartiteGraph([2 for i in range(n)])
    poly = G.chromatic_polynomial()
    return poly

# computation of the chromatic polynomial using reduction to sum of chromials of complete graphs
def complete_graph_reduction(n):
    R = PolynomialRing(ZZ, 'x') # create a polynomial ring of integers where the resulting polynomial will live
    poly = R(0)
    x = R.gen() # generator variable of the polynomial ring
    for i in range(n+1):
        # G = graphs.CompleteGraph(2*n-i)
        poly += math.comb(n,i) * math.prod([R(x-j) for j in range(2*n-i)])
    return poly

# just test whether the polynomials using both methods are equal
def test_n_up_to(limit):
    for i in range(limit):
        res1 = direct_computation(i)
        res2 = complete_graph_reduction(i)
        print(f"{i:5}: {res1 == res2}")

# this is good for comparing computing the chromials using both functions, just pass either `direct_computation` or `complete_graph_reduction` as the second argument
def print_first_n_using(n,function):
    for i in range(n):
        print(f"{i:10}: {function(i)}")

def main():

    print_first_n_using(10,complete_graph_reduction)



if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()