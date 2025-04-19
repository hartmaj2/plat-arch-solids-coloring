# Thesis overview

This document contains an overview of the topics discussed in the thesis. It is useful to get the big picture and see how the parts of the thesis interact?

## Overview

### Introduction to Platonic solids and Archimedean graph

- defining platonic and archimedean solids
- summary of properties of graphs of platonic and archimedean solids

### Overview of types of colorings

- defining what key properties all the colorings share
- defined particular types of colorings that exist
  - demonstrated examples of these colorings on platonic and archimedean solids
  - also defined some colorings that I have not used later (rainbow coloring, magic labeling)

### Connections between the colorings

- showed how some types of colorings can be obtained from other types by converting the underlying graph
- demonstrated these conversions on graphs of platonic and archimedean solids

### Chromatic numbers and chromatic polynomials

- provided examples of chromatic numbers for certain types of colorings 
  - vertex, edge and total colorings
- showed recursive formula for computing the chromatic polynomial
- examples of chromatic polynomials
- method to calculate colorings with exactly n colors from the values of the chromatic polynomial
- demonstrated limitations of the chromatic polynomials

### Symmetries

- introduced the theory behind Burnside's lemma
- introduced the orbital chromatic polynomial and algorithm for computing it
  - implemented the algorithm and showed the results I obtained
  - compared the results with the regular chromatic polynomial

### Counting independent sets

- showed a method to count independent sets irrespective of the particular names of the colors
- introduced the notion that avoids both counting relabeled independent sets multiple times but also the rotations
  - showed difficulty of computing it when compared to the method when rotations not taken into account
  - showed what bounds on the target number we can make based on the orbital chromatic polynomial and also based on the number of indep sets (not up to rotation)
- provide a semi brute force algorithm to arrive at the target number
  - showed results that I calculated using the algorithm