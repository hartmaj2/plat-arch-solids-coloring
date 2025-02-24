import md_table_printing as printing
import solids_dict_prep as sdp

DATA_COLUMN_HEADER = "vertex degree"


# since all vertices have same degree, we can wlog count the degree of the first one
def get_degree_of_first_vtx(solid_edges : list[list]):
    count = 0
    for edge in solid_edges:
        if 0 in edge:
            count += 1
    return count

# just count degrees of all the solids
def get_degree_dict(solid_to_edges : dict):
    solid_to_degree = {}
    for solid in solid_to_edges.keys():
        solid_to_degree[solid] = get_degree_of_first_vtx(solid_to_edges[solid])
    return solid_to_degree

def main():
    platonic = sdp.get_platonic_edges_dict()
    plat_degs = get_degree_dict(platonic)
    printing.print_solid_one_col_data(plat_degs,sdp.PLATONIC_FOLDER_NAME,DATA_COLUMN_HEADER)

    archimedean = sdp.get_archimedean_edges_dict()
    arch_degs = get_degree_dict(archimedean)
    printing.print_solid_one_col_data(arch_degs,sdp.ARCHIMEDEAN_FOLDER_NAME,DATA_COLUMN_HEADER)

if __name__ == "__main__":
    main()

