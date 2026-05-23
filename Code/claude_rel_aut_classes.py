#!/usr/local/bin/sage -python
# Optimized replacement for Strategies.compute_divided_by_fprint_multiprocessed
# from comp_rel_aut_classes.py.
#
# Counts the number of proper q-colorings of G modulo Aut(G) x S_q
# (i.e. modulo graph automorphisms AND relabeling of color classes).
#
# Strategy: canonical-form orbit counting.
#   For each proper coloring c, compute
#       canon(c) := lex-min over sigma in Aut(G) of   color_canonicalize(c o sigma)
#   where color_canonicalize relabels colors by their order of first appearance.
#   Two colorings are Aut x S_q equivalent iff they share the same canon.
#   Answer = |{ canon(c) : c proper coloring }|.
#
# This is O(K * |Aut(G)| * n) and embarrassingly parallel, vs. the quadratic
# pairwise unification done by the original strategy.

from sage.all import Graph, graphs
from sage.graphs.graph_coloring import all_graph_colorings

import multiprocessing as mp
import time as tm

# --- core primitives -------------------------------------------------------

def _color_canonicalize(coloring):
    """Relabel colors by order of first appearance (0, 1, 2, ...)."""
    mapping = {}
    nxt = 0
    out = []
    for c in coloring:
        m = mapping.get(c)
        if m is None:
            mapping[c] = nxt
            out.append(nxt)
            nxt += 1
        else:
            out.append(m)
    return tuple(out)


def _canon_rep(coloring, automorphisms):
    """Lex-smallest color-canonical form of `coloring` under Aut(G).

    `automorphisms` is a list of permutations, each a tuple of length n
    with perm[i] = image of vertex i (vertices assumed to be 0..n-1).
    """
    n = len(coloring)
    best = None
    for sigma in automorphisms:
        # Apply sigma: relabeled[i] = coloring[sigma[i]].
        # Inline color canonicalization for speed (this is the hot loop).
        mapping = {}
        nxt = 0
        out = [0] * n
        for i in range(n):
            col = coloring[sigma[i]]
            m = mapping.get(col)
            if m is None:
                mapping[col] = nxt
                out[i] = nxt
                nxt += 1
            else:
                out[i] = m
        t = tuple(out)
        if best is None or t < best:
            best = t
    return best


# --- multiprocessing worker plumbing --------------------------------------

_WORKER_AUTS = None


def _worker_init(auts):
    global _WORKER_AUTS
    _WORKER_AUTS = auts


def _worker_process_chunk(chunk):
    auts = _WORKER_AUTS
    seen = set()
    for c in chunk:
        seen.add(_canon_rep(c, auts))
    return seen


# --- helpers --------------------------------------------------------------

def _coloring_dict_to_tuple(d, n):
    arr = [0] * n
    for col, vs in d.items():
        for v in vs:
            arr[v] = col
    return tuple(arr)


def _automorphisms_as_lists(graph):
    """Return Aut(G) as a list of permutation tuples on 0..n-1."""
    n = graph.num_verts()
    auts = []
    for a in graph.automorphism_group():
        d = a.dict()
        auts.append(tuple(d[i] for i in range(n)))
    return auts


def _normalize_graph(graph):
    """Return a copy of graph with vertices relabeled to 0..n-1."""
    g = graph.copy(immutable=False)
    g.relabel()
    return g


# --- main API -------------------------------------------------------------

def compute_num_orbits_fast(graph, num_clr, verbose=False,
                            processes=None, chunksize=None):
    """Number of proper colorings of `graph` using up to `num_clr` colors,
    modulo Aut(G) x S_{num_clr}.
    """
    t0 = tm.time()
    g = _normalize_graph(graph)
    auts = _automorphisms_as_lists(g)
    t_auts = tm.time() - t0

    # Enumerate proper colorings, color-canonicalize, deduplicate.
    t1 = tm.time()
    n = g.num_verts()
    canonical = set()
    for d in all_graph_colorings(g, num_clr):
        canonical.add(_color_canonicalize(_coloring_dict_to_tuple(d, n)))
    canonical = list(canonical)
    t_enum = tm.time() - t1

    if verbose:
        print(f"automorphisms:                  {len(auts):>10}  ({t_auts:.3f}s)")
        print(f"color-canonical proper colorings:{len(canonical):>10}  ({t_enum:.3f}s)")

    if not canonical:
        if verbose:
            print(f"orbit representatives:          {0:>10}  (0.000s)")
            print(f"total:                                       {tm.time() - t0:.3f}s")
        return 0

    if processes is None:
        processes = mp.cpu_count()
    if chunksize is None:
        # aim for ~4 chunks per worker for load balancing
        chunksize = max(1, len(canonical) // (processes * 4))

    t2 = tm.time()
    if processes <= 1 or len(canonical) <= chunksize:
        _worker_init(auts)
        reps = _worker_process_chunk(canonical)
    else:
        chunks = [canonical[i:i + chunksize]
                  for i in range(0, len(canonical), chunksize)]
        reps = set()
        with mp.Pool(processes=processes,
                     initializer=_worker_init,
                     initargs=(auts,)) as pool:
            for partial_set in pool.imap_unordered(_worker_process_chunk, chunks):
                reps |= partial_set
    t_orbits = tm.time() - t2

    if verbose:
        print(f"orbit representatives:          {len(reps):>10}  ({t_orbits:.3f}s)")
        print(f"total:                                       {tm.time() - t0:.3f}s")

    return len(reps)


# --- script entry ---------------------------------------------------------

import solids_prep.solids_dict_prep as sdp
# INPUT
SOLID_NAME = "dodecahedron"
NUM_CLRS = 4
# G = graphs.PetersenGraph()
G = Graph(sdp.get_all_solids_dict()[SOLID_NAME][sdp.JSON_EDGES])


if __name__ == "__main__":
    mp.freeze_support()
    num_classes, total = None, tm.time()
    num_classes = compute_num_orbits_fast(G, NUM_CLRS, verbose=True)
    total = tm.time() - total

    with open("output_fast.txt", "w") as f:
        print(f"{'INPUT':-^20}", file=f)
        print(f"{SOLID_NAME=}", file=f)
        print(f"{NUM_CLRS=}", file=f)
        print(f"{'OUTPUT':-^20}", file=f)
        print(f"{num_classes=}", file=f)
        print(f"time={total:.3f}", file=f)

    print(f"num_classes = {num_classes}")
    print(f"wall time   = {total:.3f}s")
