import json

ROOT_FOLDER = "Code/JsonGraphs/Layouts/"

JSON_NAME = "name"
JSON_VERTICES = "vertices" # inside the json file, each vertex is a tuple containing the coordinates but we just need the amount
JSON_POSITIONS = "pos"

def get_pos_dict(name : str):
    pos = {}
    with open(f"{ROOT_FOLDER}{name}.json") as file:
        data = json.load(file)
        vtces = data[JSON_VERTICES]
        positions = data[JSON_POSITIONS]
        for i in range(len(vtces)):
            pos[vtces[i]] = positions[i]
    return pos