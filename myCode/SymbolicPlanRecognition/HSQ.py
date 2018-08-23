import networkx as nx

from SymbolicPlanRecognition.PathNode import PathNode

path_string_to_path_plan = {}


class HSQ(object):
    def apply_hsq(self, map_of_paths):
        # TODO: duration doesn't work due to soft tags that the hsq doesnt "see"
        G = nx.DiGraph()
        # create directed graph of paths according to tags in each time-stamp
        for i in xrange(len(map_of_paths), 1, -1):
            for path1 in map_of_paths[i]:
                # indicates whether the path contain only 'first child's from root til the tagged node
                is_first_child = self.is_first_child(path1)
                for path2 in map_of_paths[i - 1]:
                    # The depth where there is a node of the given path which is a prev_seq of node in this path
                    depth_of_seq = path2.get_seq_child_depth(path1)
                    # indicate whether there is a node of the given path which is a prev_seq of node in this path
                    has_seq_child = (depth_of_seq != -1)
                    # if path1 has no previous sequentials or there is sequential connection between the paths
                    # create nodes and edge between them in the directed graph g
                    if is_first_child or has_seq_child:
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

    # Find all simple paths from pathNodes in last tag to a pathNodes in first tag
    # In another words, return every possible explanation to behavior that have been observed
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

# create map from time-stamps to paths from each tagged node to the root
    def generate_paths_map(self,root, tags):
        map_of_paths = {}
        for tag in tags:
            for child in root.get_children():
                if child.tagged(tag):
                    leaves = child.get_leaves()
                    paths = self._make_paths(leaves, tag)
                    if tag in map_of_paths.keys():
                        map_of_paths[tag].extend(paths)
                    else:
                        paths_to_put = paths
                        map_of_paths[tag] = paths_to_put
        miss_tags = [tag for tag in tags if tag not in map_of_paths.keys()]
        for tag in miss_tags:
            map_of_paths[tag] = []
        map_paths_string = map_of_paths.__repr__()
        map_paths_string = map_paths_string.replace('],', '],\n')
        print map_paths_string
        return map_of_paths

    # For each leaf that tagged with the current tag the function create a path of pathNodes from it to the root
    # Return a list of all relevant paths for this tag
    def _make_paths(self, leaves, tag):
        paths = []
        for p in leaves:
            new_parent = None
            if p.tagged(tag):
                new_node = PathNode(p)
                while p.parent() is not None:
                    new_parent = PathNode(p.parent())
                    new_node.set_parent(new_parent)
                    p = p.parent()
                    new_node = new_parent
            if new_parent is not None:
                paths.append(new_parent)
        return paths