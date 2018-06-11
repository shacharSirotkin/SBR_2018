import sys
import networkx as nx

path_string_to_path_plan = {}


class HSQ(object):
    def apply_hsq(self, map_of_paths):
        G = nx.DiGraph()
        # create directed graph according to tags in each time-stamp
        for i in xrange(len(map_of_paths), 1, -1):
            for path1 in map_of_paths[i]:
                is_first_child = self.is_first_child(path1)
                for path2 in map_of_paths[i - 1]:
                    depth_of_seq = path2.get_seq_child_depth(path1)
                    has_seq_child = (depth_of_seq != -1)
                    # if path1 has no previous sequentials or there is sequential connection between the paths and
                    # there is no deeper node in path2 that has next sequential and has child,
                    # create nodes and edge between them in the directed graph g
                    if is_first_child or (has_seq_child and self.all_deeper_completed(path2, depth_of_seq + 2)):
                        self.generate_edge(G, path1, path2, i)
        # return all simple paths in the graph from node with last time-stamp to node with time-stamp 1
        all_paths = self.get_all_paths(map_of_paths, G)
        return all_paths

    # create nodes and edge between them in the directed graph g
    def generate_edge(self, g, path1, path2, i):
        root_node1 = path1
        root_node2 = path2
        g.add_node(str(root_node1) + " " + str(i))
        g.add_node(str(root_node2) + " " + str(i - 1))
        g.add_edge(str(root_node1) + " " + str(i), str(root_node2) + " " + str(i - 1))
        path_string_to_path_plan[str(root_node1) + " " + str(i)] = root_node1
        path_string_to_path_plan[str(root_node2) + " " + str(i - 1)] = root_node2

    # return whether there is no nodes deeper than the sequential connection between the paths that
    # has next sequential and has child
    def all_deeper_completed(self, path, j):
        path_nodes = path.search()
        i = j
        while i < len(path_nodes):
            # if node has next sequential and has child
            if (not path_nodes[i].get_is_complete()) and (path_nodes[i].get_child() is not None):
                return False
            i += 1
        return True

    def get_all_paths(self, map_of_paths, g):
        all_paths = []
        for path1 in map_of_paths[len(map_of_paths)]:
            for path2 in map_of_paths[1]:
                try:
                    for path in nx.all_simple_paths(g, source=str(path1) + " " + str(len(map_of_paths)),
                                                    target=str(path2) + " " + str(1)):
                        all_paths.append(path)
                except nx.exception.NodeNotFound:
                    pass
        return all_paths

    # return whether the path contain only 'first child's from root til the tagged node
    def is_first_child(self, path1):
        search = path1.search()
        for child1 in search:
            if child1.get_seq_of():
                return False
        return True
