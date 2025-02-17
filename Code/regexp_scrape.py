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

output_file = open(ROOT_FOLDER + "/output_scraped_new.md","w")
output_type = output_file
# output_type = sys.stdout

# scrape solid chromatic numbers (vtx and edg) and store them in the passed dictionary
def scrape_solid_data(solids_search_strings : list[str], solids_dict : dict):

    open_url = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_graphs_by_edges_and_vertices")
    content = open_url.read().decode('utf-8').replace("\n","")
    for solid in solids_search_strings:
        solids_dict[solid] = extract_chrom_nums_regexp(solid,content)

# scrapes the page content string for the data of the given solid
def extract_chrom_nums_regexp(solid_name : str, page_content : str):
    # regexp below first matches characters [space,letter,(,),-,digit] 0 to 30 times
    # then it matches </a></td>, then it skips 6 times <td>something</td> and then it captures two occurences of <td>number<\td>
    pattern = r"[\s\w\(\)\-\d]{0,30}</a></td>(<td>[0-9a-zA-Z\-]*</td>){6}<td>(\d*)</td><td>(\d*)</td>"
    prog = re.compile(solid_name + pattern)
    matches = prog.search(page_content)
    return matches.group(2), matches.group(3)

platonic = {}
archimedean = {}

def main():
    scrape_solid_data(PLATONIC_SEARCH_STRINGS,platonic)
    table_printing.print_solids(platonic,table_printing.PLATONIC_FOLDER_NAME,output_type)
    scrape_solid_data(ARCHIMEDEAN_SEARCH_STRINGS,archimedean)
    table_printing.print_solids(archimedean,table_printing.ARCHIMEDEAN_FOLDER_NAME,output_type)

if __name__ == "__main__":
    main()