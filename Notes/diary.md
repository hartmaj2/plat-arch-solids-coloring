# Diary of work progress

- UAQ := unanswered question
- PY := python trick/useful concept
- LTX := latex trick/useful concept
- VSC := vscode trick

## December

### 2024_12_12

- fixed bug with LaTeX Charles university template
  - use pdfLaTeX instead -> the problem was to stop using ps2pdf package
  - in order to do so, I needed to convert logo.eps to logo.pdf using epstopdf command

### 2024_12_14

- copied important sections of Graph Coloring Problems Book from National Library
- realized that coloring G with k-colors is the same as finding a homomorphism from G to K_k graph

### 2024_12_15

- found a webpage for visualizing the polyhedra: [link](https://polyhedra.tessera.li/)
  - it also has nice definitions for the polyhedra
  - also, I can use the .json objects to get the graph representations for free
- found out how are archimedean solids defined
  - based on operation done on platonic solids
- edited wikipedia page [link](https://en.wikipedia.org/wiki/Expansion_(geometry))

- emailed C++ tutor about graph editor program

- written first draft of the Introduction chapter of the thesis

### 2024_12_16

- drawn pictures of how the operation on Platonic solids behave
  - noted how these operations change the vertex configuration

### 2024_12_22

- fix errors in overleaf
- begin working on Sage

## February

### 2025_02_13

- read what I wrote in thesis so far
  - fixed typos

- cleaned code for calculating vtx/edge chromatic numbers of Platonic and Archimedean solids
  - [file link](Code/json_to_sage.py)
  - added comments
  - removed unused pieces of code
  - added named constants
  - abstracted away from concrete output stream
    - wrote my first answer to StackOverflow [link](https://stackoverflow.com/questions/4512733/python-equivalent-of-java-outputstream/)

- got a tip to read later about writing papers in english
  - [link](https://kam.mff.cuni.cz/~matousek/angli.pdf)
  - key takeaways:
    - include more pictures
    - don't waste too much time on stylistics; content is more important
    - don't use long sentences
    - don't use future tense too much

- learned how to convert images from .svg to .pdf using incscape
  - `inkscape ./path/to/picture.svg --export-filename="./path/to/picture.pdf"`

- LTX: learned how to work with so called 'floating objects' in latex
  - you an fix their position as it is in the source file by adding `[H]` option
  - for this you need to include float package: `\usepackage{float}`

- found out that expansion can be also viewed as cantellation
  - the result is the same 
  - difference: 
    - cantellation 
      - first cuts off edges (bevels/chamfers them)
      - truncates the newly obtained vertices to create regular d-gons where d is the degree of the 
  - there exists also [chamfering](https://en.wikipedia.org/wiki/Chamfer_(geometry))
    - edge truncation
    - similar to cantellation but after beveling/chamfering the edges, the


### 2025_02_14

- PY: found out more about regexp in python
  - `search` vs `match`
    - search: matches even if the match is somewhere in between the string
    - match: matches only if the match is somewhere starting from the beginning of the string
    - (fullmatch: matches only if entire string is match) 
  
- regexp in general
  - `x{n}` - exactly n occurences of x

- PY: python in general
  - `r"some_string\n"` interprets the string without considering \ as escape character (r as for raw string)

### 2025_02_15

- wrote definition of graph and graph coloring in my own words without checking the literature

- included the amsmath package
- learned how to define a new environment using \newtheorem{name_of_env}{text_at_beginning_of_env}

- read definitions of graphs and coloring
  - Handbook of Graph Theory - Gross, Yellen, Zhang
  - Graph Theory - Reinhard Diestel

- read Ipe documentation and learned the basics of working in it
  - problem: how to draw graphs so that nodes keep attached to the edges
    - when node is moved, the edge should keep being attached and not bend itself

- tried working with Tikz
  - programmatic way of defining a graph
  - it is super precise and the result looks great but has major disadvantage: slow to create the graph

- found out why the draggin did not work in Ipe
  - edges have to be finished with a right click 
  - (if there's a left click before the right click, it creates a midpoint of the edge that is anchored to the position where was clicked)

- organized all notes into a notes folder
- added a ipe_notes file for notes about working with ipe

- created a figure with example vertex coloring on tetrahedral graph in Ipe

### 2025_02_16

- made octahedral and cubical graphs in Ipe 
  - octahedral - vertex coloring
  - cubical - edge coloring

- made exercise from Ipe manual on snapping modes

- generalized the definition of coloring and introduced a family of colorings
  - this generalized version can be used to derive the concrete colorings from it

- learned that .stl files can be used to represent 3D objects like polyhedra
  - stl as stereolithography
  - they can be rendered in browser (wikipedia does that)

### 2025_02_17

- found out how to set table column alignment in markdown
- found out how to make latex tables

- created module to create latex table from computed chromatic numbers
- added the latex table to bachelor thesis

- had meeting with my supervisor

### 2025_02_19

- thought about problems in: https://kam.mff.cuni.cz/~fiala/slides/Polya.pdf up to page 19
  - resource for this is here: https://www.jstor.org/stable/2688047
- found this useful resources (similar problem to what I will write about): https://www.jstor.org/stable/10.4169/mathhorizons.21.4.14
  - this one has nice example of practical usefulness of Polya's theorem: https://www.jstor.org/stable/2690407

### 2025_02_20

- defined a `highlight` environment using conditional variable `useHighlights` to highlight new text for the supervisor
- found out it is effective to click on rendered file in overleaf on the part of the text where I want to focus in my code editor on the corresponding part

- wrote a definition of `k-coloring` and used it in the subsequent definitions
- wrote a definition of what it means for two colorings to be `different`
- wrote a definition of `chromatic polynomial` and added example

- added sample code that displays a planar drawing of a graph and saves it to a file

- tried to find out what is the explicit formula for `chromatic polynomial` of octahedron
  - harder than it seems
  - found out number of 3 and 4 colorings and tested using SageMath

### 2025_02_21

- built stronger intuition about why the combinatorial graph theory proof that there are only 5 platonic solids holds
  - did an overview (big idea) of what facts are used and what are the key observations to make

- found out that Tutte's polynome is a generalization of chromatic polynomial: https://en.wikipedia.org/wiki/Tutte_polynomial#:~:text=analysing%20these%20quantities.-,Chromatic%20polynomial,-%5Bedit%5D

- calculated chromatic polynomial of octahedron by hand to build intuition
  - graph here: https://www.desmos.com/calculator/r9nqeute7w
  - the terms in front of K_n polys come from Pascal's triangle

- found it is possible to calculate chrom polys using SageMath
  - following function: https://github.com/sagemath/sage/blob/develop/src/sage/graphs/chrompoly.pyx

### 2025_02_22

- added references to SageMath used functions

- fixed wordings based on recommendation of supervisor
  - "Concrete colorings" -> "The general concept of coloring"
  - "General coloring" -> "Common properties of colorings"`
  - LTX: fixed latex typing of `\chi'(G)`

- added note about The Four Color Theorem under the tables with calculated chromatic numbers

- LTX: automatized bibliography references using resources.bib file
  - need to add the following lines:
    - `\bibliographystyle{plain}`
    - `\bibliography{Resources/references}`

- computed some tractable chromatic polynomials (prly won't add to the thesis but I can consult this with supervisor)

- LTX: automatized list of tables printing 
  - use `\listoftables` with the `table` environment
  - each table must have `caption` attribute
  
- LTX: added bibliography and list of tables to table of contents using `\addcontentsline{toc}{chapter}{Bibliography}`

### 2025_02_24

- found out why calculation of chromial of octahedron in terms of complete graphs yields Pascal's triangle
  - see: [here](../Resources/Handwritten/octahedron_chrom_poly_pascal.pdf)

### 2025_02_25

- finished revising Vizing's proof for chromatic index upper bound
  - nice video: [here](https://www.youtube.com/watch?v=OZWZpQmGp0g&ab_channel=TomS)

- proved why the construction of Vizing class two graphs from Platonic solids works:
  - see construction: [here](https://en.wikipedia.org/wiki/Vizing%27s_theorem#:~:text=al.%20(1988).-,Planar%20graphs,-%5Bedit%5D)
  - see proof: [here](../Resources/Handwritten/class_two_from_plat.pdf)

- improved vtx degree counting program by including a sanity check

- improved md and latex printers to be able to print for each solid data with variable amount of columns given the list of names of the columns and corresponding dictionary with the right amount of data entries per each element of the dictionary

- added table with amount of vertices, edges, faces and degree at all vertices into the thesis
- added a short text about Vizing theorem and Vizing class of plat and arch solids

### 2025_02_26

- wrote definition of drawing of a graph, plane graph and a planar graph

### 2025_02_27

- edited definitions for colorings to be able to color faces as well
- added a definition of face coloring including a figure with an example on a octahedral graph

## March

### 2025_03_01

- restructured chapters into more meaningful ordering

- added definitions of rainbow coloring and magic labeling
  - added references

- started working on chapter about conversions between the colorings

### 2025_03_02

- fixed point 4 in definition of graph drawing

- added visualizations of total coloring

- added definition of face coloring with visualisation

- created conversion from a graph to its line graph
  - edge coloring is faster using the conversion
  - tested, if even faster when using sage line_graph conversion (running time seems to be the same as for my conversion)
- created conversion from a graph to total graph
  - computed total chromatic numbers using this conversion

### 2025_03_03

- improved latex printing function for variable column amount tables

- tried to calculate total chromatic number using distance graph conversion
  - unfortunately, no function for distance graph seems to exist in Sage

### 2025_03_04

- converted bachelor thesis format to the correct standard (I had the old one before)
  - the new standard has advantages:
    - links to figures & tables jump to the right places (so the figure is actually visible)
    - the metadata is propagated to all places where it should go without having to repeat yourself
    - title page is separate from thesis.tex (the preamble + just the ordering of the documents containing the actual content)

### 2025_03_05

- read further from Polya.pdf from my supervisor
  - built a bit more intuition 
    - why transformations on square form a group
    - why transformation that preserve a certain coloring form a subgroup 
    - why the set of all colorings that I can get by applying transformation to some coloring form an equivalence class
  - revised notation
    - fixpoint - for a transformation it is the set of all elements that are immune to the transformation 
    - stabilizer - for some element it is the set of all transformation that leave him untouched
    - orbit - equivalence class of a under the relation defined by "all the elements I can get to from a by applying transformations on it"
- unanswered questions: 
  - (a) why every transformation in G can be obtained as a left coset of some rotation with a subgroup defined as the transformations preserving some coloring?
  - (b) why -||- as a right coset of one rotation and all the subgroups defined by transformations perserving the colorings in the "orbit"

### 2025_03_06

- discovered answer to the question (a) above:
  - (a) this comes from the way how bijection between left cosets (using their representatives) and elements of the orbit is defined
    - this bijection is defined as mapping from gH_a -> g(a) (maps the representant of the coset to the element/coloring to which the representants transformation takes us)
    - because that mapping is a valid bijection, each transformation that takes me to a different coloring (inside of the same orbit) must be representant of a different coset

- read chapter about Lagrange's theorem and Burnside's lemma in [algebra 1 notes](https://www.karlin.mff.cuni.cz/~zemlicka/24-25/Algebra_1_translation.pdf)
  - wrote a summary about what are key arguments of the proof of Burnside's lemma
  - thought about where exactly is Lagrange's theorem used (in the part where we show that # of cosets of a stabilizer of c is same as the # of orbits of c to get equation: |stab(c)| * |orb(c)| = |G|)
  - where in the proof do we need counting two ways (not necessary if we don't need to express the amount of orbits using fixpoints)

- unanswered questions:
  - what characterizes the permutations that correspond to reflection or a rotation?

### 2025_03_08

- tried to find out some pattern in how chromatic poly of cube can be expressed as chromatic poly of trees using the recursive rool (contracting or removing an edge)
  - found out, that contracting an edge e can remove multiple other edges; removes 1 + (# of tricycles that e lies on) edges
  - the point above holds because we use the fact that parallel edges can be removed

- analyzed what defines a rotation
  - how can I find out all possible rotations?
  - rotation:
    - must have an axis x
    - x must go through centroid of the solid
    - x must go through centre of vertex/edge/face ?

- tried to figure out what is the difference between reflection and rotation
  - axis of rotation seems to always be an object with 2 less dimensions than the object we're rotating
  - axis of reflection -||- 1 less dimension -||-
  - what a reflection does in n-dim space can be done using some rotation of the object when embedded into (n+1)-dim space
  - unanswered questions:
    - what is the general difference between rotation and reflection?
      - what property of the solid is not preserved when reflecting?
      - what properties are preserved when only rotating?
    - why rotations and reflections of a graph correspond to automorphisms?

- checked that automorphisms w/ composition indeed form a group

### 2025_03_09

- found a constructive way to count automorphisms
  - 1. compute how many ways the first vertex can be mapped
    - each such way must result in a different automorphism
  - 2. then compute how many ways the neighbors can be mapped
    - this might already be the last step since when the neighbors are mapped, the rest might follow from the constraints given on them by the edges between them
    - UAQ: if they have no edges between them, is it possible to map them arbitrarily?

  - IMPORTANT: in step (2) if I want to consider rotations only
    - rotations are characterized by the fact, that they preserve orientations of the cycles
    - so the after on neighbor is picked the second must already follow from the orientation of the cycle in the original labeling

- found two examples of colorings of cube in supervisors Polya.pdf that seem to belong to the same orbit
  - probably not in the same orbit if considering only rotations and not reflections

- UAQ: why supervisor chose to exclude reflections (are they not automorphisms as well?)

- understood how size of fixpoint of automorphism can be calculated using the number of cycles of the automorphism

- calculated that for 2 colors, the amount of orbits when considering reflections also is 22 instead of 23
  - that agrees with the fact, that I found two cube configurations from supervisors slides, that can be obtained from one another by performing a reflection

- made calculation of orbits by Burnside's lemma for 48 automorphisms in Desmos
  - [link](https://www.desmos.com/calculator/mmruacwjl6)

- experimented with conda but realized I don't need it
  - removed both conda and miniforge

- installed sympy simply using pip

- calculated the expansion of polya polynomial for transformations of cube for 2 colors
  - [link](../Code/polya_cube.py)

### 2025_03_10

- thought about # of automorphism of Platonic solids, got the following results:
  - tetrahedron - 24 (4!)
  - cube - 48 (8*3*2)
  - octahedron - 48 (6*4*2)
  - dodecahedron - 120 (20*3*2)
  - icosahedron - 120 (12*5*2)

- tested that the counts above were correct using Sage
  - [link to code used here](../Code/automorphisms.py)

- had a meeting with supervisor
  - [link to notes](../Meetings/meet_25_03_10.md)

- PY: found a nice operator to merge dictionaries in python 
  - `merged_dict = dict1 | dict2`

- simplified code of solids prep program
  - removed specific functions for getting edges only
  - added function to get merged dicts for combined plat and arch solids
  - used this to prepare edges set for `snub cube` for its chrom poly to be computed on faculty HPC

### 2025_03_11

- proofread chapter named `Colorings and symmetries`

- revised Burnside's lemma and prepared plan of attack on counting orbits of proper colorings

### 2025_03_12

- thought about how to compute fixpoint sizes for each transformation when counting only proper colorings
  - got following observations:
    - if transformation has cycle s.t. any two vertices on the cycle are connected -> fixpoint size = 0
    - otherwise, we contract all vertices on cycle into one vertex (this simulates that they must have same color)
    - then we just calculate # of colorings irrespective of symmetries of the resulting graph
      - any proper coloring of cycles will be a fixpoint

- borrowed book `Graph Coloring Problems`

- got idea: instead of computing chromatic polynomial of `snub cube`
  - try to calculate # of proper n colorings up to the # of vertices and then interpolate a polynomial
  - first I can experiment if the same procedure would work on `rhombicuboctahedron`

- mentioned Brook's theorem in the thesis and added reference to magic labeling definitions

- PY: found a useful python function `enumerate(iterable)` that returns a pair `index,elem` where elem is element of the iterable and index its index
  - added sage to path analysis by adding this line to settings.json: `"python.analysis.extraPaths": ["/private/var/tmp/sage-10.5-current/local/var/lib/sage/venv-python3.12.5/lib/python3.12/site-packages"],`

- created a program that generates graph coloring plots and merges them into a single file
  - this will be used later for checking that my calculations make sense


### 2025_03_13

- calculated chromatic polynomial of rhombicuboctahedron using HPC cluster
  - was 2x faster than on my computer

- found out that there exists a polynomial that counts the number of colorings using x colors up to symmetries -> the `orbital chromatic polynomial`
  - 
  - implemented a function that computes it
  - used it to compute the orbital chromatic polynomial for all the graphs for which calculating ordinary chromatic polynomial was fast

### 2025_03_15

- latex table printing
  - generalized my function for latex printing so I don't need a special function to print the polynomials
  - improved the look of latex tables to recommended format

- added vertex configurations to the general graph props table

- better visualisations
  - created a visualisation of the snub operation and added it to the thesis
  - unified the look of all the visualisations with Inkscape

- added text about how chromatic polynomial can be computed using a recursive formula
  - referenced the book "Chromatic Graph Theory" by Chartrand and Zhang

- removed my definition of a graph drawing and referenced the one from "Invitation to Discrete Mathematics" by Matousek and Nesetril 

- improved definitions:
  - added name of the defined term next to the definition heading
  - used `\emph` instead of `\textbf`

- updated `README.md`

### 2025_03_16

- PY: learned that inside f-string, escape `{` using `{{`

- LTX: one can set spacing between rows by `\renewcommand{\arraystretch}{<ratio>}`

- added table of selected orbital chromatic polynomials to the thesis
  - also improved the chromatic poly printing code
  - also added choice to set the row spacing ratio inside latex table printing function

- LTX: used regexp to replace all `\begin{definition}` and `\end{definition}` with `\begin{defn}` or `\end{defn}` correspondingly
  - matching regexp: `\\([a-z]{3,5})\{definition\}`
  - replacement regexp: `\$1{defn}`

### 2025_03_17

- took into account recommendations from supervisor for better formulations in the thesis text

- LTX: labeled my lemmas in the formal proof of the formula for the chromatic polynomial of the complete k-partite graph. 
  - `\label{lemma:name-of-lemma}` should be put right bellow the start of the lemma environment

- also finished the formal proof of formula for chromatic polynomial of complete k-partite graph with partition size 2

- had meeting with my supervisor

- improved the look of visualisations of the colorings:
  - removed black borders around vertices
  - made lines of octahedral coloring to have same thickness as the ones for cubical for unified look

- LTX: fixed wrong hyperrefs for equations (for some reason using a tag with label messes with the referencing)

### 2025_03_18

- decided to scratch most of old text from the Symmetries chapter

- wrote a definition of automorphism
  - IMPORTANT: automorphism must be a **bijection**
  - I am quite sure the it is enough to say it is a bijection $b: V \rightarrow V$ s.t. $\{u,v\} \in E$ implies $\{b(u),b(v)\} \in E$
    - then the other implication follows from the fact that it is a bijection and when some non-edge would be mapped to an edge, then it would be impossible to map m other edges to m-1 edges because one edge was mapped to by this non-edge, and a pair of vertices cannot be mapped onto by two different pairs of vertices
  - Kapitolky z DM have defn at page 117 at the bottom

- wrote a definition of a group and checked it with definition from Hladik

- thought about what the transitivity equivalence relation will mean to me in our scenario of colorings

### 2025_03_19

- wrote definitions of transitivity relation, orbit and stabilizer

- in the evening managed to stab a knife into my palm (don't ask how) and then had to go to emergency and got some stitches so didn't do much more...

### 2025_03_20 

- wrote the formula for counting orbits using stabilizers, added notation for the set of all orbits

- added tables with sizes of automorphism groups of graphs of Platonic and Archimedean solids

### 2025_03_22

- bachelor thesis text:
  - defined fixpoints
  - showed how two way counting used in Burnside's lemma
  - added and used definition of set of colorings with up to n colors to avoid working with infinite sets
  - added definition of orbital chromatic polynomial and a reference to Cameron's work

### 2025_03_23

- read a paper about a method of calculating the chromatic polynomial of sparse graphs
  - [link](https://www.researchgate.net/profile/Ramon-Figueroa-Centeno/publication/269396607_An_improved_Algorithm_for_the_Chromatic_Polynomial/links/54892a930cf2ef344790ac53/An-improved-Algorithm-for-the-Chromatic-Polynomial.pdf)
  - unfortunately, this is not the paper that SageMath references as I realized later

- wrote an issue on SageMath to provide me with the paper they reference
  - used ChatGPT "Deep Research" function to look for the paper in the meantime
  - found a paper that references the work as well, supposedly it should be from University of Waterloo
  - sent a mail to University of Waterloo to ask if they can provide me access to the paper

- expanded the text about computing chromatic polynomials using the other formula and moved the table with selected chromatic polynomials

- improved citation of SageMath to follow their official guidelines of how to cite it

### 2025_03_24

- wrote definitions needed to prove the formula for computing the orbital chromatic polynomial using the usual chromatic polynomial
  - fixation graph
  - independent set

- started writing the proof for the computation of orbital chromatic polynomial
  - one-to-one correspondence between colorings of original graph fixed by a permutation and the colorings of the fixation graph for the given permutation

### 2025_03_25

- finished writing the proof
  - realized that the proof to be valid should indeed define a bijection
    - show injectivity, surjectivity and that it is a valid function

### 2025_03_26

- reviewed the proof again and simplified it
  - added a todo for the missing argument:
    - so far we know only that for any natural number, the polys have equal values but we need to show that they are indeed the same polynomials (but we don't need that in practice for the computations)

- started writing pseudocode for the orbital chromatic polynomial algorithm

### 2025_04_02

- want a reusable simple way to time my algorithms for bachelor thesis

- create timing module containing function decorators that will time my functions
  - PY: for decorators - use `*args` to be able to pass arguments even when I don't know how many there will be
    - `*args` - arguments
    - `**kwargs` - keyworded arguments
    - when definning function:
      - can provide `default arguments` to params but must follow the `non-default` parameters
      - the caller must provide arguments for all the `non-default` params
    - when calling function:
      - i can add keyword to an argument
      - `keyword` arguments must follow `non-keyword` arguments

- implement some of the suggestions provided by my supervisor

- implemented a module for benchmarking runtime of functions
  - pass a function with arguments
  - receive original result and the running time as well

- used the timing function mentioned above together with my table printing functions to nicely compare run times of the functions for each solid
  - added a transform option to md table printing (can apply the transform on data before outputting it into the column)

### 2025_04_03

- wrote functions to print polynomials that are ready to paste into desmos

- visualized polynomials in Desmos to see which have bearable number of colorings
  - [link](https://www.desmos.com/calculator/mci9dnx1lk)

- rewrote plotting program to not use actual files but temporary files for coloring pics before merge
  - advantage: don't have to care about name collisions and removing the files manually

- found out that platonic solid graphs have presets with the layout being already fixed
  - unfortunately it seems like only the cube layout will be geometrically nice

### 2025_04_05

- PY: found out how to type functions in
  - `from collections.abc import Callable`
  - `abc` stands for Abstract Base Class
  - the function is then annotated as `Callable[[arg1,arg2,...,argN],ret]`

- switched to yaml from json for config files for the graph plotting configs
  - yaml offers:
    - comments
    - newlines matter (don't have to separate entries by commas)
    - anchors and aliases for repeated values

- found that there exists a command to check for MacOS updates through command line
  - [link](https://ss64.com/mac/softwareupdate.html)
  - the reason I got to it is this: [link](https://doc.sagemath.org/html/en/reference/spkg/_prereq.html)
    - bcs I want to have newest version of SageMath
    - for that I would like to try to install SageMath from source

- found out that the reason why `edge_styles` did not work for me was really bcs I had an old version of sage namely `SageMath 10.5` but that option was included in `SageMath 10.6`
  - [link](https://github.com/sagemath/sage/pull/38823)

- installed `SageMath 10.6` using the binary build as described [here](https://doc.sagemath.org/html/en/installation/index.html)
  - VSC: change python analisys setting to new version of sage: `"python.analysis.extraPaths": ["/private/var/tmp/sage-10.6-current/local/var/lib/sage/venv-python3.12.5/lib/python3.12/site-packages"],`

- added the generated octahedron 3-colorings figure to the thesis and added a commentary

### 2025_04_08

- implemented function to evaluate polynomial function of platonci solids at points 2 ... k