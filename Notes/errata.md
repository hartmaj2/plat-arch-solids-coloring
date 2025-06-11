# Errata in the submitted thesis

## Found myself

### Wrong logical symbol above Lemma 1

- $\{w,x\} \in \bar{E}(G_{\star,\bar{e}}) \implies \{u,x\} \in \bar{E}(G) \vee \{v,x\} \in \bar{E}(G)$
  - was $\wedge$ instead of $\vee$

### Wrong definition of loop

- loop was defined as $l \in \binom{E}{1}$
  - should be $l \in V$

## Found by oponent

### (1) Missing precise definition of Archimedean solid

- archimedean solid
  - all faces congruent to some regular (same sized sides and angles)  convex polygon
  - all vertices are identical (for each pair of vertices $v_1, v_2$ exists an automorphism that maps $v_1$ to $v_2$)
  - not a Platonic solid

### (2) ???

### (3) Chromatic polynomial not shown to really be a polynomial

- comes from the fact that it is a combination of chromatic polynomials of complete graphs which are indeed polynomials

### (4) Magic labeling out of context

- well yes
- wanted to show that there exists other types of colorings where finding conversions to reduce to the same problem would be hard (possibility for further investigation)

### (5) Talk more about what duality does to Platonic and Archimedean solids

### (6) Formulate Brook's and Vizing's theorems

### (7) Show proof of the recursive formula for chromatic polynomial

### (8) Connect formula for k-partite graphs with partition size 2 logically to the rest of thesis

- the connection: more general case of the graph of octahedron

### (9) Lemma 1 should have 2 instead of general n

- for general $n$ there would be $\binom{n}{2}$ non-edges in the partition before the operation and $\binom{n-1}{2}$ non-edges after which does not result in decrease in number of non-edges by $1$
- for $2$ we go from $\binom{2}{2} = 1$ to $0$ non-edges so it holds

### (9) Lemma 2 should also have 2 instead of general n

- for general $n$ the two graphs could be different if partition size where first non-edge was picked had size $i$ and second $j$ s.t. $i \neq j$
  - for $2$ we can only pick non-edges from partitions of same sizes

### (10) Blank spaces at the end of pages

### (11) Mention that orbital polynomial is indeed a polynomial

- it is actually mentioned in the last sentence of Definition $33$

### (12) Should compare bounds given by Claims 7 and 8