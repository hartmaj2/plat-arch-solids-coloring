import json
import os

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"
INPUT_FOLDER_PATH = ROOT_FOLDER + "/JsonGraphs"

JSON_NAME_PROPERTY_KEY_NAME = "name"
JSON_EDGES_PROPERTY_KEY_NAME = "edges"

ARCHIMEDEAN_FOLDER_NAME = "Archimedean"
PLATONIC_FOLDER_NAME = "Platonic"

# retrieves data from json files necessary to create sage graphs
def get_solid_data(folder_name: str, solid_filename : str) -> tuple[str,list]:
    with open(f"{INPUT_FOLDER_PATH}/{folder_name}/{solid_filename}","r") as file:
        graph_data : dict = json.load(file)
        edges = graph_data[JSON_EDGES_PROPERTY_KEY_NAME]
        name = graph_data[JSON_NAME_PROPERTY_KEY_NAME]
        return name,[tuple(edge) for edge in edges] # convert: list of lists -> list of tuples

# processes all solids and return dictionary of their edge set (list of tuples)
def get_edges_dict(folder_name : str, solid_names : list[str]):
    edges_dict = {} # solid_name -> solids_edges
    for solid_filename in solid_names:
        solid_name, solid_edges = get_solid_data(folder_name,solid_filename)
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