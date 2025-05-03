#!/usr/local/bin/sage -python
# This program calculates num of relaut equiv classes using generation of all set partitions and then filtering

import solids_prep.solids_dict_prep as sdp

import timing.timing as tmng
import time as tm

from sage.all import Graph
from sage.all import *

import multiprocessing as mp

# BEGIN: COLORING STANDARDIZATION BY FINGERPRIT

class Fprint:
    # fingerprint stores information about sizes of independent sets of the colorings
    # contains tuples in format (count_of_vtces,clr_val)
    @staticmethod
    def create_fprint(coloring_list : list[int]) -> list[tuple]:
        num_clrs = max(coloring_list) + 1 # there is one more colors than what is the label of the greatest valued color
        fingerprint = [[0,clr] for clr in range(num_clrs)] # stores a pair in format (count_of_vertices,color_value)
        for clr in coloring_list:
            fingerprint[clr][0] += 1 # increase the count component of the pair
        return sorted([tuple(pair) for pair in fingerprint],key=lambda pair : pair[0]) # return the fingerprint sorted based on the sizes of indep sets

    # makes a string out of the fingerprint where each number is encoded as a letter from the alphabet
    # this will later allow for lexicographic sorting of the fingerprints after they are ordered
    @staticmethod
    def stringify_fprnt_counts(fingerprint : list[tuple]) -> str:
        return "".join([chr(count) for (count,clr) in fingerprint]) # join the result into one string

    # like the above but uses the color values to stringify
    @staticmethod
    def stringify_fprnt_clr_vals(fingerprint : list[tuple]) -> str:
        return "".join([chr(clr) for (count,clr) in fingerprint]) # join the result into one string

    # returns list of fingerprinted colorings where each fingerprinted coloring is a tuple in form (clring as list, fingerprint)
    @staticmethod
    def get_fprnted_clrings(colorings_as_list : list[list]) -> list[tuple]:
        return [(clring,Fprint.create_fprint(clring)) for clring in colorings_as_list]

    @staticmethod
    def stringify(tuple : tuple[int]) -> str:
        return "".join([str(a) for a in tuple])

    # takes a coloring corresponding to some independent set and its fingerprint
    # uses the fingerprint to recolor the independent sets based on their sizes
    @staticmethod
    def recolor_indep_sets_by_sizes(fingerprinted : tuple[list[int],list[tuple]]) -> tuple[list[int],tuple[int]]:
        orig_coloring = Fprint.get_coloring(fingerprinted)
        num_clrs = max(orig_coloring) + 1
        sorted_fprint = Fprint.get_fingerprint(fingerprinted).copy()
        sorted_fprint.sort(key=lambda tup : tup[0],reverse=True)
        color_mapping = [0] * num_clrs
        for i,tup in enumerate(sorted_fprint):
            color_mapping[tup[1]] = i
        new_clring_list = [color_mapping[clr] for clr in orig_coloring]
        return (new_clring_list, tuple([size for (size,clr) in Fprint.create_fprint(new_clring_list)]))

    # recolors all fingerprinted colorings to standard form (largest indep sets get lower index colors)
    @staticmethod
    def get_standardized(fingerprinteds : list[tuple[list[int],list[tuple]]]) -> list[tuple[list[int],tuple[int]]]:
     return [Fprint.recolor_indep_sets_by_sizes(fprinted) for fprinted in fingerprinteds]

    # retrieves the fingerprint out of the fingerprinted coloring
    @staticmethod
    def get_fingerprint(fingerprinted_coloring: tuple[list,list]) -> list:
        return fingerprinted_coloring[1]

    @staticmethod
    def get_coloring(fingerprinted_coloring: tuple[list,list]) -> list:
        return fingerprinted_coloring[0]

    @staticmethod
    # extracts only the sizes part of the fingerprint as tuple (to be used for hashing)
    def get_sizes_vector(fingerprint : list[tuple]) -> tuple:
        return tuple([size for (size,clr) in fingerprint])
    
# END: COLORING STANDARDIZATION BY FINGERPRIT

# BEGIN: GETTING ALL COLORINGS AS LIST
class Clr:
    # converts the coloring in dict format to list format
    @staticmethod
    def get_coloring_list(clring_as_dict : dict[int,list]) -> list[int]:
        num_vertices = len(reduce(lambda x,y: x + y,clring_as_dict.values(),[])) # reduce is equivalent of foldl in functional programming languages
        clring_as_list = [0 for _ in range(num_vertices)]
        for color in clring_as_dict.keys():
            for vtx in clring_as_dict[color]:
                clring_as_list[vtx] = color
        return clring_as_list

