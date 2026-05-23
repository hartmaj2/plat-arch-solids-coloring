#!/usr/local/bin/sage -python
# Direct-enumeration version of compute_orbits_fast.
#
# Counts the number of proper q-colorings of G modulo Aut(G) x S_q.
#
# Difference from compute_orbits_fast.py:
#   We do NOT call Sage's `all_graph_colorings`. Instead we enumerate
#   color-canonical proper colorings directly by DFS over a chosen
#   vertex ordering. A coloring is "color-canonical" iff for every i,
#   coloring[i] <= max(coloring[0..i-1]) + 1, i.e. colors appear in
#   order 0, 1, 2, ... of first use. This collapses the S_q color-
#   relabeling action at enumeration time and avoids producing the
#   (up to q!) labeled siblings that all_graph_colorings emits.
#
# Then orbit reduction under Aut(G) is identical to the previous file
# (canonical-form orbit counting via _canon_rep).

from sage.all import Graph, graphs
from sage.graphs.graph_coloring import all_graph_colorings  # only for cross-check / unused

import multiprocessing as mp
import time as tm

import solids_prep.solids_dict_prep as sdp


# --- direct enumeration of color-canonical proper colorings ---------------

def _choose_vertex_order(g):
    """Pick a vertex ordering that maximizes the number of already-placed
    neighbors at each step (good for DFS pruning). Assumes vertices 0..n-1.

    Returns a list `order` of length n where order[k] is the vertex placed
    at position k. The first vertex is one of maximum degree.
    """
    n = g.num_verts()
    deg = [g.degree(v) for v in range(n)]
    in_order = [False] * n
    order = []

    # Start with a max-degree vertex (ties broken by smallest label).
    first = max(range(n), key=lambda v: (deg[v], -v))
    order.append(first)
    in_order[first] = True

    # For each remaining vertex track how many of its neighbors are already placed.
    nb_placed = [0] * n
    for u in g.neighbor_iterator(first):
        nb_placed[u] += 1

    while len(order) < n:
        # Greedy: max nb_placed; ties by max degree; then smallest label.
        best = -1
        best_key = None
        for v in range(n):
            if in_order[v]:
                continue
            key = (nb_placed[v], deg[v], -v)
            if best_key is None or key > best_key:
                best_key = key
                best = v
        order.append(best)
        in_order[best] = True
        for u in g.neighbor_iterator(best):
            if not in_order[u]:
                nb_placed[u] += 1

    return order


def _enumerate_canonical_colorings(g, q):
    """Iteratively enumerate all SURJECTIVE color-canonical proper
    q-colorings of g (i.e. proper colorings that use every color in
    {0, ..., q-1}).

    Returns a list of tuples of length n. Each tuple is indexed by the
    *original* vertex labels of g (assumed 0..n-1), so the output is
    directly comparable with vertex-tuple representations elsewhere.

    Color-canonical means: colors appear in order 0, 1, 2, ... along
    the chosen DFS vertex ordering, which collapses the S_q action at
    enumeration time. Surjectivity is enforced both as a final check
    (max color used == q-1) and as a pruning rule during DFS.

    Symmetry breaking: the first vertex in the ordering is forced to
    color 0.
    """
    n = g.num_verts()
    if n == 0:
        return [tuple()]
    order = _choose_vertex_order(g)
    # neighbors of order[i] that come *before* it in the ordering
    pos = [0] * n
    for k, v in enumerate(order):
        pos[v] = k
    prior_nbrs = [[] for _ in range(n)]  # indexed by k = position in order
    for k in range(n):
        v = order[k]
        for u in g.neighbor_iterator(v):
            if pos[u] < k:
                prior_nbrs[k].append(pos[u])

    results = []
    # coloring_by_pos[k] = color assigned at order-position k
    coloring_by_pos = [0] * n
    # iterative DFS using a stack of (k, candidates_iterator)
    # but recursion is simpler and n is small; use sys.setrecursionlimit safety
    import sys
    sys.setrecursionlimit(max(1000, 10 * n))

    def dfs(k, max_used):
        if k == n:
            # Only accept SURJECTIVE colorings (uses all q colors).
            if max_used == q - 1:
                arr = [0] * n
                for kk in range(n):
                    arr[order[kk]] = coloring_by_pos[kk]
                results.append(tuple(arr))
            return
        # Surjectivity pruning: need to introduce (q-1 - max_used) new colors
        # in the remaining (n - k) positions. Each new color requires at least
        # one position, so this is necessary.
        remaining = n - k
        needed = (q - 1) - max_used
        if needed > remaining:
            return
        used = 0  # bitmask of colors used by prior neighbors
        for j in prior_nbrs[k]:
            used |= 1 << coloring_by_pos[j]
        limit = max_used + 1
        if limit > q - 1:
            limit = q - 1
        for c in range(limit + 1):
            if used & (1 << c):
                continue
            coloring_by_pos[k] = c
            new_max = max_used if c <= max_used else c
            dfs(k + 1, new_max)

    dfs(0, -1)
    return results


# --- orbit reduction (same logic as compute_orbits_fast.py) ----------------

def _canon_rep(coloring, automorphisms):
    """Lex-smallest color-canonical form of `coloring` under Aut(G)."""
    n = len(coloring)
    best = None
    for sigma in automorphisms:
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


def _automorphisms_as_lists(graph):
    n = graph.num_verts()
    auts = []
    for a in graph.automorphism_group():
        d = a.dict()
        auts.append(tuple(d[i] for i in range(n)))
    return auts


def _normalize_graph(graph):
    g = graph.copy(immutable=False)
    g.relabel()
    return g


# --- main API -------------------------------------------------------------

def compute_num_orbits_direct(graph, num_clr, verbose=False,
                              processes=None, chunksize=None):
    """Number of proper q-colorings of `graph` modulo Aut(G) x S_q,
    using direct DFS enumeration of color-canonical colorings.
    """
    t0 = tm.time()
    g = _normalize_graph(graph)
    auts = _automorphisms_as_lists(g)
    t_auts = tm.time() - t0

    t1 = tm.time()
    canonical = _enumerate_canonical_colorings(g, num_clr)
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

# INPUT
SOLID_NAME = "dodecahedron"
NUM_CLRS = 5
# G = graphs.PetersenGraph()
G = Graph(sdp.get_all_solids_dict()[SOLID_NAME][sdp.JSON_EDGES])


if __name__ == "__main__":
    mp.freeze_support()
    total = tm.time()
    num_classes = compute_num_orbits_direct(G, NUM_CLRS, verbose=True)
    total = tm.time() - total

    with open(f"out_{SOLID_NAME}_{NUM_CLRS}.txt", "w") as f:
        print(f"{'INPUT':-^20}", file=f)
        print(f"{SOLID_NAME=}", file=f)
        print(f"{NUM_CLRS=}", file=f)
        print(f"{'OUTPUT':-^20}", file=f)
        print(f"{num_classes=}", file=f)
        print(f"time={total:.3f}", file=f)

    print(f"num_classes = {num_classes}")
    print(f"wall time   = {total:.3f}s")
