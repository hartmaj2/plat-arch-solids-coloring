#!/usr/local/bin/sage -python

# Draws all colorings using up to max_clrs colors and merges the drawings into a single collage
# The colorings are generated iteratively as all 0 colorings, 1 colorings, ... , max_clrs colorings

# IMPORTANT: the i-colorings can only use i colors and cannot use the rest of (max_clrs - i) colors so we get fewer
# results than what the chromatic polynomial tells us for that many colors

# IMPORTANT2: make sure that in the Plots directory is nothing else than the {collage_name}.png file

# IMPORTS

import solids_prep.solids_dict_prep as sdp
import os
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
solid_name = "cube"
edges = sdp.get_all_solids_dict()[solid_name][sdp.JSON_EDGES]
g = Graph(edges)

# removes the leftover image from last round
def clean_folder():
    if f"{collage_name}.png" in os.listdir(output_path):
        os.remove(os.path.join(output_path,f"{collage_name}.png"))

# creates separate images for all the colorings
def create_images(graph, max_clrs):
    clean_folder()
    for num_clrs in range(max_clrs+1):
        clrings = all_graph_colorings(graph,num_clrs,hex_colors=True)
        for i,c in enumerate(clrings):
            graph.plot(vertex_colors=c).save(f"{output_path}{filename_base}_{num_clrs}clrs_{i}.png")

# merges the images of the colorings in the directory into a single square-like collage
def merge_images():
    filenames = os.listdir(output_path)
    images = [Image.open(os.path.join(output_path, img)) for img in sorted(filenames)]
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
    
    for filename in filenames:
        os.remove(os.path.join(output_path, filename))

    collage.save(f"{output_path}{collage_name}.png")


print("generating coloring images...")
create_images(g,max_clrs)
print("merging images...")
merge_images()