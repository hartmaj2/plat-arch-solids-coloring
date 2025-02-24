# Diary of work progress

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

- learned how to work with so called 'floating objects' in latex
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

- found out more about regexp in python
  - `search` vs `match`
    - search: matches even if the match is somewhere in between the string
    - match: matches only if the match is somewhere starting from the beginning of the string
    - (fullmatch: matches only if entire string is match) 
  
- regexp in general
  - `x{n}` - exactly n occurences of x

- python in general
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
  - fixed latex typing of `\chi'(G)`

- added note about The Four Color Theorem under the tables with calculated chromatic numbers

- automatized bibliography references using resources.bib file
  - need to add the following lines:
    - `\bibliographystyle{plain}`
    - `\bibliography{Resources/references}`

- computed some tractable chromatic polynomials (prly won't add to the thesis but I can consult this with supervisor)

- automatized list of tables printing 
  - use `\listoftables` with the `table` environment
  - each table must have `caption` attribute
  
- added bibliography and list of tables to table of contents using `\addcontentsline{toc}{chapter}{Bibliography}`

### 3035_02_24

- found out why calculation of chromial of octahedron in terms of complete graphs yields Pascal's triangle
  - see: [here](../Resources/Handwritten/octahedron_chrom_poly_pascal.pdf)

- 