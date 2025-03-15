# IMPORTS 

import sys
import re

# TABLE VISUALS

TABLE_BEGIN_HERE = r"\begin{table}[H]"
TABLE_END = r"\end{table}"
CENTERING = r"\centering"
CAPTION_PLACEHOLDER = "Enter caption here."
LABEL_PLACEHOLDER = "tab:enter-custom-label-here"

TABULAR_BEGIN = r"\begin{tabular}"
TABULAR_END = r"\end{tabular}"

ALIGNMENT_CHAR_CENTER = 'c'
ALIGNMENT_CHAR_LEFT = 'l'

BOLDTEXT = r"\textbf{"
HORIZ_SPACE = r"@{\hspace{1.5cm}}"

TOPRULE = r"\toprule"
MIDRULE = r"\midrule"
BOTTOMRULE = r"\bottomrule"

LATEX_NEWLINE = r"\\"
LATEX_COL_SEPARATOR = '&'

CURLY_BRACE_LEFT = r"{"
CURLY_BRACE_RIGHT = r"}"

PLATONIC_OUTPUT_NAMES = ["tetrahedron","cube","octahedron","dodecahedron","icosahedron"]
ARCHIMEDEAN_OUTPUT_NAMES = ["truncated icosidodecahedron","truncated cube","icosidodecahedron","rhombicuboctahedron","truncated icosahedron","truncated octahedron","snub cube","truncated cuboctahedron","truncated tetrahedron","cuboctahedron","snub dodecahedron","truncated dodecahedron","rhombicosidodecahedron"]

# prints latex table given the dictionary of data, where the dictionary points from name -> [data1, ... , dataN]
# on input we expect list of header names passed to `data_col_headrs`
# we can also specify transformation to be applied on ALL the data in the solid_data_dict (be default, this is just conversion to string)
def print_solid_mult_col_data(key_data_dict: dict, text_col_header : str, data_col_headrs : list[str], caption = CAPTION_PLACEHOLDER, label = LABEL_PLACEHOLDER, output_type = sys.stdout, transform = lambda x : str(x), data_alignment_str = ALIGNMENT_CHAR_CENTER):
    # PRINT HEADER AND ENVIRONMENT THINGIES
    print(TABLE_BEGIN_HERE,file=output_type)
    print(CENTERING,file=output_type)
    # PRINT TABULAR FORMAT STRING
    tabular_format_string = get_tabular_format_string(data_col_headrs, data_alignment_str)
    print(tabular_format_string,file=output_type)
    print(TOPRULE,file=output_type)
    # PRINT HEADER
    header_line_string = get_header_line_string(text_col_header,data_col_headrs)
    print(header_line_string,file=output_type)
    print(MIDRULE,file=output_type)
    # END OF HEADER PRINTING
    for solid_name in sorted(key_data_dict.keys()):
        solid_data_cols = key_data_dict[solid_name]
        table_entry_row = f"{solid_name}"
        for solid_data_entry in solid_data_cols:
            table_entry_row += f" {LATEX_COL_SEPARATOR} {transform(solid_data_entry)}"
        table_entry_row += f" {LATEX_NEWLINE}"
        print(table_entry_row,file=output_type)
    print(BOTTOMRULE,file=output_type)
    print(TABULAR_END,file=output_type)
    # PRINT CAPTION AND LABEL
    print_caption_and_label(caption,label,output_type)
    print(TABLE_END,file=output_type)
    print(file=output_type)

def print_caption_and_label(caption : str, label : str, output_type):
    print(r"\caption{",file=output_type,end="")
    print(caption,file=output_type,end="")
    print(r"}",file=output_type)
    print(r"\label{",file=output_type,end="")
    print(label,file=output_type,end="")
    print(r"}",file=output_type)

def get_tabular_format_string(data_col_headers : list[str], data_alignment_str):
    tabular_format_string = f"{TABULAR_BEGIN}{CURLY_BRACE_LEFT}{ALIGNMENT_CHAR_LEFT}{HORIZ_SPACE}"
    for _ in data_col_headers:
        tabular_format_string += f"{data_alignment_str}"
    tabular_format_string += f"{CURLY_BRACE_RIGHT}"
    return tabular_format_string

def get_header_line_string(text_col_header : str, data_col_headers : list[str]):
    header_line_string = f"{BOLDTEXT}{text_col_header}{CURLY_BRACE_RIGHT}"
    for col_headr in data_col_headers:
        header_line_string += f" {LATEX_COL_SEPARATOR} {BOLDTEXT}{col_headr}{CURLY_BRACE_RIGHT}"
    header_line_string += f" {LATEX_NEWLINE}"
    return header_line_string