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