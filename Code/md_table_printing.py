# IMPORTS 

import sys

# TABLE VISUALS

NAME_COL_SIZE : int = 40
CHROM_NO_COL_SIZE : int = 9

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