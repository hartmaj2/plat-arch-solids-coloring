import md_table_printing as printing
import solids_dict_prep as sdp

DATA_COLUMN_HEADER = "vtx deg"

# since all vertices have same degree, we can wlog count the degree of the first one
def get_degree_of_first_vtx(solid_data : list[list],solid_name : str):
    deg = 0
    for vtx in solid_data[sdp.JSON_VTCES_PROPERTY_KEY_NAME]:
        count = 0
        for edge in solid_data[sdp.JSON_EDGES_PROPERTY_KEY_NAME]:
            if vtx in edge:
                count += 1
        # print(f"degree of {vtx} in {solid_name} has degree {count}")
        if deg != 0 and count != deg:
            print(f"Vertex {vtx} has different degree than some other vertex in {solid_name}") # DEBUG: sanity check if all the vertices really have same degree
        deg = count
    return deg

# count degrees of all the solids
def get_degree_dict(solid_data_dict : dict):
    solid_to_degree = {}
    for solid in solid_data_dict.keys():
        solid_to_degree[solid] = get_degree_of_first_vtx(solid_data_dict[solid],solid)
    return solid_to_degree

def main():
    platonic = sdp.get_platonic_solid_dict()
    plat_degs = get_degree_dict(platonic)
    printing.print_solid_one_col_data(plat_degs,sdp.PLATONIC_FOLDER_NAME,DATA_COLUMN_HEADER)

    archimedean = sdp.get_archimedean_solid_dict()
    arch_degs = get_degree_dict(archimedean)
    printing.print_solid_one_col_data(arch_degs,sdp.ARCHIMEDEAN_FOLDER_NAME,DATA_COLUMN_HEADER)

if __name__ == "__main__":
    main()

