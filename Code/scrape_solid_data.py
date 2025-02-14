import urllib.request
import re
import table_printing

# This program web scrapes wikipedia web page for chromatic numbers of platonic and archimedean graphs

# solids names to search for in the given url
PLATONIC_SEARCH_STRINGS = [
    'Tetrahedral',
    'Cubical',
    'Octahedral',
    'Dodecahedral',
    'Icosahedral'
]

ARCHIMEDEAN_SEARCH_STRINGS = [
    'Truncated tetrahedral',
    'Cuboctahedral',
    'Truncated cubical',
    'Truncated octahedral',
    'Rhombicuboctahedral',
    'Truncated cuboctahedral',
    'Snub cubical',
    'Icosidodecahedral',
    'Truncated dodecahedral',
    'Truncated icosahedral',
    'Rhombicosidodecahedral',
    'Truncated icosidodecahedral',
    'Snub dodecahedral'
]

# url to search
URL_TO_OPEN = "https://en.wikipedia.org/wiki/List_of_graphs_by_edges_and_vertices"

ROOT_FOLDER = "Code"

output_file = open(ROOT_FOLDER + "/output_scraped_old.txt","w")
output_type = output_file
# output_type = sys.stdout

# scrape solid chromatic numbers (vtx and edg) and store them in the passed dictionary
def scrape_solid_data(solids_search_strings : list[str], solids_dict : dict):

    f = urllib.request.urlopen(URL_TO_OPEN)
    for line in f:
        line = line.decode('utf-8')
        name_of_found_solid = check_line_contains_any(solids_search_strings,line)
        if name_of_found_solid != None:
            solids_dict[name_of_found_solid] = extract_chrom_nums(f) 

# checks if line contains any of the solids from the list
def check_line_contains_any(solid_names : dict, line : str) -> str | None :
    for solid_name in solid_names:
        res = line.find(solid_name)
        if res != -1:
            return solid_name
    return None

VTX_CHROM_NUM_OFFSET = 6
EDGE_CHROM_NUM_OFFSET = 7
PATTERN = r'^<td>(\d+)</td>$'
PATTERN2 = r'^<td>(\d+)$'

# extract chromatic numbers given the table columns offsets and patterns above
def extract_chrom_nums(open_url) -> tuple[int,int]:
    for i in range(6):
        line = open_url.readline()
    line = open_url.readline().decode('utf-8')
    vtx_chrom_m = re.match(PATTERN,line)
    line = open_url.readline().decode('utf-8')
    edge_chrom_m = re.match(PATTERN2,line)
    return vtx_chrom_m.group(1), edge_chrom_m.group(1)


platonic = {}
archimedean = {}

def main():
    scrape_solid_data(PLATONIC_SEARCH_STRINGS,platonic)
    table_printing.print_solids(platonic,table_printing.PLATONIC_FOLDER_NAME,output_type)
    scrape_solid_data(ARCHIMEDEAN_SEARCH_STRINGS,archimedean)
    table_printing.print_solids(archimedean,table_printing.ARCHIMEDEAN_FOLDER_NAME,output_type)

if __name__ == "__main__":
    main()