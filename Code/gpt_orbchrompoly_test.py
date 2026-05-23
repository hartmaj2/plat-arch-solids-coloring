#!/usr/local/bin/sage -python

from pathlib import Path
import sys

from sage.all import Graph, graphs
from sage.all import Graph, PolynomialRing, QQ

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph_utils.orbital_chrompoly import orbital_chromatic_polynomial

from sage.all import *

def quotient_by_automorphism(G, perm):
    """
    Return Gamma / g, where g is an automorphism of G.

    If a cycle of g contains an edge of G, return None.
    In that case the quotient has a loop, hence chromatic polynomial is 0.
    """
    cycles = perm.cycle_tuples(singletons=True)

    vertex_to_cycle = {}
    for i, C in enumerate(cycles):
        for v in C:
            vertex_to_cycle[v] = i

    # Check whether any vertex cycle contains an edge.
    for u, v in G.edges(labels=False):
        if vertex_to_cycle[u] == vertex_to_cycle[v]:
            return None

    Q = Graph(multiedges=False, loops=False)
    Q.add_vertices(range(len(cycles)))

    for u, v in G.edges(labels=False):
        cu = vertex_to_cycle[u]
        cv = vertex_to_cycle[v]
        if cu != cv:
            Q.add_edge(cu, cv)

    return Q


def orb_chrompoly_gpt3(G):
    R = PolynomialRing(QQ, 'x')
    s = R(0)

    for g in G.automorphism_group():
        c = g.cycle_tuples(singletons=True)
        q = {v:i for i,C in enumerate(c) for v in C}

        if any(q[u] == q[v] for u,v in G.edges(labels=False)):
            continue

        Q = Graph([(q[u], q[v]) for u,v in G.edges(labels=False)])
        s += R(Q.chromatic_polynomial())

    return s / G.automorphism_group().order()

def orb_chrompoly_gpt2(G, var="x"):
    """
    Compute OP_{G, Aut(G)}(x), the orbital chromatic polynomial
    under the full automorphism group Aut(G).
    """
    R = PolynomialRing(QQ, var)
    x = R.gen()

    aut_group = G.automorphism_group()
    total = R.zero()

    for g in aut_group:
        Q = quotient_by_automorphism(G, g)

        if Q is None:
            continue

        total += R(Q.chromatic_polynomial())

    return total / aut_group.order()

def orb_chrompoly_gpt(G):
    """
    Computes the orbital chromatic polynomial of a graph G
    under the action of its automorphism group.

    Parameters:
    G (Graph): A SageMath graph.

    Returns:
    Polynomial: The orbital chromatic polynomial.
    """
    # Compute the automorphism group of G
    aut_group = G.automorphism_group()
    
    # Store unique chromatic polynomials under automorphisms
    colorings = set()
    
    # Loop over all automorphisms in the group
    for phi in aut_group:
        # Relabel the graph according to the automorphism
        relabeled_graph = Graph(G)  # Make a copy
        relabeled_graph.relabel(lambda v: phi(v))  # Correct relabeling method
        
        # Compute the chromatic polynomial and store it
        chrom_poly = relabeled_graph.chromatic_polynomial()
        colorings.add(chrom_poly)
    
    # Compute the orbital chromatic polynomial as the average over unique colorings
    orbital_poly = sum(colorings) / len(colorings) if colorings else 0
    
    return orbital_poly


def make_octahedron_graph() -> Graph:
    # The octahedron graph is the complete 3-partite graph K_{2,2,2}.
    return graphs.CompleteMultipartiteGraph([2, 2, 2])


def main() -> None:
    g = make_octahedron_graph()

    orbital_poly_v1 = orbital_chromatic_polynomial(g)
    orbital_poly_v2 = orb_chrompoly_gpt3(g)

    print("Octahedron graph:")
    print(f"  vertices: {g.num_verts()}")
    print(f"  edges: {g.num_edges()}")
    print(f"  automorphisms: {g.automorphism_group().order()}")
    print()
    print("Orbital chromatic polynomial (version 1):")
    print(orbital_poly_v1)
    print()
    print("Orbital chromatic polynomial (version 2):")
    print(orbital_poly_v2)
    print()
    print("Versions match:")
    print(orbital_poly_v1 == orbital_poly_v2)


if __name__ == "__main__":
    main()