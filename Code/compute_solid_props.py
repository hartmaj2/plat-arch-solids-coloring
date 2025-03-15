import t_printing.latex_table_printing as printing
import solids_prep.solids_dict_prep as sdp

# Creates a table showing basic properties of the archimedean solids like # of vertices, edges, faces, and the degree of each vertex

# OUTPUT TABLE SETTINGS
MD_DATA_HEADERS = ["v","e","f","d","vertex config"]
LATEX_DATA_HEADERS = ["$|V|$","$|E|$","$|F|$","$d$","Vertex config."]
data_headers = LATEX_DATA_HEADERS

PLAT_CAPTION = "Basic properties of Platonic graphs"
PLAT_LABEL = "tab:platonic-basic-props"
ARCH_CAPTION = "Basic properties of Archimedean graphs"
ARCH_LABEL = "tab:archimedean-basic-props"

# INPUT FILE SETTINGS

ROOT_FOLDER = "Code"

# OUTPUT SETTING

# uncomment following 2 lines to output to a folder
output_file = open(ROOT_FOLDER + "/Results/graph_props2.md","w")
output_type = output_file

# import sys
# output_type = sys.stdout

# since all vertices have same degree, we can wlog count the degree of the first one
def get_degree_of_vtces(solid_data : dict[str,list]):
    deg = 0
    for vtx in solid_data[sdp.JSON_VERTICES]:
        count = 0
        for edge in solid_data[sdp.JSON_EDGES]:
            if vtx in edge:
                count += 1
        if deg != 0 and count != deg:
            print(f"Vertex {vtx} has different degree than some other vertex.") # DEBUG: sanity check if all the vertices really have same degree
        deg = count
    return deg

def get_num_vtces(solid_data : dict[str,list]):
    return len(solid_data[sdp.JSON_VERTICES])

def get_num_edges(solid_data : dict[str,list]):
    return len(solid_data[sdp.JSON_EDGES])

# compute number of faces using the fact that the graphs are planar -> Euler's formula: v + f = e + 2
def get_num_faces(solid_data : dict[str,list]):
    return 2 + get_num_edges(solid_data) - get_num_vtces(solid_data)

# compute vertex configuration using the faces list of the solid
# ASSUMPTION: the face tuples when lexicographically sorted are then in a correct order of how the faces go around the vertex
def get_vtx_config(solid_data : dict[str,list]):
    face_type_list = []
    for face in solid_data[sdp.JSON_FACES]:
        if 0 not in face:
            break
        face_type_list.append(len(face)) # the face just contains list of n vertices that lie on the face so that corresponds to n-gonality of the face
    return ".".join([str(num) for num in normalize_vertex_conf(face_type_list)])

def normalize_vertex_conf(vtx_conf_list : list[int]):
    m = min(vtx_conf_list)
    mi = vtx_conf_list.index(m)
    normalized = []
    for i in range(len(vtx_conf_list)):
        normalized.append(vtx_conf_list[(mi + i) % len(vtx_conf_list)])
    return normalized


def get_v_e_f_d_dict(solid_data_dict : dict):
    solid_to_data = {}
    for solid in solid_data_dict:
        data = solid_data_dict[solid]
        solid_to_data[solid] = [get_num_vtces(data),get_num_edges(data),get_num_faces(data),get_degree_of_vtces(data),get_vtx_config(data)]
    return solid_to_data

def main():
    platonic = sdp.get_platonic_solid_dict()
    plat_data = get_v_e_f_d_dict(platonic)
    printing.print_solid_mult_col_data(plat_data,sdp.PLATONIC_FOLDER,data_headers,caption=PLAT_CAPTION,label=PLAT_LABEL,output_type=output_type)

    archimedean = sdp.get_archimedean_solid_dict()
    arch_data = get_v_e_f_d_dict(archimedean)
    printing.print_solid_mult_col_data(arch_data,sdp.ARCHIMEDEAN_FOLDER,data_headers,caption=ARCH_CAPTION,label=ARCH_LABEL,output_type=output_type)

if __name__ == "__main__":
    main()