# END: GETTING ALL COLORINGS AS LIST

class Comp:
    # tries to unify two colorings by building a permutation of colors on the fly
    # the permutation has to be valid and all vertices have to be checked
    # permutation is invalid if two colors try to map to the same color or if one color tries to map to multiple colors
    # permutation will be represented by two lists: img and preimg
    @staticmethod
    def try_unify_by_aut(c1 : list[int], c2 : list[int], a : list[tuple], num_clrs : int) -> tuple | None:
        img = [-1] * num_clrs # -1 means mapped to no color yet
        preimg = [-1] * num_clrs # -1 means no color mapped to this yet
        for cycle in a:
            k = len(cycle)
            for i in range(k):
                vtx_preim = cycle[i]
                vtx_img = cycle[(i+1)%k]
                b1 = c1[vtx_preim]
                b2 = c2[vtx_img]
                if img[b1] == -1: # b1 not mapped to anything yet
                    if preimg[b2] != -1: # some other color has already mapped to b2
                        return None
                    else: # we can map b1 -> b2
                        img[b1] = b2
                        preimg[b2] = b1
                else:
                    if img[b1] != b2: # we have already mapped to some other color so we cannot map to this one as well
                        return None
        return tuple(img)

    # function that receives two colorings and a graph and returns automorphism (as list of cycles) and relabeling by which they can be unified or None
    # result means that we can get from c1 to c2 using automorphism a and relabel r in the returned (a,r) tuple 
    @staticmethod
    def get_unification_proof(c1 : list[int], c2 : list[int], auts_as_cycles : list[list[tuple]], num_clrs : int) -> tuple[list[tuple],tuple] | None: # -> (automorphism, relabeling) or None
        for aut in auts_as_cycles:
            res_relabel = Comp.try_unify_by_aut(c1,c2,aut,num_clrs)
            if res_relabel is not None:
                return aut,res_relabel
        return None

    # returns a dictionary where keys are the representative colorings and the values are lists of colorings that are relaut eqivalent to it
    @staticmethod
    def get_classified_by_relaut_eqiv_class(clrings : list[list[int]], g : Graph, num_clrs : int, verbose = False, log_index : int = 0, size_seq = None) -> dict[tuple[int,...],list[list[int]]]:
        if verbose:
            log_file = open(f"ZClassLogs/log{log_index}.txt","w")
            print(f"{size_seq}",file=log_file)
            classified : dict[tuple,list[list[int]]] = {} 
            auts_as_cycles = [a.cycle_tuples(singletons=True) for a in g.automorphism_group()]
            for i,c_curr in enumerate(clrings):
                if i % 10 == 0:
                    print(f"representants:{len(classified):<10}step:{i:<10}",file=log_file)
                    log_file.flush()
                for c_repr in classified.keys():
                    uni_proof = Comp.get_unification_proof(c_curr,list(c_repr),auts_as_cycles,num_clrs)
                    if uni_proof is None: # the coloring is not automorph+relabel equivalent to the c_repr representant
                        continue
                    else:
                        classified[c_repr].append(c_curr)
                        break # we don't want to check for more ways to transform this coloring to the same representant
                else : # there was no representant to which we can rel+automorph
                    hashable_curr = tuple(c_curr)
                    classified[hashable_curr] = [c_curr] # set this coloring as a representant
            print("DONE",file=log_file)
            log_file.close()
            return classified
        else:
            classified : dict[tuple,list[list[int]]] = {} 
            auts_as_cycles = [a.cycle_tuples(singletons=True) for a in g.automorphism_group()]
            for c_curr in clrings:
                for c_repr in classified.keys():
                    uni_proof = Comp.get_unification_proof(c_curr,list(c_repr),auts_as_cycles,num_clrs)
                    if uni_proof is None: # the coloring is not automorph+relabel equivalent to the c_repr representant
                        continue
                    else:
                        classified[c_repr].append(c_curr)
                        break # we don't want to check for more ways to transform this coloring to the same representant
                else : # there was no representant to which we can rel+automorph
                    hashable_curr = tuple(c_curr)
                    classified[hashable_curr] = [c_curr] # set this coloring as a representant

            return classified

    # to be used by the thread pool
    @staticmethod
    def process_item(item):
        size_seq, colorings, i, graph, num_clr, verbose = item
        reprs = list(Comp.get_classified_by_relaut_eqiv_class(colorings,graph,num_clr,verbose=verbose,log_index=i,size_seq=size_seq).keys())
        return size_seq,reprs

