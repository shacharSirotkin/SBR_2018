import networkx as nx

from SymbolicPlanRecognition.PathNode import PathNode


class HSQ(object):
    def __init__(self):
        self.path_by_string = {}
        self.graph = nx.DiGraph()

    def apply_hsq(self, map_of_paths):
        # create directed graph of paths according to tags in each time-stamp
        for i in xrange(len(map_of_paths), 1, -1):
            for current_path in map_of_paths[i]:
                # indicates whether the path contain only 'first child's from root til the tagged node
                is_first_child = self.is_first_child(current_path)
                for previous_path in map_of_paths[i - 1]:
                    # The depth where there is a sequential connection from node in previous_path
                    # to node in current_path
                    depth_of_seq = previous_path.get_seq_to_next_depth(current_path)
                    # indicate whether there is a node of the given path which is a prev_seq of node in this path
                    has_seq_child = (depth_of_seq != -1)
                    # if current_path has no previous sequentials or there is sequential connection
                    # between the paths, create nodes and edge between them in the directed graph g
                    if is_first_child or has_seq_child:
                        self.generate_edge(current_path, previous_path, i)
        # return all simple paths in the graph from node with last time-stamp to node with time-stamp 1
        all_paths = self.get_all_paths(map_of_paths)
        return all_paths

    # create nodes and edge between them in the directed graph g
    def generate_edge(self, path1, path2, i):
        root_node1 = path1
        root_node2 = path2
        self.graph.add_node(str(root_node1) + " " + str(i))
        self.graph.add_node(str(root_node2) + " " + str(i - 1))
        self.graph.add_edge(str(root_node1) + " " + str(i), str(root_node2) + " " + str(i - 1))
        self.path_by_string[str(root_node1) + " " + str(i)] = root_node1
        self.path_by_string[str(root_node2) + " " + str(i - 1)] = root_node2

    # Find all simple paths from pathNodes in last tag to a pathNodes in first tag
    # In another words, return every possible explanation to behavior that have been observed
    def get_all_paths(self, map_of_paths):
        all_paths = []
        for end_path in map_of_paths[len(map_of_paths)]:
            for start_path in map_of_paths[1]:
                try:
                    for path in nx.all_simple_paths(self.graph, source=str(end_path) + " " + str(len(map_of_paths)),
                                                    target=str(start_path) + " " + str(1)):
                        all_paths.append(path)
                except nx.exception.NodeNotFound:
                    pass
        return all_paths

    # return whether the path contain only 'first child's from root til the tagged node
    def is_first_child(self, path1):
        search = path1.search()
        for child1 in search:
            if child1.get_prev_seqs():
                return False
        return True

    # create map from time-stamps to paths by running over from each tagged leaf to the root
    def generate_paths_map(self, root, tags):
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
