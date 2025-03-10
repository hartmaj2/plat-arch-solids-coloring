import t_printing.md_table_printing as printing
import solids_prep.solids_dict_prep as sdp

DATA_COLUMN_HEADER = "vtx deg"
DATA_HEADERS = ["v","e","f","d"]

# since all vertices have same degree, we can wlog count the degree of the first one
def get_degree_of_vtces(solid_data : dict[list], solid_name : str):
    deg = 0
    for vtx in solid_data[sdp.JSON_VERTICES]:
        count = 0
        for edge in solid_data[sdp.JSON_EDGES]:
            if vtx in edge:
                count += 1
        # print(f"degree of {vtx} in {solid_name} has degree {count}")
        if deg != 0 and count != deg:
            print(f"Vertex {vtx} has different degree than some other vertex in {solid_name}") # DEBUG: sanity check if all the vertices really have same degree
        deg = count
    return deg

def get_num_vtces(solid_data : dict[list]):
    return len(solid_data[sdp.JSON_VERTICES])

def get_num_edges(solid_data : dict[list]):
    return len(solid_data[sdp.JSON_EDGES])

# compute number of faces using the fact that the graphs are planar -> Euler's formula: v + f = e + 2
def get_num_faces(solid_data : dict[list]):
    return 2 + get_num_edges(solid_data) - get_num_vtces(solid_data)

# count degrees of all the solids
def get_degree_dict(solid_data_dict : dict):
    solid_to_degree = {}
    for solid in solid_data_dict.keys():
        solid_to_degree[solid] = get_degree_of_vtces(solid_data_dict[solid],solid)
    return solid_to_degree

def get_v_e_f_d_dict(solid_data_dict : dict):
    solid_to_data = {}
    for solid in solid_data_dict:
        data = solid_data_dict[solid]
        solid_to_data[solid] = [get_num_vtces(data),get_num_edges(data),get_num_faces(data),get_degree_of_vtces(data,solid)]
    return solid_to_data

def main():
    platonic = sdp.get_platonic_solid_dict()
    plat_data = get_v_e_f_d_dict(platonic)
    printing.print_solid_mult_col_data(plat_data,sdp.PLATONIC_FOLDER,DATA_HEADERS)

    archimedean = sdp.get_archimedean_solid_dict()
    arch_data = get_v_e_f_d_dict(archimedean)
    printing.print_solid_mult_col_data(arch_data,sdp.ARCHIMEDEAN_FOLDER,DATA_HEADERS)

if __name__ == "__main__":
    main()

