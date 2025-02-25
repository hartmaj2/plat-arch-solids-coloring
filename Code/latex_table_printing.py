# IMPORTS 

import sys
import re

# TABLE VISUALS

NAME_COL_SIZE : int = 30
CHROM_NO_COL_SIZE : int = 9

TABLE_BEGIN_HERE = r"\begin{table}[H]"
TABLE_END = r"\end{table}"
CENTERING = r"\centering"
CAPTION_PLACEHOLDER = r"\caption{Enter caption here.}"
VERTICAL_SPACE = r"\vspace{5pt}"
LABEL_PLACEHOLDER = r"\label{tab:enter-custom-label-here}"

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
    print(TABLE_BEGIN_HERE,file=output_type)
    print(CENTERING,file=output_type)
    print(CAPTION_PLACEHOLDER,file=output_type)
    print(VERTICAL_SPACE,file=output_type)
    print(LABEL_PLACEHOLDER,file=output_type)
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
    print(TABLE_END,file=output_type)

# prints latex table given the dictionary of data for the given solid
def print_solid_one_col_data(solid_data_dict: dict, solid_category_name = "solid", data_col_name = "data", data_alignment = ALIGNMENT_CHAR_CENTER, output_type = sys.stdout, transform = lambda x : str(x)):
    # PRINT HEADER AND ENVIRONMENT THINGIES
    tabular_format_string = f"{TABULAR_BEGIN}{CURLY_BRACE_LEFT}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_LEFT}{TABLE_VERTICAL_LINE_MARKER}{data_alignment}{TABLE_VERTICAL_LINE_MARKER}{CURLY_BRACE_RIGHT}"
    print(TABLE_BEGIN_HERE,file=output_type)
    print(CENTERING,file=output_type)
    print(CAPTION_PLACEHOLDER,file=output_type)
    print(VERTICAL_SPACE,file=output_type)
    print(LABEL_PLACEHOLDER,file=output_type)
    print(tabular_format_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE,file=output_type)
    header_line_string = f"{solid_category_name} {LATEX_COL_SEPARATOR} {data_col_name} {LATEX_NEWLINE}"
    print(header_line_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE + LATEX_HORIZONTAL_LINE,file=output_type)
    # END OF HEADER PRINTING
    for solid_name in sorted(solid_data_dict.keys()):
        solid_data = transform(solid_data_dict[solid_name])
        table_entry_row = f"{solid_name} {LATEX_COL_SEPARATOR} {solid_data} {LATEX_NEWLINE}"
        print(table_entry_row,file=output_type)
        print(LATEX_HORIZONTAL_LINE,file=output_type)
    print(TABULAR_END,file=output_type)
    print(TABLE_END,file=output_type)

# prints latex table given the dictionary of data, where the dictionary points from name -> [data1, ... , dataN]
# on input we expect list of header names passed to `data_col_headrs`
def print_solid_mult_col_data(solid_data_dict: dict, solid_category_name : str, data_col_headrs : list[str], data_col_size = 9, output_type = sys.stdout):
    # PRINT HEADER AND ENVIRONMENT THINGIES
    tabular_format_string = f"{TABULAR_BEGIN}{CURLY_BRACE_LEFT}{TABLE_VERTICAL_LINE_MARKER}{ALIGNMENT_CHAR_LEFT}{TABLE_VERTICAL_LINE_MARKER}"
    header_line_string = f"{solid_category_name}"
    for col_headr in data_col_headrs:
        tabular_format_string += f"{ALIGNMENT_CHAR_CENTER}{TABLE_VERTICAL_LINE_MARKER}"
        header_line_string += f" {LATEX_COL_SEPARATOR} {col_headr}"
    tabular_format_string += f"{CURLY_BRACE_RIGHT}"
    header_line_string += f" {LATEX_NEWLINE}"
    print(TABLE_BEGIN_HERE,file=output_type)
    print(CENTERING,file=output_type)
    print(CAPTION_PLACEHOLDER,file=output_type)
    print(VERTICAL_SPACE,file=output_type)
    print(LABEL_PLACEHOLDER,file=output_type)
    print(tabular_format_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE,file=output_type)
    print(header_line_string,file=output_type)
    print(LATEX_HORIZONTAL_LINE + LATEX_HORIZONTAL_LINE,file=output_type)
    # END OF HEADER PRINTING
    for solid_name in sorted(solid_data_dict.keys()):
        solid_data_cols = solid_data_dict[solid_name]
        table_entry_row = f"{solid_name}"
        for solid_data_entry in solid_data_cols:
            table_entry_row += f" {LATEX_COL_SEPARATOR} {solid_data_entry}"
        table_entry_row += f" {LATEX_NEWLINE}"
        print(table_entry_row,file=output_type)
        print(LATEX_HORIZONTAL_LINE,file=output_type)
    print(TABULAR_END,file=output_type)
    print(TABLE_END,file=output_type)

def print_solid_one_col_poly(solid_data_dict: dict, solid_category_name = "solid", data_col_name = "data", data_alignment = "p{0.5\\linewidth}",output_type = sys.stdout):
    print_solid_one_col_data(solid_data_dict,solid_category_name,data_col_name,data_alignment,output_type,poly_to_latex)

# converts polynomial sage object to a string and then replaces the necessary part with proper latex syntax and wraps in equation environment
def poly_to_latex(polynomial):
    str_with_wrong_superscripts =  "$" + str(polynomial).replace("*","") + "$"
    return re.sub(r'\^(\d+)',"^{\\1}",str_with_wrong_superscripts) # replaces x^123 with x^{123} for example