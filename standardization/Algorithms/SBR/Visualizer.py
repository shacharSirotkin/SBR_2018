import networkx as nx
import copy
import pydot

id_counter = 0

def make_tree_graph(final_root, visualize_file_name):
    G = nx.DiGraph()
    for child in final_root.get_children():
        new_child = copy.deepcopy(child)
        new_child.set_ID(generate_ID())
        G.add_node(new_child.get_ID(), label = child.get_label())
        create_sub_trees(G, new_child)
    pydot_graph = nx.nx_pydot.to_pydot(G)
    pydot.Dot.write(pydot_graph,visualize_file_name, format="pdf")



def create_sub_trees(G, root):
    if root.get_children() != []:
        for child in root.get_children():
            new_child = copy.deepcopy(child)
            new_child.set_ID(generate_ID())
            G.add_node(new_child.get_ID(), label = child.get_label())
            G.add_edge(root.get_ID(), new_child.get_ID())
            create_sub_trees(G, new_child)

def generate_ID():
    global id_counter
    id_counter += 1
    return id_counter




