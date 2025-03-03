# IMPORTS 

import sys

# TABLE VISUALS

NAME_COL_SIZE : int = 40
CHROM_NO_COL_SIZE : int = 9

CAPTION_PLACEHOLDER = "Enter caption here."

VTX_CHROM_NUM_HEADER = "X(G)"
EDG_CHROM_NUM_HEADER = "X'(G)"

TABLE_COLS_SEPARATOR = "|"
TABLE_ROWS_SEPARATOR = "-"

# prints a table given the solids in solid_data_dict and the name of the solid category
# prints to the output given by third parameter
def print_solid_chrom_nums(solid_data_dict : dict, solid_category_name = "solid", output_type = sys.stdout):
    header_line_string = f"{TABLE_COLS_SEPARATOR} {solid_category_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {VTX_CHROM_NUM_HEADER:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {EDG_CHROM_NUM_HEADER:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
    header_separator_string = f"{TABLE_COLS_SEPARATOR} {TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR}:{TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{CHROM_NO_COL_SIZE}}:{TABLE_COLS_SEPARATOR}:{TABLE_ROWS_SEPARATOR:{TABLE_ROWS_SEPARATOR}^{CHROM_NO_COL_SIZE}}:{TABLE_COLS_SEPARATOR}"
    print(header_line_string,file=output_type)
    print(header_separator_string,file=output_type)
    for solid_name in sorted(solid_data_dict.keys()):
        vtx_chrom_num, edge_chrom_num = solid_data_dict[solid_name]
        table_entry_row = f"{TABLE_COLS_SEPARATOR} {solid_name:^{NAME_COL_SIZE}} {TABLE_COLS_SEPARATOR} {vtx_chrom_num:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR} {edge_chrom_num:^{CHROM_NO_COL_SIZE}} {TABLE_COLS_SEPARATOR}"
        print(table_entry_row,file=output_type)
    print(file=output_type)

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

# prints md table given the dictionary of data, where the dictionary points from name -> [data1, ... , dataN]
# on input we expect list of header names passed to `data_col_headrs`
def print_solid_mult_col_data(solid_data_dict: dict, solid_category_name : str, data_col_headrs : list[str], data_col_size = 9, caption = CAPTION_PLACEHOLDER, label = "",output_type = sys.stdout):
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
            table_entry_row += f" {solid_data_entry:^{data_col_size}} {TABLE_COLS_SEPARATOR}"
        print(table_entry_row,file=output_type)
    print(file=output_type)