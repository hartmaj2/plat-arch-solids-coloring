import yaml

ROOT_FOLDER = "Code/JsonGraphs/Layouts/"

EDGES = "edges"
VERTICES = "vertices" # inside the json file, each vertex is a tuple containing the coordinates but we just need the amount
POSITIONS = "pos"
EDGE_STYLES = "edge_styles"
EDGE_COLORS = "edge_clrs"

EXTENSION = ".yaml"

NOT_DICT_ERROR_MESSAGE = "Expected a dictionary but got something else"

# load yaml prop dict
def get_solid_data_dict(filename : str) -> dict:
    with open(f"{ROOT_FOLDER}{filename}{EXTENSION}") as file:
        data = yaml.safe_load(file)
        if not isinstance(data,dict): # yaml parsed object does not have to be a dict necessarily
            raise TypeError(NOT_DICT_ERROR_MESSAGE)
        return data

# loads the solid config data from the yaml file
# the dict has vtx index as key and the tuple representing (x,y) position as value
def get_pos_dict(filename : str) -> dict:
    pos = {}
    data = get_solid_data_dict(filename)
    vtces = data[VERTICES]
    positions = data[POSITIONS]
    for i in range(len(vtces)):
        pos[vtces[i]] = positions[i]
    return pos

# prepare a dict containing a dict of neighbors and edge labels for each vertex
# the edges are labeled from 0,...,m in the order as they are defined in the YAML config document
def get_labeled_neighbor_dict(filename : str) -> dict[int,dict]:
    data = get_solid_data_dict(filename)
    neighs = {}
    for vtx in data[VERTICES]:
        neighs[vtx] = {}
    for i,edge in enumerate(data[EDGES]):
        u,v = edge[0],edge[1]
        neighs[u][v] = i
    return neighs

# return a dictionary where key is color string and value is a list of edges of that color
# color is a string in format '#FFFFFF'
# edges are triples (vtx1,vtx2,edge_label)
def get_labeled_edge_clrs(filename : str) -> dict[str,list]:
    data = get_solid_data_dict(filename)
    edges = data[EDGES]
    colors = {}
    for i,color in enumerate(data[EDGE_COLORS]):
        if color not in colors:
            colors[color] = []
        colors[color].append((edges[i][0],edges[i][1],i))
    return colors

# return a dictionary where for each edge with label i, it contains the corresponding style string ('solid','dotted',...)
def get_labeled_edge_styles(filename : str) -> dict[int,str]:
    data = get_solid_data_dict(filename)
    styles = {}
    for i,style in enumerate(data[EDGE_STYLES]):
        styles[i] = style
    return styles