import solids_prep.solids_dict_prep as sdp

VERTICES = sdp.JSON_VERTICES
EDGES = sdp.JSON_EDGES
NAME = sdp.JSON_NAME
# platonic = sdp.get_platonic_solid_dict()
# archimedean = sdp.get_archimedean_solid_dict()

# creates adjacency list from the dictionary of vertices [0,...,n-1]
def create_adj_list(solid : dict[str,dict]) -> list:
    adj_list = [[] for vtx in solid[VERTICES]]
    for (i,j) in solid[EDGES]:
        adj_list[i].append(j)
        adj_list[j].append(i)
    return adj_list

# creates a map from edges of the original graph to their new labels {n,...,n+m-1}
# IMPORTANT: we assume edges are lexicographically ordered
def create_edge_map(solid : dict[str,dict]) -> dict:
    edge_map = {}
    current_index = len(solid[VERTICES])
    for edge in solid[EDGES]:
        edge_map[edge] = current_index
        current_index += 1
    return edge_map

# creates a line graph using the adjacency list and the edge map
def create_line_graph(solid: dict[str,dict]):
    adj_list = create_adj_list(solid)
    edge_map = create_edge_map(solid)
    lg = {}
    lg[VERTICES] = edge_map.values()
    lg[EDGES] = get_line_graph_edges(adj_list,edge_map)
    return lg

def get_line_graph_edges(adj_list : list[list], edge_map : dict[tuple,int]):
    lg_edges = []
    for (i,j) in edge_map.keys(): # note that by ordering of edges in edge_map: i < j
        for v in adj_list[i]: # there exists an edge (i,v) or (v,i)
            if v > j: # since v > j and j > i we have v > i so the edge is in format (i,v) and also is lexicographically ahead
                lg_edges.append((edge_map[(i,j)],edge_map[(i,v)]))
        for v in adj_list[j]: # there exists an edge (j,v) or (v,j)
            if v < j and v > i: # the edge is in format (v,j) and since v > i it is lexicographically ahead
                lg_edges.append((edge_map[(i,j)],edge_map[(v,j)]))
            if v > j: # the edge is in format (j,v) and since j > i it must be lexicographically ahead
                lg_edges.append((edge_map[(i,j)],edge_map[(j,v)]))
    return lg_edges

# given edges and edge map constructs edges of the corresponding incidence graph
def get_incid_graph_edges(edges : list[tuple], edge_map : dict[tuple,int]):
    ig_edges = []
    for (i,j) in edges:
        ig_edges.append((i,edge_map[(i,j)]))
        ig_edges.append((j,edge_map[(i,j)]))
    return ig_edges

# creates total graph using the original graph vertices and edges, line graph vertices and edges and incidence graph edges
def create_total_graph(solid : dict[str,dict]):
    adj_list = create_adj_list(solid)
    edge_map = create_edge_map(solid)
    lg_edges = get_line_graph_edges(adj_list,edge_map)
    ig_edges = get_incid_graph_edges(solid[EDGES],edge_map)
    tg = {}
    tg[VERTICES] = solid[VERTICES] + list(edge_map.values())
    tg[EDGES] = solid[EDGES] + lg_edges + ig_edges
    return tg

# for name in platonic.keys():
#     tg = create_total_graph(platonic[name])
#     print(f"{name}\nm={len(tg[EDGES])}")

# print()

# for name in archimedean.keys():
#     tg = create_total_graph(archimedean[name])
#     print(f"{name}\nm={len(tg[EDGES])}")