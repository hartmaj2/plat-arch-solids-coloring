import json
import os

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"
INPUT_FOLDER_PATH = ROOT_FOLDER + "/JsonGraphs"

JSON_NAME = "name"
JSON_VERTICES = "vertices" # inside the json file, each vertex is a tuple containing the coordinates but we just need the amount
JSON_EDGES = "edges"
JSON_FACES = "faces"

ARCHIMEDEAN_FOLDER = "Archimedean"
PLATONIC_FOLDER = "Platonic"

# retrieves the data for the given solid consisting of the name of the solid indices of vertices and the list of edges
def get_processed_data(folder_name: str, solid_filename : str) -> tuple[str,list,list,list]:
    with open(f"{INPUT_FOLDER_PATH}/{folder_name}/{solid_filename}","r") as file:
        graph_data : dict = json.load(file)

        name = graph_data[JSON_NAME]

        vertices = graph_data[JSON_VERTICES]
        vertices = [i for i in range(len(vertices))] # list of vtx coordinates -> list of vtx indices

        edges = graph_data[JSON_EDGES]
        edges = [tuple(edge) for edge in edges] # list of lists -> list of tuples 
        
        faces = graph_data[JSON_FACES]
        faces = [tuple(face) for face in faces] # list of lists -> list of tuples 

        return name,vertices,edges,faces

# normalizes the edges to the format that for (i,j) edge i < j
def get_normalized(edges : list[tuple]):
    normalized = []
    for (i,j) in edges:
        if i < j:
            normalized.append((i,j))
        else:
            normalized.append((j,i))
    return normalized

# sorts the edges lexicographically in ascending order
def lexisort(edges : list[tuple]):
    # we sort in two passes using the fact that the sort is stable
    edges.sort(key = lambda e : e[1]) 
    edges.sort(key = lambda e : e[0])
    
# returns a dictionary indexed by solid name with elements being a dictionary indexed by property name ("vertices" or "edges")
def get_solid_data_dict(folder_name : str, solid_names : list[str]):
    solid_dict = {} # solid_name -> solids_edges
    for solid_filename in solid_names:
        solid_name, solid_vertices, solid_edges, solid_faces  = get_processed_data(folder_name,solid_filename)
        solid_edges = get_normalized(solid_edges) # for convenience, make the edges in format (i,j) where always i < j
        lexisort(solid_edges) # also, we sort the edges lexicographically in ascending order
        lexisort(solid_faces)
        solid_dict[solid_name] = { JSON_VERTICES : solid_vertices, JSON_EDGES : solid_edges, JSON_FACES : solid_faces } # it is a dict of dicts
    return solid_dict

# returns solid dict for platonic solids
def get_platonic_solid_dict():
    solid_names = os.listdir(INPUT_FOLDER_PATH + '/' + PLATONIC_FOLDER) # retrieves solid names in current folder
    return get_solid_data_dict(PLATONIC_FOLDER,solid_names)

# returns solid dict for archimedean solids
def get_archimedean_solid_dict():
    solid_names = os.listdir(INPUT_FOLDER_PATH + '/' + ARCHIMEDEAN_FOLDER) # retrieves solid names in current folder
    return get_solid_data_dict(ARCHIMEDEAN_FOLDER,solid_names)

# returns dict of all solids created by merging results of the separate functions
def get_all_solids_dict():
    return get_platonic_solid_dict() | get_archimedean_solid_dict()

# filters the dict of all solids to include only the ones whose names are contained in the selected solids list
def get_selected_solids_dict(selected_solids : list[str]):
    all_solids = get_all_solids_dict()
    selected_dict = {}
    for solid_name in all_solids.keys():
        if solid_name in selected_solids:
            selected_dict[solid_name] = all_solids[solid_name]
    return selected_dict


# THE FOLLOWING WERE USED TO PRINT THE STANDARD KEY ORDER FOR THE SOLID GRAPHS FOR THE TABLE
# to get the standard ordering of solid keys based on vertex count first and edge count second
def get_std_ordered_key_list(solid_data_dict : dict):
    # get sorted array of keys for the dict
    keys = list(solid_data_dict.keys())
    keys.sort(key = lambda name : len(solid_data_dict[name][JSON_FACES])) # third prioritize num of faces
    keys.sort(key = lambda name : len(solid_data_dict[name][JSON_EDGES])) # second prioritize num of faces
    keys.sort(key = lambda name : len(solid_data_dict[name][JSON_VERTICES])) # first prioritize num of edges
    return keys

# print(get_std_ordered_key_list(get_platonic_solid_dict()))
# print(get_std_ordered_key_list(get_archimedean_solid_dict()))