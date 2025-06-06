# IMPORTS 

import sys

# TABLE VISUALS

NAME_COL_SIZE : int = 40
DEFAULT_COL_SIZE : int = 9

CAPTION_PLACEHOLDER = "Enter caption here."

TABLE_COLS_SEPARATOR = "|"
TABLE_ROWS_SEPARATOR = "-"

# prints md table given the dictionary of data for the given solid
def print_solid_one_col_data(solid_data_dict: dict, solid_category_name = "solid", data_col_name = "data", data_col_size = 9, output_type = sys.stdout):
    header_line_string = f"{TABLE_COLS_SEPARATOR} {solid_category_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {data_col_name:^{data_col_size}} {TABLE_COLS_SEPARATOR}"
    header_separator_string = f"{TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR}:{TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{data_col_size}}:{TABLE_COLS_SEPARATOR}"
    print(header_line_string,file=output_type)
    print(header_separator_string,file=output_type)
    for solid_name in sorted(solid_data_dict.keys()):
        solid_data = str(solid_data_dict[solid_name])
        table_entry_row = f"{TABLE_COLS_SEPARATOR} {solid_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {solid_data:^{data_col_size}} {TABLE_COLS_SEPARATOR}"
        print(table_entry_row,file=output_type)
    print(file=output_type)

# for compatibility with chromatic_polys.py latex printing
def print_solid_one_col_poly(solid_data_dict: dict, solid_category_name = "solid", data_col_name = "data", data_alignment = "",output_type = sys.stdout):
    print_solid_one_col_data(solid_data_dict,solid_category_name,data_col_name,output_type=output_type)

# prints md table given the dictionary of data, where the dictionary points from name -> [data1, ... , dataN]
# on input we expect list of header names passed to `data_col_headrs`
def print_solid_mult_col_data(solid_data_dict: dict, solid_category_name : str, data_col_headrs : list[str], data_col_size = DEFAULT_COL_SIZE, caption = CAPTION_PLACEHOLDER, label = "",output_type = sys.stdout, transform = lambda x : str(x)):
    print(caption,file=output_type)
    header_line_string = f"{TABLE_COLS_SEPARATOR} {solid_category_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
    header_separator_string = f"{TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
    for data_col_headr in data_col_headrs:
        header_line_string += f" {data_col_headr:^{data_col_size}} {TABLE_COLS_SEPARATOR}"
        header_separator_string += f":{TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{data_col_size}}:{TABLE_COLS_SEPARATOR}"
    print(header_line_string,file=output_type)
    print(header_separator_string,file=output_type)
    for solid_name in sorted(solid_data_dict.keys()):
        solid_data_cols = solid_data_dict[solid_name]
        table_entry_row = f"{TABLE_COLS_SEPARATOR} {solid_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
        for solid_data_entry in solid_data_cols:
            table_entry_row += f" {transform(solid_data_entry):^{data_col_size}} {TABLE_COLS_SEPARATOR}"
        print(table_entry_row,file=output_type)
    print(file=output_type)