# Ipe notes

## Creating a tetrahedral graph

objective: create a tetrahedral graph with one center node and all the other nodes equaly spaced around it
solution steps:
1. set the `origin` of angular snap axis using `F1-key` (or use `org` on mac toolbar)
2. snap the origin to grid using `snap to grid`
3. set the `snap angle` to 30 degrees
4. create a circle with center at the origin using `circles (by center and radius)`
5. use both `angular snap` and `snap to boundary` to place the vertices at 120 degree intervals around the circle
6. hide the angular axis using `axes` button on mac touch toolbar

## General 

- one face should fit roughly 28 pts (~10 mm) on the grid

## Edge coloring

- use pen size 0.6

## Angular snap

- set origin using `org` and then the direction using `dir` on mac toolbar
  - tip: the direction set by `dir` is kept even if we choose a new point as origin using `org`