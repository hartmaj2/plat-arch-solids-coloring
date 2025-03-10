#!/usr/local/bin/sage -python

# Computes chromatic polynomials using SageMath function here: https://github.com/sagemath/sage/blob/develop/src/sage/graphs/chrompoly.pyx

# IMPORTS

from sage.all import Graph
from sage.all import *

import solids_prep.solids_dict_prep as sdp
import time

# DEBUG

polys_to_skip = ["truncated icosidodecahedron","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","snub cube","truncated cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron"]


# calls sage code on given data
def compute_chromatic_polynomial(solid_edges : list[tuple]):
    G = Graph(solid_edges)
    poly = G.chromatic_polynomial()
    return poly


# main loop over folders with different solid types (Platonic, Archimedean)
def main():
    solid_name = "snub cube"
    archimedean_edges = sdp.get_archimedean_edges_dict()
    edges = archimedean_edges[solid_name]
    print(solid_name)
    starting_time = time.time()
    print(f"{starting_time=}")
    print(str(compute_chromatic_polynomial(edges)))
    end_time = time.time()
    duration = end_time - starting_time
    print(f"{end_time=}")
    print(f"{duration=}")


if __name__ == "__main__": # __name__ variable is either `__main__` or `json_to_sage`
    main()