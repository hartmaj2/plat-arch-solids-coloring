# Sage notes

## General graphs

Let g be a sage graph:

- g.order() -> num of vertices of the graph
- g.size() -> num of edges of the graph 

## Colorings

- chromatic vertex numbers in sage computed using `all_graph_colorings` function in the general case (if graph not bipartite, not complete etc.)
  - [link](https://github.com/sagemath/sage/blob/develop/src/sage/graphs/graph_coloring.pyx#L420)
  - `all_graph_colorings` computes how many colorings there are for a given number of colors
  - `all_graph_colorings` uses reduction of graph coloring -> exact cover problem -> Dancing links algorithm

## How to make printed colorings in the collages look unified?

- the colorings should be all aligned using some automorphism in a way, s.t. the vertices in corresponding independent sets are at same positions

- throughout the passage through all colorings, we encounter the relabeling-automorphism classes in some order

- we will for each relabeling-automorphism class store the layout of the independent sets of the first representative encountered

### Algorithm
  
1. relaut <- 0
2. for c in colorings
3.   ref, p, a <- coloring in relaut obtained by relabeling p and automorphism a
4.   if no such ref exists: # this is the first representative
5.     relaut <+- c
6.   else:
7.     update coloring c using automorphism a

step 3:
- for coloring in relaut
  - for automorphism in aut(g)
    - try if we can map using an automorphism combined with relabeling to the other coloring