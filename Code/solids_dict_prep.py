import json
import os

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"
INPUT_FOLDER_PATH = ROOT_FOLDER + "/JsonGraphs"

JSON_NAME_PROPERTY_KEY_NAME = "name"
JSON_VTCES_PROPERTY_KEY_NAME = "vertices" # inside the json file, each vertex is a tuple containing the coordinates but we just need the amount
JSON_EDGES_PROPERTY_KEY_NAME = "edges"

ARCHIMEDEAN_FOLDER_NAME = "Archimedean"
PLATONIC_FOLDER_NAME = "Platonic"

# retrieves data from json files necessary to create sage graphs
def get_name_and_edges(folder_name: str, solid_filename : str) -> tuple[str,list]:
    with open(f"{INPUT_FOLDER_PATH}/{folder_name}/{solid_filename}","r") as file:
        graph_data : dict = json.load(file)
        edges = graph_data[JSON_EDGES_PROPERTY_KEY_NAME]
        name = graph_data[JSON_NAME_PROPERTY_KEY_NAME]
        return name,[tuple(edge) for edge in edges] # convert: list of lists -> list of tuples

# processes all solids and return dictionary of their edge set (list of tuples)
def get_edges_dict(folder_name : str, solid_names : list[str]):
    edges_dict = {} # solid_name -> solids_edges
    for solid_filename in solid_names:
        solid_name, solid_edges = get_name_and_edges(folder_name,solid_filename)
        edges_dict[solid_name] = solid_edges
    return edges_dict

# returns dict of edges for platonic solids
def get_platonic_edges_dict():
    solid_names = os.listdir(INPUT_FOLDER_PATH + '/' + PLATONIC_FOLDER_NAME) # retrieves solid names in current folder
    return get_edges_dict(PLATONIC_FOLDER_NAME,solid_names)

# returns dict of edges for archimedean solids
def get_archimedean_edges_dict():
    solid_names = os.listdir(INPUT_FOLDER_PATH + '/' + ARCHIMEDEAN_FOLDER_NAME) # retrieves solid names in current folder
    return get_edges_dict(ARCHIMEDEAN_FOLDER_NAME,solid_names)

# retrieves the data for the given solid consisting of the name of the solid indices of vertices and the list of edges
def get_name_vtcs_edgs(folder_name: str, solid_filename : str) -> tuple[str,list,list]:
    with open(f"{INPUT_FOLDER_PATH}/{folder_name}/{solid_filename}","r") as file:
        graph_data : dict = json.load(file)
        vertices = graph_data[JSON_VTCES_PROPERTY_KEY_NAME]
        edges = graph_data[JSON_EDGES_PROPERTY_KEY_NAME]
        name = graph_data[JSON_NAME_PROPERTY_KEY_NAME]
        return name,[i for i in range(len(vertices))],[tuple(edge) for edge in edges] # convert1: list of coordinates -> list of indices, convert2: list of lists -> list of tuples 

# returns a dictionary indexed by solid name with elements being a dictionary indexed by property name ("vertices" or "edges")
def get_solid_data_dict(folder_name : str, solid_names : list[str]):
    solid_dict = {} # solid_name -> solids_edges
    for solid_filename in solid_names:
        solid_name, solid_vertices, solid_edges = get_name_vtcs_edgs(folder_name,solid_filename)
        solid_dict[solid_name] = { JSON_VTCES_PROPERTY_KEY_NAME : solid_vertices, JSON_EDGES_PROPERTY_KEY_NAME : solid_edges } # it is a dict of dicts
    return solid_dict

# returns solid dict for platonic solids
def get_platonic_solid_dict():
    solid_names = os.listdir(INPUT_FOLDER_PATH + '/' + PLATONIC_FOLDER_NAME) # retrieves solid names in current folder
    return get_solid_data_dict(PLATONIC_FOLDER_NAME,solid_names)

# returns solid dict for archimedean solids
def get_archimedean_solid_dict():
    solid_names = os.listdir(INPUT_FOLDER_PATH + '/' + ARCHIMEDEAN_FOLDER_NAME) # retrieves solid names in current folder
    return get_solid_data_dict(ARCHIMEDEAN_FOLDER_NAME,solid_names)