class Classify:

    @staticmethod
    def classify_by_size_seq(standardized : list[tuple[list[int],tuple[int,...]]]):
        classified : dict[tuple[int,...],list[list[int]]] = {}
        for (clring,size_seq) in standardized:
            if size_seq not in classified:
                classified[size_seq] = []
            classified[size_seq].append(clring)
        return classified

    @staticmethod
    def get_representants_by_sizes(graph : Graph, num_clr : int, classified : dict[tuple[int,...],list[list[int]]], verbose = False) -> dict[tuple[int,...],list[tuple[int,...]]]:
        reprs : dict[tuple[int,...],list[tuple[int,...]]] = {}
        i = 0
        for (size_seq,colorings) in zip(classified.keys(),classified.values()):
            reprs[size_seq] = list(Comp.get_classified_by_relaut_eqiv_class(colorings,graph,num_clr,verbose=verbose,log_index=i).keys())
            i += 1
        return reprs

class Partitions:

    @staticmethod
    def get_vtx_set_partitions(graph : Graph, num_clrs : int) -> list[list[list[int]]]:
        vtces = graph.vertices()
        sage_partitions = SetPartitions(vtces,num_clrs)
        partitions = []
        for sage_partition in sage_partitions:
            partition = []
            for sage_part in sage_partition:
                part = [] 
                for vtx in sage_part:
                    part.append(vtx)
                partition.append(part)
            partitions.append(partition)
        
        return partitions

    # tests whether all parts of the partition are independent sets
    @staticmethod
    def is_partition_into_indepsets(partition : list[list[int]], graph : Graph) -> bool:
        for part in partition:
            if not graph.is_independent_set(part):
                return False
        return True

    @staticmethod
    def partition_to_clring_as_list(partition : list[list[int]], graph : Graph) -> list[int]:
        clring = len(graph.vertices()) * [0]
        for i,part in enumerate(partition):
            for vtx in part:
                clring[vtx] = i
        return clring


class Strategies:
    # computes the number of equivalence classes of the relabeling-automorphism relation for given graph and given number of colors
    @staticmethod
    def compute_using_set_partitions(graph : Graph, num_clrs : int, verbose : bool = False) -> int:
        if verbose:
            partitions = Partitions.get_vtx_set_partitions(graph,num_clrs)
            print(f"{len(partitions)}")
            indep_partitions = list(filter(lambda p : Partitions.is_partition_into_indepsets(p,graph),partitions))
            print(f"{len(indep_partitions)}")
            clrings = list(map(lambda p : Partitions.partition_to_clring_as_list(p,graph),indep_partitions))
            fingerprinteds = Fprint.get_fprnted_clrings(clrings)

            standardized = Fprint.get_standardized(fingerprinteds)

            classified = Classify.classify_by_size_seq(standardized)

            pool = mp.Pool(mp.cpu_count()) # creates a new pool with 8 workers (since I have 8 cores)
            items = []
            for i,(size_seq,coloring) in enumerate(zip(classified.keys(),classified.values())):
                items.append((size_seq,coloring,i,graph, num_clrs, verbose))
            results = pool.map(Comp.process_item,items)
            pool.close() # tells the pool that we will not be submitting any more processes
            pool.join() # tells the pool to wait at this point of the program until all jobs are done
            reprs = {}
            for (size_seq,colorings) in results:
                reprs[size_seq] = colorings
            res = sum([len(colorings) for colorings in reprs.values()])
            return res
            
        else:
            raise NotImplementedError



# SOLID SETTINGS
SOLID_NAME = "petersen"
NUM_CLRS = 10

# GRAPH DATA
# G = Graph(sdp.get_all_solids_dict()[SOLID_NAME][sdp.JSON_EDGES])
G = graphs.PetersenGraph()

# because of the multiprocessing we have to use the if __name__ == "__main__" construct
if __name__ == "__main__":

    file = open("output.txt","w")
    
    num_classes,time = tmng.run_and_get_time(Strategies.compute_using_set_partitions,G,NUM_CLRS,verbose=True)
    print(f"{"INPUT":-^20}",file=file)
    print(f"{SOLID_NAME=}",file=file)
    print(f"{NUM_CLRS=}",file=file)
    print()
    print(f"{"OUTPUT":-^20}",file=file)
    print(f"{num_classes=}",file=file)
    print(f"{time=:.3}",file=file)

    file.close()

