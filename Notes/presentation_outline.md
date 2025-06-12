# Outline of topics I want to cover in the presentation

## TODO

- [x] remove final slide
- [x] add coloring types slide
  - vertex coloring, total coloring, conversion between colorings
- [x] merge complete k-partite graphs with partition size 2
  - just have slide with the formula as the very first
  - remove latex text above the formula
- [x] -||- pascal triangle
- [x] fix sharpness of octahedron screenshot
- [x] merge computation slide
  - pictures under text (keep the same ones, two next to each other)
- [x] change picture on the problem slide
  - the second coloring should not be possible to be received just by relabeling but relabeling + rotation
- [ ] counting partitions into independent sets
  - with vs without rotations
- [ ] remove transition slides

## Introduction

- what are the objects that my thesis investigates?
- what was the main goal of the thesis?

## Slides outline

1. What are platonic and archimedean solids?
   - definition + examples (pictures)
2. Various types of coloring
   - argument why we show them
   - visualisations
3. Chromatic polynomial
   -  definition + recursive formula
4. Formula for chromatic polynomial of complete k-partite graphs with partite size 2
   - show the formula + visualization
   - don't go into the details of the proof
5. Orbital chromatic polynomial
   - definition of transitivity relation (exists automorphism which preserves colors, rotation)
   - definition + algorithm for computing it
6. Counting partitions into independent sets instead of all colorings
   - define relabeling relation
7. Counting independent sets up to automorphisms

## Latex formulas to use

For a graph $G$ the chromatic polynomial is denoted $P(G,x)$

## Burnside's orbit counting lemma

- $stab(c) = \{ \alpha \in Aut(G) , \alpha(c) = c\}$
  - transformations that leave the coloring $c$ intact

- transitiviity relation $\sim$ defined as $c_1 \sim c_2$ iff there exists automorphism $\alpha$ s.t. $c_1 = \alpha(c_2)$

- orbit
  - $[c]_\sim = \{b \in C, b \sim c\}$

- what is the main idea behind Burnside's counting lemma
  - count the sum of sizes of stabilizers over all colorings
    - show stabilizer forms a subgroup (1. has identity, 2. closed under composition, 3. closed under inverse)
  - use Lagrange's theorem
    - for group $G$ and subgroup $H$ we have: $|H| \cdot k = |G|$ for some $k \in \mathbb{N}$

- count $\sum_{c \in C}|Stab(c)| = \sum_{o \in C / G} \sum_{x \in o}|Stab(c)| = \sum_{o \in C / G} \sum_{x \in o}\frac{|G|}{|o|}$
  - we first rewrote sum and then used Lagrange's theorem (orbit-stabilizer theorem)
- $\sum_{o \in C / G} \sum_{x \in o}\frac{|G|}{|o|} = \sum_{o \in C / G}|G|=|G| \cdot |C/G|$ where $|C/G|$ is what we want

- so the hard part is to prove that $|Stab(x)| \cdot |Orb(x)| = |G|$
  - we have to show that $Stab(x)$ is a group and $Orb(x)$ is the transversal (i.e. its size is the amount of left cosets of $Stab(x)$)