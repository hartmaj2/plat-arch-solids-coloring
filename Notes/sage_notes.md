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