# IMPORTS 

import sys

# TABLE VISUALS

NAME_COL_SIZE : int = 30
CHROM_NO_COL_SIZE : int = 9

TABULAR_BEGIN = r"\begin{tabular}"
TABULAR_END = r"\end{tabular}"

VTX_CHROM_NUM_HEADER = r"$\chi(G)$"
EDG_CHROM_NUM_HEADER = r"$\chi'(G)$"

TABLE_VERTICAL_LINE_MARKER = '|'
ALIGNMENT_CHAR_CENTER = 'c'
ALIGNMENT_CHAR_LEFT = 'l'

LATEX_HORIZONTAL_LINE = r"\hline"
LATEX_NEWLINE = r"\\"
LATEX_COL_SEPARATOR = '&'

CURLY_BRACE_LEFT = r"{"
CURLY_BRACE_RIGHT = r"}"

ARCHIMEDEAN_FOLDER_NAME = "Archimedean"
PLATONIC_FOLDER_NAME = "Platonic"

PLATONIC_OUTPUT_NAMES = ["tetrahedron","cube","octahedron","dodecahedron","icosahedron"]
ARCHIMEDEAN_OUTPUT_NAMES = ["truncated icosidodecahedron","truncated cube","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","truncated octahedron","snub cube","truncated cuboctahedron","truncated tetrahedron","cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron",]

def print_solids(solid_dict : dict, solid_category : str, output_type = sys.stdout):
    tabular_format_string = f"{TABULAR_BEGIN}{CURLY_BRACE_LEFT}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_LEFT}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_CENTER}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_CENTER}{TABLE_VERTICAL_LINE_MARKER}{CURLY_BRACE_RIGHT}"
    print(tabular_format_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE,file=output_type)
    header_line_string = f"{solid_category} {LATEX_COL_SEPARATOR} {VTX_CHROM_NUM_HEADER} {LATEX_COL_SEPARATOR} {EDG_CHROM_NUM_HEADER} {LATEX_NEWLINE}"
    print(header_line_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE + LATEX_HORIZONTAL_LINE,file=output_type)
    for solid_name in sorted(solid_dict.keys()):
        vtx_chrom_num, edge_chrom_num = solid_dict[solid_name]
        table_entry_row = f"{solid_name} {LATEX_COL_SEPARATOR} {vtx_chrom_num} {LATEX_COL_SEPARATOR} {edge_chrom_num} {LATEX_NEWLINE}"
        print(table_entry_row,file=output_type)
        print(LATEX_HORIZONTAL_LINE,file=output_type)
    print(TABULAR_END,file=output_type)


# prints latex table given the dictionary of data for the given solid
def print_solid_one_col_data(solid_data_dict: dict, solid_category_name = "solid", data_col_name = "data", output_type = sys.stdout):
    tabular_format_string = f"{TABULAR_BEGIN}{CURLY_BRACE_LEFT}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_LEFT}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_CENTER}{TABLE_VERTICAL_LINE_MARKER}{CURLY_BRACE_RIGHT}"
    print(tabular_format_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE,file=output_type)
    header_line_string = f"{solid_category_name} {LATEX_COL_SEPARATOR} {str(data_col_name)} {LATEX_NEWLINE}"
    print(header_line_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE + LATEX_HORIZONTAL_LINE,file=output_type)
    for solid_name in sorted(solid_data_dict.keys()):
        solid_data = str(solid_data_dict[solid_name])
        table_entry_row = f"{solid_name} {LATEX_COL_SEPARATOR} {solid_data} {LATEX_NEWLINE}"
        print(table_entry_row,file=output_type)
        print(LATEX_HORIZONTAL_LINE,file=output_type)
    print(TABULAR_END,file=output_type)