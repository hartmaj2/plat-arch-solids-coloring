# Extracts edges of the solid specified in solid_name and 
# prints corresponding sage command to create graph with those edges
# Useful when I want to run sage jobs

import solids_prep.solids_dict_prep as sdp

solids = sdp.get_all_solids_dict()
solid_name = "rhombicuboctahedron"

edges = solids[solid_name][sdp.JSON_EDGES]

print(solid_name)
print(f"g = Graph({edges})")