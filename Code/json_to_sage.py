#!/usr/local/bin/sage -python

import sage.all
import json

def get_solid_edges(solid_name : str):
    with open(f"Code/JsonGraphs/Platonic/{solid_name}.json","r") as file:
        graph_data = json.load(file)
        edges = graph_data["edges"]
        return [tuple(edge) for edge in edges]

solids = ["tetrahedron","cube","octahedron","dodecahedron","icosahedron"]
with open(f"Code/sage_graphs.txt","w") as output_file:
    for solid_name in solids:
        command_str = f"G = Graph({get_solid_edges(solid_name)}); G.plot(layout='planar').show(); chromatic_number(G)"
        output_file.write(f"{solid_name}: {command_str}\n")
        print("hello")
        