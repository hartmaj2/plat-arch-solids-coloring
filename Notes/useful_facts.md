# Relevant mathematical facts, proofs and techniques

## Geometry and combinatorics
- all convex polyhedra correspond to planar graphs (Kapitoly 6.6) 
- there is only five platonic solids (Kapitoly 6.6)
- planar graphs have X(G) <= 4 [Appel & Haken](https://en.wikipedia.org/wiki/Four_color_theorem) (1976)
- planar graphs without triangles X(G) <= 3 [Grötzsch](https://en.wikipedia.org/wiki/Gr%C3%B6tzsch%27s_theorem) (1959)
- 3-vertex-connected planar graphs <=> 3d convex polyhedra (1916 - Steinitz)(1967 - Grünbaum) [Steinitz](https://en.wikipedia.org/wiki/Steinitz%27s_theorem)

## Algebra

- Lagrange's theorem
  - if I have a subgroup of a group, its size always divides the size of the group

- things to grasp intuitively
  - why cosets of a subgroup are disjoint in general?
    - the concrete example of this -> when I take cosets based on the rotation, they must also be disjoint
    - good question for later: why will they cover all elements of the group?

- useful notation to remember:
  - transversal - defined for a subgroup
    - I am a transversal if I apply all elements on the group and from their cosets, I have exactly one element in the intersection with each of them
  - index - defined for a subgroup
    - number of different cosets that can be formed by applying some element on the subgroup on them 

## How does Lagrange's theorem help in counting different colorings up to rotations and symmetries

- what does it mean to count up to rotations and symmetrie?
  - if we can get from one coloring to another by using the transformation, we want to consider it a same object -> only count it once
  - we call all the colorings that we can get to using some transformation an `orbit`

- observation:
  - orbits can be defined using a relation ~ where a ~ b iff exist transformation p s.t. p(a) = b
  - it can be shown that this relation is an equivalence -> no two orbits overlap

- let G be the set of all transformations
- let C be the set of all colorings
- let stab(c) be the set of all transformations, that leave the coloring unchanged (the result is not a different coloring)
- let orb(c) be the set of all elements in the orbit of c

- objective: count the number of orbits (those are exactly the colorings unique up to transformations)

- to get the number of orbits, Burnside's lemma gives us a very nice formula:
  - `sum{c in C}( |stab(c)| ) = |G| * |{orb(c) : c in C}|`
  - at first, this might seem very obscure
  - for the formula to hold, one crusial relation must be established, that is a relation between the index of stabilizer of some element and the size of the orbit of that element

- here we need to define, what an index is and for that, we need to define what a coset is
- these are group concepts

- cosets are sets that can be created by applying a given transformation from G on all choices of transformations from a subgroup H
- by using algebra, it can be shown, that given a subgroup H (some chosen transformations that behave nicely), its cosets partition the set of all transformatins G into evenly sized sets => the size of a subgroup must always divide the size of the group
- not we can define index
  - index of a subgroup H is the amount of partitions that are form, when we take all cosets of H
  - we can think of H as a choice of some transformations that leave a given coloring c untouched (they form a subgroup stab(c)) 
  - then if we compose all other transformation with the transformations from the stabilizer, we get a partitioning of all the transformations from G
  - the index will then be the number of different cosets that will be created this way

- now, we would like to show, that the number of different cosets of the stab(c) will be equal to the number of orbits |orb(c)|
  - if we show that we will be able to apply Lagrange's theorem on stab(c) (we can do that bcs stab(c) forms a subgroup) we will then obtain
  - `|G| = |stab(c)| * |orb(c)|`
    - the important thing to notice about the equation above is, that it makes the result of taking ANY element and multiplying size of its stab(c) by size of orb(c) a constant so we get same result for any coloring we go through

- so we have `sum{c in C}( |stab(c)| ) = sum{orb(c) in orbs}[sum{a in orb(c)}[|stab(c)|]] = sum{orb(c) in orbs}[sum{a in orb(c)}[|stab(c)|]]`
  - now I use the fact, that for all colorings in the same orbit, the size of their stabilizers is the same
  - `sum{orb(c) in orbs}[sum{a in orb(c)}[|stab(c)|]] = sum{orb(c) in orbs}[ |stab(c)| * sum{a in orb(c)}[1]] = sum{orb(c) in orbs}[ |stab(c)| * |orb(c)| ]`
  - now we can finally use the observation above which tells us that the term inside the sum is a constant no matter what our orbit is
  - `= |G| * sum{orb(c) in orbs}[ 1 ] = |G| * |{orb(c) : c in C}|` so we got a formula for counting the amount of orbits

- note:
  - we can use coounting in two ways to also establish the formula from perspective of summing size of fixpoints over all possible transformations