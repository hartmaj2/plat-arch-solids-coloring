# CCode — C++ orbit counter

A self-contained C++17 port of
[Code/claude_rel_aut_classes_direct.py](../Code/claude_rel_aut_classes_direct.py).
For a graph `G` and an integer `q` it counts the proper `q`-colorings
of `G` modulo `Aut(G) × S_q` using the same algorithm as the Python
version:

1. Read the graph from a JSON file (only the `"edges"` array is used).
2. Compute `Aut(G)` by backtracking with Weisfeiler–Lehman vertex
   invariants.
3. DFS-enumerate every color-canonical surjective proper `q`-coloring
   (collapses the `S_q` action at enumeration time).
4. Map each coloring to its lex-smallest color-canonical image under
   `Aut(G)` and count distinct representatives (parallelized with
   OpenMP when available).

No external libraries are required. JSON files are parsed by a tiny
hand-written extractor for the `"edges"` array.

## Build

From this directory:

```sh
make
```

On macOS, OpenMP requires Homebrew's `libomp`:

```sh
brew install libomp
make
```

If `libomp` is not present the program still builds and runs
single-threaded.

## Usage

```sh
# Run on a JSON file:
./orbits ../Code/JsonGraphs/Platonic/dodecahedron.json 5

# Look up a solid by name (searches Code/JsonGraphs/{Platonic,Archimedean}):
./orbits --solid dodecahedron 5

# Reproduce the Python test: tetrahedron, octahedron, cube, icosahedron, q = 2..8
./orbits --test
```

`--test` writes a summary to `test_rel_aut_classes_direct_cpp.txt`,
matching the layout produced by
[Code/test_rel_aut_classes_direct.py](../Code/test_rel_aut_classes_direct.py).

## Notes

- Vertex labels must be `0..n-1` (this is how all the JSON files in
  `Code/JsonGraphs` are written).
- `q` is limited to ≤ 64 (a `uint64_t` bitmask is used during the
  enumeration). The solids in this project all need `q ≤ 5`.
- For very large coloring counts the program holds the full canonical
  enumeration in memory (≈ `n` bytes per coloring), the same as the
  Python version.
