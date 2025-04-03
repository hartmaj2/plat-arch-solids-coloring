#!/usr/local/bin/sage -python

# Draws all colorings using up to max_clrs colors and merges the drawings into a single collage
# The colorings are generated iteratively as all 0 colorings, 1 colorings, ... , max_clrs colorings

# IMPORTANT: the i-colorings can only use i colors and cannot use the rest of (max_clrs - i) colors so we get fewer
# results than what the chromatic polynomial tells us for that many colors

# IMPORTS

import solids_prep.solids_dict_prep as sdp
import solids_prep.solids_layout_prep as slp

import tempfile
from PIL import Image
import math

from sage.all import Graph
from sage.all import *
from sage.graphs.graph_coloring import all_graph_colorings

# OUTPUT SETTING
output_path = "Code/Plots/"
filename_base = "res"
collage_name = "collage"

# INPUT SETTINGS
max_clrs = 3
solid_name = "octahedron"
edges = sdp.get_all_solids_dict()[solid_name][sdp.JSON_EDGES]
g = Graph(edges)
positions = slp.get_pos_dict(solid_name)

# creates separate images for all the colorings
def create_images(graph : Graph, max_clrs : int) -> list[Image.Image]:
    images = []

    for num_clrs in range(max_clrs+1):
        clrings = all_graph_colorings(graph,num_clrs,hex_colors=True)

        for c in clrings:
            graphic = graph.plot(vertex_colors=c,vertex_labels=True,pos=positions,edge_labels=True)
            
            # store each image in temporary file and then create corresponding PIL image
            with tempfile.NamedTemporaryFile(suffix=".png",delete=True) as tmp:
                graphic.save(tmp.name)
                img_file = Image.open(tmp.name)
                images.append(img_file.copy())
                img_file.close()

    return images

# merges the images of the colorings in the directory into a single square-like collage
def merge_images(images : list[Image.Image]):
    print(f"merging {len(images)} images")

    imgs_per_row = math.ceil(math.sqrt(len(images)))
    image_width = images[0].size[0]
    img_padding_size = 100

    collage_width = image_width * imgs_per_row + img_padding_size * (imgs_per_row - 1)
    collage = Image.new("RGB",(collage_width,collage_width),(255,255,255))

    for i,img in enumerate(images):
        col = (i % imgs_per_row)
        x = col * (image_width + img_padding_size)
        row = (i // imgs_per_row)
        y = row * (image_width + img_padding_size)
        collage.paste(img,(x,y))

    collage.save(f"{output_path}{collage_name}.png")


print("generating coloring images...")
images = create_images(g,max_clrs)
print("merging images...")
merge_images(images)