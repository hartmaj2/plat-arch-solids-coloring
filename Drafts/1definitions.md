# Definitions

## Polyhedra

### Notation

- Schläfli symbol [link](https://en.wikipedia.org/wiki/Schl%C3%A4fli_symbol)
  - !only for regular polyhedra (Platonic)
  - {p,q}:
    - p - edges around each face
    - q - degree of each vertex
  - the dual has Schlafli {q,p}
- vertex configuration [link](https://en.wikipedia.org/wiki/Vertex_configuration)

### General

- uniform 
  - all faces regular polygons ( TODO: how does this translate to graphs?)
  - vertex transitive 
    - each vertex incident with same set of regular polygons
    - OR in other words: hanging the polyhedron on a string from any vertex will result in same situation (vertices are indistinguishable)

- regular
  - all faces are congruent to the same regular polygon

- semi-regular 
    - all faces are congruent to a regular polygon but these polygons can be different
    - EX: archimedean solids, prisms, antiprisms

### Platonic solid

- polyhedron
- ! convex
- all faces are congruent to the same regular polygon <=> each vertex configuration has only one type of integer
- ! all vertices must be incident with same amount of the polygons <=> all vertices have the same vertex sequences

- vertex sequence
  - enumerates the counts of sides that the polygons around each vertex have

### Archimedean solid 

- constructed from archimedean solids by operations: (TODO: how the operations translate to the graphs)
  - **truncation** [link](https://en.wikipedia.org/wiki/Truncation_(geometry))
    - cut off each vertex while:
      - creating new faces which are all regular polygons
      - duplicating amount of vertices of the original faces
  - **rectification** (truncation in the limiting case i.e. maximal possible) [link](https://en.wikipedia.org/wiki/Rectification_(geometry))
    - cut off each vertex while:
      - creating new faces which are all regular polygons
      - keeping the amount of vertices of the original faces the same as before (new vertices are midpoints of edges of old faces)
  - **expansion** [link](https://en.wikipedia.org/wiki/Expansion_(geometry))
    - a.k.a. cantellation
  - **snub** [link](https://en.wikipedia.org/wiki/Snub_(geometry))
    - expand and cut the squares made by the expansion into two triangles
    - then twist original faces in a chosen direction