# Errata in the submitted thesis

## Found myself

### Wrong logical symbol above Lemma 1

- $\{w,x\} \in \bar{E}(G_{\star,\bar{e}}) \implies \{u,x\} \in \bar{E}(G) \vee \{v,x\} \in \bar{E}(G)$
  - was $\wedge$ instead of $\vee$

### Wrong definition of loop

- loop was defined as $l \in \binom{E}{1}$
  - should be $l \in V$

## Found by oponent

### Copy of oponent statements

Některé konkrétní připomínky:
- str. 8: Mezi archimedovská tělesa nejsou zahrnuta prismata a antiprismata!
- str. 9 (nebo i jinde): Bylo by vhodné zmínit, že 3-souvilé rov. grafy mají jistým způsobem
unikátní nakreslení v rovině.
- str. 12, Def. 11: Je zaveden chromatický polynom jako funkce. To, že tato funkce je
polynomem ale není ještě několik stran vůbec patrné.
- str. 15: Koncept Magic labelings je sice zajímavý, ale zde je poměrně vytržený z
kontextu a pro zbytek práce není třeba. Jaký byl důvod jeho uvádění?
- str. 18: V souvislosti se stěnovým barvením a dualitou by bylo možné zmínit, jak funguje
v rámci platonských a archimedovských těles.
- str. 21: Jsou zmíněny Brooksova a Vizingova věta, které však nejsou vůbec formulovány
jako tvrzení.
- str. 21, Eq. (4.1): Bylo by vhodné formulovat jako Lemma s důkazem.
- str. 22 (23): Sekce 4.3 nesouvisí se zbytkem práce. Bylo by vhodné ji nějak uvést s
logicky propojit.
- str. 22: V lematech 1 a 2 je třeba nahradit obecné n hodnotou 2.
- str. 23: Prázdné místo na konci stránky je typografickou chybou. V menší míře též na str.
33, 35, 43.
- str. 31: Není ukázáno, že Orbital chromatic pol. je vůbec polynom. Plyne to z Věty 6,
není to ale vůbec zmíněno.
- str. 40 a 41: Přišlo by mi zajímavé porovnání výsledků Cl. 7 a 8 v jedné tabulce s
patříčným komentářem.

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