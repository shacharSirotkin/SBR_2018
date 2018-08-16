from SymbolicPlanRecognition import NodeFactory
from SymbolicPlanRecognition.CSQ import CSQ
from SymbolicPlanRecognition.HSQ import HSQ
from SymbolicPlanRecognition.Matcher import Matcher
from SymbolicPlanRecognition.Parser_2 import Parser
from SymbolicPlanRecognition.PathNode import PathNode
from SymbolicPlanRecognition.TagManagers import DurationTagManager, BasicTagManager


class SymbolicPlanRecognition(object):
    def __init__(self, domain_file, duration=True, self_cycle=True, interleaving=False):
        # TODO: dill with interrupt
        if not duration:
            tag_manager = BasicTagManager(self_cycle, interleaving)
        else:
            tag_manager = DurationTagManager(interleaving)
        self._csq = CSQ(tag_manager)
        self._hsq = HSQ()
        self._previous_tagged_nodes = []
        self._parser = Parser(NodeFactory.create_node)
        self._root = self.parse(domain_file)
        # get list of any node in the plan library
        self._plans = self._root.search()
        self._matcher = Matcher(self._root)
        self._all_tags = []

    def apply_hsq(self):
        # for each tag create path from obs to root
        map_of_paths = self._generate_paths_map()
        # apply hsq on the optional paths
        return self._hsq.apply_hsq(map_of_paths)

    def apply_csq(self, current_optional_obs, t):
        self._all_tags.append(t)
        self._previous_tagged_nodes = self._csq.apply_csq(current_optional_obs, t, self._previous_tagged_nodes)
        return self._previous_tagged_nodes

    # create map from time-stamps to paths of each tagged node to the root
    def _generate_paths_map(self):
        map_of_paths = {}
        for tag in self._all_tags:
            for child in self._root.get_children():
                if child.tagged(tag):
                    leaves = child.get_leaves()
                    paths = self._make_paths(leaves, tag)
                    if tag in map_of_paths.keys():
                        map_of_paths[tag].extend(paths)
                    else:
                        paths_to_put = paths
                        map_of_paths[tag] = paths_to_put
        print map_of_paths
        return map_of_paths

    def _make_paths(self, leaves, tag):
        paths = []
        for p in leaves:
            new_parent = None
            if p.tagged(tag):
                new_node = PathNode(p)
                while p.parent() is not None:
                    new_parent = PathNode(p.parent())
                    # if node has no next sequential nodes mark it as complete
                    if not new_node.get_next_seqs():
                        new_node.set_complete(True)
                    new_node.set_parent(new_parent)
                    p = p.parent()
                    new_node = new_parent
            if new_parent is not None:
                paths.append(new_parent)
        return paths

    def parse(self, domain_file):
        return self._parser.parse(domain_file)

    def match(self, observation):
        return self._matcher.match(observation)