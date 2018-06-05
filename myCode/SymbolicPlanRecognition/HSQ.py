import sys
import networkx as nx

sys.path.insert(0, 'c:/users/ranga/appdata/local/continuum/anaconda2/lib/site-packages')

path_string_to_path_plan = {}


class HSQ(object):
    def hsq(self, map_of_paths):
        G = nx.DiGraph()
        for i in xrange(len(map_of_paths), 1, -1):
            for path1 in map_of_paths[i]:
                is_first_child = self.if_is_first_child(path1)
                for path2 in map_of_paths[i - 1]:
                    level_of_seq = path2.has_seq_child(path1)
                    has_seq_child = (level_of_seq != -1)
                    if is_first_child or (has_seq_child and self.all_completed_from_level(path2, level_of_seq + 2)):
                        self.generate_edge(G, path1, path2, i)
        all_paths = self.get_all_paths(map_of_paths, G)
        return all_paths

    def generate_edge(self, g, path1, path2, i):
        root_node1 = path1
        root_node2 = path2
        g.add_node(str(root_node1) + " " + str(i))
        g.add_node(str(root_node2) + " " + str(i - 1))
        g.add_edge(str(root_node1) + " " + str(i), str(root_node2) + " " + str(i - 1))
        path_string_to_path_plan[str(root_node1) + " " + str(i)] = root_node1
        path_string_to_path_plan[str(root_node2) + " " + str(i - 1)] = root_node2

    def all_completed_from_level(self, path, j):
        path_children = path.search()
        i = j
        while i < len(path_children):
            if (not path_children[i].get_is_complete()) and (path_children[i].get_child() != None):
                return False
            i += 1
        return True

    def get_all_paths(self, map_of_paths, g):
        all_paths = []
        for path1 in map_of_paths[len(map_of_paths)]:
            for path2 in map_of_paths[1]:
                try:
                    for path in nx.all_simple_paths(g, source=str(path1) + " " + str(len(map_of_paths)), target=str(path2) + " " + str(1)):
                        all_paths.append(path)
                except nx.exception.NodeNotFound:
                    pass
        return all_paths

    def if_is_first_child(self, path1):
        is_first_child = True
        search = path1.search()
        for child1 in search:
            if child1.get_seq_of():
                is_first_child = False
                break
        return is_first_child
