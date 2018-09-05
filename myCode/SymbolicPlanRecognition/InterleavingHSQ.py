import itertools
import networkx as nx

from SymbolicPlanRecognition.HSQ import HSQ


class InterleavingHSQ(HSQ):
    def __init__(self):
        HSQ.__init__(self)

    def get_all_paths(self, map_of_paths):
        all_paths = HSQ.get_all_paths(self, map_of_paths)
        interrupts = self._find_interrupting_behavior(all_paths)
        self._check_interleaving(interrupts)
        return all_paths

    def _find_interrupting_behavior(self, all_paths):
        all_paths_ends = [path[0] for path in all_paths]
        suspected_paths = set([])
        for path_end in all_paths_ends:
            suspected_paths.update([nx_node for nx_node in self.graph.nodes
                                    if not nx.has_path(self.graph, path_end, nx_node)])
        suspected_nodes = {suspected_path: self.path_by_string[suspected_path] for suspected_path in suspected_paths}
        suspected_starts = {suspected_path: suspected_node for suspected_path, suspected_node
                            in suspected_nodes.iteritems() if self.is_first_child(suspected_node)}
        interrupts = []
        for path1 in suspected_nodes.keys():
            for path2 in suspected_starts.keys():
                try:
                    for path in nx.all_simple_paths(self.graph, source=path1, target=path2):
                        interrupts.append(path)
                except nx.exception.NodeNotFound:
                    pass
        interrupts.extend([[key] for key in suspected_starts.keys()])
        return interrupts

    def _check_interleaving(self, interrupts):
        for interrupt in interrupts:
            tags = [path[path.rfind(' '):] for path in interrupt]
            interrupted_graph = self.graph.copy()
            nodes_to_remove = [node for node in self.graph.nodes if node[node.rfind(' '):] in tags]
            interrupted_graph.remove_nodes_from(nodes_to_remove)
            leaving_tag = str(min(map(int, tags)) - 1)
            return_tag = str(max(map(int, tags)) + 1)
            left_nodes = [node for node in self.graph.nodes if node[node.rfind(' ') + 1:] == leaving_tag]
            left_nodes = {from_node: self.path_by_string[from_node] for from_node in left_nodes}
            return_to_nodes = [node for node in self.graph.nodes if node[node.rfind(' ') + 1:] == return_tag]
            return_to_nodes = {to_node: self.path_by_string[to_node] for to_node in return_to_nodes}
            edges_to_add = []
            for leaving_node, return_node in itertools.product(left_nodes.iteritems(), return_to_nodes.iteritems()):
                is_first_child = self.is_first_child(return_node[1])
                # depth_of_seq = self._check_interleaved_nodes(leaving_node[1], int(leaving_tag), return_node[1],
                #                                              int(return_tag))
                # The depth where there is a node of the given path which is a prev_seq of node in this path
                depth_of_seq = leaving_node[1].get_seq_child_depth(return_node[1])
                # indicate whether there is a node of the given path which is a prev_seq of node in this path
                has_seq_child = (depth_of_seq != -1)
                # if path1 has no previous sequentials or there is sequential connection between the paths
                # create nodes and edge between them in the directed graph g
                if is_first_child or has_seq_child:
                    edges_to_add.append((leaving_node[0], return_node[0]))

    def _check_interleaved_nodes(self,leaved_node, leaved_tag, return_to_node, return_to_tag):
        last_leaved = leaved_node.get_last()
        last_return = return_to_node.get_last()
        return False