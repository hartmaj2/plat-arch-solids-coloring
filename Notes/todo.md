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

- [x] check if automorphism calculations for platonic solids correct

- [x] start writing chapter outline
  - symmetries
  - operations on platonic solids interpreted on graphs

- [x] sum up all my questions so far and prepare them in the document for next meeting

- [ ] use Burnside/Polya to calculate only valid colorings of the objects

- [ ] find out how I can enumerate automorphisms of some objects and get their cycle counts and lengths

- [ ] calculate chrom poly of `snub cube` using faculty HPC

## 2025_03_12

- [ ] write down relevant chapters from `Graph Coloring Problems`

- [x] test if my proposed contraction method for calculating fixpoint sizes yields sensible results (on C_4 and 3 colrs)

## 2025_03_13

- [x] calculate how my method works on cube

- [x] implement algorithm to calculate that automatically

## 2025_03_15

- [x] try to make my tables more presentable (correct format)

- [x] update visuals of the graph props table of the solids to new look

- [x] make md table printing also compatible with chrompoly computing program and remove one col data printer

- [x] iplement function in solid dict prep to give me just selected solids
  - will take list of names of solids I want

- [x] change chromatic poly table to include only the short polys (cube, octahedron, tetrahedron)

- [x] remove the definition of graph drawing and just add reference to a book where it is defined and state that we will understand graph drawing in the same way

- [x] change keywords in definitions to `\emph{keyword}` instead of `\textbf{keyword}`

## 2025_03_16

- [x] improve the argument for computation of chromatic polynomial of the octahedron
  - maybe label the graph resulting from the sequence of operations earlier so I can refer to it
  - maybe state the result as lemma? or theorem?

## 2025_03_17

- [x] test the formula form computing chromial of complete k-partite graphs with partition size 2

## 2025_03_19

- [x] write down all definitions that are necessary before defining what an orbital polynomial is
   - [x] transitivity relation
   - [x] stabilizer

## 2025_03_22

- [x] mention Burnside's lemma in the thesis
  - [x] define fixpoint

- [x] define the orbital chromatic polynomial

- [ ] show how orbital chromatic polynomial is computed
  - [ ] definition contracted graph
  - [ ] source code for my implementation

## Main tasks

- [ ] finish chapter about symmetries and orbital chromatic polynomials
  - [ ] what definitions are necessary?
  - [ ] add references

## Side tasks

- [ ] simplify the chapter about symmetries

### Definitions

- [ ] distinguish between proper and improper colorings in the definitions

- [ ] define the V(G) syntax

### Basic chromatic polynomials

- [ ] comment the results of the chromatic polynomial table
  - what function was used to compute them?
  - why only selected included?
  - mention that some polys took too long to compute (for 48 edges took ten minutes, for 60 edges did not finish)

- [ ] add demonstrative figures to the proof for formula of chromatic polynomial of complete k-partite graph with partition size 2

### Independent sets

- [ ] compute how many arrangments of k independent sets exist on various solids (start with tetrahedron, cube etc.)
  - [ ] read about calculating number of graph colorings up to order of colours
    - [link](https://webspace.maths.qmul.ac.uk/p.j.cameron/csgnotes/countcols.pdf)

- [ ] calculate # of such colorings for C_4 and cube

### Misc

- [ ] what do operations on the Platonic solids do on the graphs?

- [ ] try to add list of Schlegel diagrams of the solid graphs as appendix
  - [link_to_figs](https://en.wikipedia.org/wiki/Archimedean_graph)