# TODOs for bachelor thesis

## 2024_12_10

- [x] look at how other bachelor theses look
  - [x] how is abstract written
  - [x] how are definitions written
  - [x] what are the creative parts

## 2025_02_13

- [x] review all work done so far
- [x] write definitions of colorings
- [x] look for picture visualisations of operations on platonic solids 
  - truncation, rectification, expansion, snub

## 2025_02_16

- [x] define other colorings and add examples on cubic graph / or octahedral graph
- [x] define total coloring and add example

### 2025_02_17

- [x] prepare questions to ask supervisor
- [x] sum up what I did since last meeting
- [x] put table with vtx and edge chromatic nums to the thesis

- [x] add source to figures from Wikipedia
- [x] fix definition wordings
  - use inline definition and tag
- [x] Share overleaf link with supervisor + github repo link

### 2025_02_20

- [x] write definition of chromatic polynomial
- [x] find out how hard it is to find a formula of chromatic polynomial in general
  - what are some methods to calculate by hand?
  - read the definition inside "Chromatic Graph Theory" book

### 2025_02_21

- [x] check what could be useful from KG 2 on MFF 
  - maybe some chromatic polynomial theory?

- [x] calculate chromatic polynomials of platonic solids

### 2025_02_22

- [x] calculate chrom polys of polyhedra for which it runs in reasonable time (i.e. under a minute or so)

- [x] fix the general definition of colorings

## 2025_02_24

- [x] add paragraph about all Platonic and Archimedean solids being in Vizing class one (show degrees of the graphs in the table as well)

## 2025_03_01

- [x] read about different coloring types where value of color matters
  - [x] rainbow coloring (more to do with connectivity of graph, the value does not actually matter)
  - [x] magic labeling

- [x] write definitions of the colorings above and add example figures

- [x] add bibliography resources for the definitions above

## 2025_03_02

- [x] how to convert special colorings to vertex coloring by transforming the graph to a different graph
  - [x] describe and add figures to visualize
  - [x] implement in python and compute the chromatic numbers for these colorings

## 2025_03_03

- [x] comment the results for total chromatic number
  - [x] check if correct for tetrahedron

- [x] prune unused code in the printers
  - [x] for compatibility add caption and label params to md printer as well (can just be ignored)
  - (i don't need the specific printers anymore)

- [x] change format of Bachelor thesis to the correct new one
  - [link](https://gitlab.mff.cuni.cz/teaching/thesis-templates/thesis-en)
  - first create new overleaf project and make sure everything works properly
    - links
    - supervisor todo environment
    - tables 
    - figures
    - references
  - when that really works, move the documents from the temporary project to the main project

## 2025_03_04

- [x] finish reading Polya from supervisor

## 2025_03_09

- [x] find out why my computation leads to 48 automorphisms of cube instead of 24 as in Polya.pdf

- [x] find out what result I get when I use all 48 automorphisms of cube

## 2025_03_10

- [ ] check if automorphism calculations for platonic solids correct

- [ ] start writing chapter outline
  - symmetries
  - operations on platonic solids interpreted on graphs

- [ ] use Burnside/Polya to calculate only valid colorings of the objects

- [ ] find out how I can enumerate automorphisms of some objects and get their cycle counts and lengths

- [ ] sum up all my questions so far and prepare them in the document for next meeting

## Main tasks

- [x] finish reading Polya from supervisor

- [ ] compute how many arrangments of k independent sets exist on various solids (start with tetrahedron, cube etc.)

- [ ] revise what Brook's theorem about coloring says
  - [ ] mention it in my thesis under vertex coloring

- [ ] write an introduction to the chapter about symmetries
  - [ ] how do we define symmetry
  - [ ] how will we work with symmetry throughout my thesis
  - [ ] define, what it means for two colorings to be different up to taking symmetries
    - using equivalence classes of transitivity relation (group actions)

## Side tasks

- [ ] what do operations on the Platonic solids do on the graphs?

- [ ] read useful resources found on 19.2.2025

- [ ] find nice visualisation for snub operation

- [ ] consider, how the number of colorings of tetrahedral graph changes (the chromatic polynomial) when taking difference only up to symmetries

- [ ] figure out nice proof why automorphisms correspond exactly to valid transformation of the objects
  - [ ] what does it mean for a transformation of 2d-shape/solid to be valid?
    - (no tearing edges etc.)

- [ ] what is the dividing property between rotations and reflections?
  - rotations seem to disallow flipping the shape/solid using one more dimension than the dimension that the shape/solid lives in (think about 2d square being reflected is as if it was rotated by axis that exists only when considering 3d)