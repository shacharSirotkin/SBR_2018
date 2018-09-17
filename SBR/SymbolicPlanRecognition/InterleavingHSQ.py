import itertools
import networkx as nx

from SymbolicPlanRecognition.HSQ import HSQ


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


class InterleavingHSQ(HSQ):
    def __init__(self):
        HSQ.__init__(self)

    def get_all_paths(self, map_of_paths):
        all_paths = HSQ.get_all_paths(self, map_of_paths)
        if all_paths:
            interrupts = self._find_interrupting_behavior(all_paths)
        else:
            interrupts = self._get_every_possible_interrupt(len(map_of_paths))
        interleaving_behaviors = self._check_interleavings(interrupts, map_of_paths)
        all_paths.extend(interleaving_behaviors)
        return all_paths

    def _find_interrupting_behavior(self, all_paths):
        interrupts = []
        suspected_paths = set([])
        all_paths_ends = [path[0] for path in all_paths]
        for path_end in all_paths_ends:
            suspected_paths.update([nx_node for nx_node in self.graph.nodes
                                    if not nx.has_path(self.graph, path_end, nx_node)])
        suspected_nodes = {suspected_path: self.path_by_string[suspected_path] for suspected_path
                           in suspected_paths}
        suspected_starts = {suspected_path: suspected_node for suspected_path, suspected_node
                            in suspected_nodes.iteritems() if self.is_first_child(suspected_node)}
        for path1 in suspected_nodes.keys():
            for path2 in suspected_starts.keys():
                try:
                    for path in nx.all_simple_paths(self.graph, source=path1, target=path2):
                        interrupts.append(path)
                except nx.exception.NodeNotFound:
                    pass
        interrupts.extend([[key] for key in suspected_starts.keys()])
        return interrupts

    def _get_every_possible_interrupt(self, tags_number):
        interrupts = []
        nodes_by_tag = {}
        for tag in xrange(2, tags_number):
            nodes = [node for node in self.graph.nodes if int(node[node.rfind(' ') + 1:]) == tag]
            nodes_by_tag[tag] = nodes
        for size in xrange(1, len(nodes_by_tag.keys())):
            for tag in xrange(2, tags_number - 1):
                if not tag + size in nodes_by_tag.keys():
                    break
                for_product = []
                for i in xrange(tag, tag + size + 1):
                    if i in nodes_by_tag.keys():
                        for_product.append(nodes_by_tag[i])
                products = map(list, list(itertools.product(*for_product)))
                interrupts.extend(products)
        inconsistent = []
        for interrupt in interrupts:
            for (current_node, next_node) in pairwise(interrupt):
                if not self.graph.has_edge(next_node, current_node):
                    inconsistent.append(interrupt)
                    break
        interrupts = [interrupt for interrupt in interrupts if interrupt not in inconsistent]
        interrupts.extend([key] for key in self.graph.nodes.keys())
        return interrupts

    def _check_interleavings(self, interrupts, paths_map):
        interleaving_behaviors = []
        for interrupt in interrupts:
            interrupted_behaviors = self._check_one_interleaving(interrupt, paths_map)
            if interrupted_behaviors:
                interleaving_behaviors.append([interrupted_behaviors, interrupt])
        return interleaving_behaviors

    def _check_one_interleaving(self, interrupt, paths_map):
        if len(interrupt) == 1:
            pass
        tags = [path[path.rfind(' '):] for path in interrupt]
        leaving_tag = str(min(map(int, tags)) - 1)
        return_tag = str(max(map(int, tags)) + 1)
        leaving_nodes = [node for node in self.graph.nodes if node[node.rfind(' ') + 1:] == leaving_tag]
        leaving_nodes = {from_node: self.path_by_string[from_node] for from_node in leaving_nodes}
        return_to_nodes = [node for node in self.graph.nodes if node[node.rfind(' ') + 1:] == return_tag]
        return_to_nodes = {to_node: self.path_by_string[to_node] for to_node in return_to_nodes}
        edges_to_add = []
        for leaving_node, return_node in itertools.product(leaving_nodes.iteritems(), return_to_nodes.iteritems()):
            if self.is_first_child(return_node[1]) or \
                    self._check_interleaved_nodes(leaving_node, return_node):
                edges_to_add.append((return_node[0], leaving_node[0]))
        nodes_to_remove = [node for node in self.graph.nodes if node[node.rfind(' '):] in tags]
        interrupted_graph = self.graph.copy()
        interrupted_graph.remove_nodes_from(nodes_to_remove)
        interrupted_graph.add_edges_from(edges_to_add)
        interrupted_behaviors = []
        for end_path in paths_map[len(paths_map)]:
            for start_path in paths_map[1]:
                try:
                    for path in nx.all_simple_paths(interrupted_graph,
                                                    source=str(end_path) + " " + str(len(paths_map)),
                                                    target=str(start_path) + " " + str(1)):
                        interrupted_behaviors.append(path)
                except nx.exception.NodeNotFound:
                    pass
        return interrupted_behaviors

    def _check_interleaved_nodes(self, leaved_node, return_to_node):
        depth_of_seq = leaved_node[1].get_seq_to_next_depth(return_to_node[1])
        if depth_of_seq == -1:
            return False
        previous_layer = [self.path_by_string[prev_node] for prev_node in self.graph.successors(return_to_node[0])]
        prev_layer_depths = [prev_node.get_seq_to_next_depth(return_to_node[1]) for prev_node in previous_layer]
        if prev_layer_depths:
            deepest_connection = max(prev_layer_depths)
            return depth_of_seq >= deepest_connection
        else:
            return depth_of_seq != -1
