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

## 2025_03_24

- [x] write defn of fixation graph

- [ ] show how orbital chromatic polynomial is computed
  - [x] definition fixation graph

## 2025_03_25

- [ ] show how orbital chromatic polynomial is computed
  - [x] finish (almost) proof for the formula

## 2025_04_02

- [x] take into account supervisor suggestions

- [x] check the pseudocode for computing orbital chromatic polynomial
- [x] add source code for my sage implementation of the orbital chromatic polynomial algorithm

## 2025_04_03

- [x] change the orbchrompoly alg to also print the colorings?
  - I don't think that would work

- [x] find graph on which to visualize orbchrompoly
  - [ ] improve md printing to print polynomials nicer for desmos
    - remove the asterisk
    - put exponents into a curly brace
  - [x] use desmos to find out the numbers

- [x] test drawing graphs with hard coded layout in sage

- [x] octahedron 3 colors

## 2025_04_05

- [x] label edges and draw the ones behind with different color / style

- [x] draw edges in behind in dotted style
  - [x] if not work -> post issue on SageMath git

- [x] add octahedron example comparison of chrompoly and orbpoly using the generated plot

## 2025_04_08

- [x] compute dicts of evaluated chromatic and orbital chromatic polynomials for PLATONIC SOLIDS ONLY
  - best to have the polys for same solid right next to each other to see the difference nicely

## 2025_04_09

- [x] make table printing so I can define the order in which the solids appear in the table

- [x] let user enter how much spacing they want next to the latex key column 
  - best to make this compatible with md table printing as well (can just ignore the parameter)

- [x] add tables of evaluated chromatic polynomials compared with evaluated orbital chromatic polynomials
  - figure out name of this chapter (comparing evaluations of chromatic and orbital chromatic polynomials)

- [x] adapt all tables to the new ordering of the solids
  - at this occasion also default to latex printing in all the programs

- [x] comment the figure visualizing pascals triangle recursion on octahedron

- [x] write code that receives all computed n-colorings from SageMath and removes duplicates up to automorphisms

- [x] add preset colors based on their total amount to the plotting code

## 2025_04_10

- [x] make cube printing have dotted lines where necessary

- [x] implement pruning of colorings that are not in canonic form 
  - canonic form of coloring is (first occurences of colors as ints when going through coloring as list of ints must be in increasing order) 

- [x] write about how to calculate colorings using exactly n-colors from the tables showing at most n-colors

- [x] compute table with # of number of colorings using exactly n colors with respect to symmetries
  - write a program that does this by the method we used at the meeting with supervisor
  - describe how the method works

## 2025_04_12

- [x] add .yaml layout for icosahedron plotting 
  - maybe use ChatGPT to generate them

- [x] make the plotting work with svgs instead of pngs

## 2025_04_13

- [x] add documentation pdf file (from goodnotes) for the icosahedron .yaml

- [x] add .yaml for dodecahedron and tetrahedron plotting

- [x] implement coloring independent set size fingerprint
  - for n-coloring the fingerprint: 
    - has a list of size n where each position has size of the indep set (later we will want this sorted)
    - has a second list of size n where each position corresponds to the color value of that independent set
  - probably create a class for the fingerprint for better semantics

- [x] make colorings in the output sorted based on independent set size fingerprint

- [x] think how to sort the 3-colorings so the picture looks systematic
  - somehow you the automorphisms to transform the colorings to some standard form

## 2025_04_14

- [x] implement printing in rows based on fingerprint classes

- [x] implement pseudoalg from [sage notes](../Notes/sage_notes.md)

## 2025_04_15

- [x] write about counting equivalence classes of relabel relation

## 2025_04_16

- [x] define relabeling-automorphism relation

- [x] argue, why we cannot just simply multiply each partition with respect to rotation by n! where n is the number of colors 
  - (provide an example maybe on 4-colorings of cube, show two classes that have different amounts of representatives)
  - provide a mathematical bound on the number (it can be at least something and at most something)
    - bcs there can't be more than n! colorings corresponding to a single coloring

## 2025_04_17

- [x] add table with colorings where we consider relabelings as same thing but automorphisms are not considered

## 2025_04_18

- [x] show the lower and upper bound on the count of equivalence classes of the relabeling-automorphism relation

- [x] compute tables with intervals resulting from both types of bounds
  - then maybe also show a table which combines together to get the tightest bound possible

- [x] add example with particular 3-colorings of cube and show that we count some colorings multiple times
  - some colorings are just rotated - show example of colorings we counted as different but can be unified by rotation
  - some colorings are just relabeled - show example of colorings we counted as different even though that can be received by relabeling

## 2025_04_19

- [x] finish thesis overview

- [x] write first version of the conclusion of the thesis

- [x] debug why 4 colorings of cube consider the (2,2,2,2) colorings all as same
  - what permutation and relabeling causes their identification?

## 2025_04_20

- [x] compute numbers of equivalence classes using the improved algorithm

- [x] describe the algorithm for calculating the number of equivalence classes of the relabeling-automorphism relation

## 2025_04_22

- [x] use the improved function also in the `coloring_plots.py` code

## 2025_04_23

- [x] proofread what I wrote in the thesis

- [x] show figures with selected examples of equivalent classes that we calculated

- [ ] test if result will be printed faster if I use the alg. from thesis for relaut colorings printing instead of the old one (which is prly slower)

## 2025_04_27

- [x] try separating thousands in the tables of thesis

- [x] implement function to add small spaces `\,` to a number
- [x] update tables to use thousands separation

- [x] emphasize which colorings I am showing examples of in the table
- [x] update text about which examples I decided to show and update table caption

- [x] add size sequences under the octahedron figure

- [x] improve conclusion

## 2025_04_28

- [x] write abstract of the thesis

- [x] add keywords
  - look what keywords Cameron used in his similar theses

- [x] write dedication

- [x] rewrite introduction

## 2025_04_29

- [x] fix easy visual stuff in the thesis
  - [x] k in abstract math mode
  - [x] unify if mentioning names with initials or not
  - [x] remove some of the keywords
  - [x] dots in tables remove for Archimedean solids
  - [x] solid size vectors unified
  - [x] make vertices bigger (try with ChatGPT)
  - [x] finally to the icosahedron example
  - [x] polynomials flip 20,...1, to 1,...20 (ChatGPT + compare)

- [x] rewrite introduction to be more motivating and less describing the content
  - try to write another version and then compare, worst case we fall back to old version

## 2025_04_30

- [x] test the thesis for PDF/A compliance

- [x] test abstract generation

- [ ] try run the relaut equiv class program for specific colorings only with more time than just 60 seconds

- [ ] think about data structure for searching for the correct representant (could it be made faster)

- [ ] create a multiprocess version of the relabeling automorphism finding program (parallel version)

## Main tasks

- [ ] improve definition of coloring to include difference between proper and improper coloring

## Side tasks

### Improve visuals

- [ ] in the visualisation of Pascal's triangle formula for K_{k x 2} graphs, emphasize where the operation is done in the figure

- [ ] make some section headings shorter

### Improve definitions

- [ ] distinguish between proper and improper colorings in the definitions

### Misc

- [ ] rewrite python script to find representative colorings for single solid and n
  - try to rewrite in C++ (maybe with help of ChatGPT)