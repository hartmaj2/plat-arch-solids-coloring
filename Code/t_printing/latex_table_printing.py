# IMPORTS 

import sys
import re

# TABLE VISUALS

STD_PLAT_TABLE_ORDER = ['tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron']
STD_ARCHIMEDEAN_TABLE_ORDER = ['truncated tetrahedron', 'cuboctahedron', 'truncated cube', 'truncated octahedron', 'rhombicuboctahedron', 'icosidodecahedron', 'snub cube', 'truncated cuboctahedron', 'truncated icosahedron', 'truncated dodecahedron', 'rhombicosidodecahedron', 'snub dodecahedron', 'truncated icosidodecahedron']

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
HORIZ_SPACE_BEGIN = r"@{\hspace{"
HORIZ_SPACE_END = r"cm}}"
DEFAULT_HORIZ_SPACE_VAL = 1.5

TOPRULE = r"\toprule"
MIDRULE = r"\midrule"
BOTTOMRULE = r"\bottomrule"

LATEX_NEWLINE = r"\\"
LATEX_COL_SEPARATOR = '&'

CURLY_BRACE_LEFT = r"{"
CURLY_BRACE_RIGHT = r"}"

STRETCH_COMMAND = r'\renewcommand{\arraystretch}{'
STRETCH_DEFAULT_VALUE = 1.0

# prints latex table given the dictionary of data, where the dictionary points from name -> [data1, ... , dataN]
# on input we expect list of header names passed to `data_col_headrs`
# we can also specify transformation to be applied on ALL the data in the solid_data_dict (be default, this is just conversion to string)
def print_solid_mult_col_data(key_data_dict: dict, key_order : list[str], text_col_header : str, data_col_headrs : list[str], caption = CAPTION_PLACEHOLDER, label = LABEL_PLACEHOLDER, output_type = sys.stdout, transform = lambda x : str(x), data_alignment_str = ALIGNMENT_CHAR_CENTER, first_col_horiz_space = DEFAULT_HORIZ_SPACE_VAL,row_spacing = STRETCH_DEFAULT_VALUE):
    adapted_dict = adapt_dict_for_mult_row_data(key_data_dict)
    print_solid_mult_row_data(adapted_dict,key_order,text_col_header,data_col_headrs,caption,label,output_type,transform,data_alignment_str,row_spacing,first_col_horiz_space,"")

def print_caption_and_label(caption : str, label : str, output_type):
    print(r"\caption{",file=output_type,end="")
    print(caption,file=output_type,end="")
    print(r"}",file=output_type)
    print(r"\label{",file=output_type,end="")
    print(label,file=output_type,end="")
    print(r"}",file=output_type)

def get_tabular_format_string(data_col_headers : list[str], data_alignment_str, horiz_space_val : float):
    tabular_format_string = f"{TABULAR_BEGIN}{CURLY_BRACE_LEFT}{ALIGNMENT_CHAR_LEFT}{HORIZ_SPACE_BEGIN}{horiz_space_val}{HORIZ_SPACE_END}"
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

def adapt_dict_for_mult_row_data(key_data_dict : dict) -> dict:
    new = {}
    for key,val in zip(key_data_dict.keys(),key_data_dict.values()):
        new[key] = [val] # this creates a single row with the value val
    return new

# same like mult col but for some key, there might be multiple rows after another
# so now, the key_data_dict must contain for each key a list of rows where each row is the size of data_col_headrs
def print_solid_mult_row_data(key_data_dict: dict, key_order : list[str], text_col_header : str, data_col_headrs : list[str], caption = CAPTION_PLACEHOLDER, label = LABEL_PLACEHOLDER, output_type = sys.stdout, transform = lambda x : str(x), data_alignment_str = ALIGNMENT_CHAR_CENTER, row_spacing = STRETCH_DEFAULT_VALUE,first_col_horiz_space=DEFAULT_HORIZ_SPACE_VAL,row_cluster_sep = MIDRULE):
    
    # MAYBE CHANGE ROW SPACING
    if row_spacing != STRETCH_DEFAULT_VALUE:
        print(f"{STRETCH_COMMAND}{row_spacing:.1f}{CURLY_BRACE_RIGHT}",file=output_type)

    # PRINT HEADER AND ENVIRONMENT THINGIES
    print(TABLE_BEGIN_HERE,file=output_type)
    print(CENTERING,file=output_type)
    # PRINT TABULAR FORMAT STRING
    tabular_format_string = get_tabular_format_string(data_col_headrs, data_alignment_str,first_col_horiz_space)
    print(tabular_format_string,file=output_type)
    print(TOPRULE,file=output_type)
    # PRINT HEADER
    header_line_string = get_header_line_string(text_col_header,data_col_headrs)
    print(header_line_string,file=output_type)
    print(MIDRULE,file=output_type)
    # END OF HEADER PRINTING
    for i,solid_name in enumerate(key_order):
        rows = key_data_dict[solid_name]
        for j,data_row in enumerate(rows):
            table_entry_row = ""
            if j == 0: # only the first row in the cluster has the name of the solid there
                table_entry_row += f"{solid_name}"
            for solid_data_entry in data_row:
                table_entry_row += f" {LATEX_COL_SEPARATOR} {transform(solid_data_entry)}"
            table_entry_row += f" {LATEX_NEWLINE}"
            print(table_entry_row,file=output_type)
        if row_cluster_sep != "" and i != len(key_data_dict) - 1: # print the cluster separator only if there is some (can be a midrule or something similar)
            print(row_cluster_sep)
    print(BOTTOMRULE,file=output_type)
    print(TABULAR_END,file=output_type)
    # PRINT CAPTION AND LABEL
    print_caption_and_label(caption,label,output_type)
    print(TABLE_END,file=output_type)

    # MAYBE CHANGE ROW SPACING BACK TO DEFAULT
    if row_spacing != STRETCH_DEFAULT_VALUE:
        print(f"{STRETCH_COMMAND}{STRETCH_DEFAULT_VALUE}{CURLY_BRACE_RIGHT}",file=output_type)

    print(file=output_type)