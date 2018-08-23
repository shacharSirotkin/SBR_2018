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
        self._parser = Parser(NodeFactory.create_duration_node)
        self._root = self.parse(domain_file)
        # get list of any node in the plan library
        self._plans = self._root.search()
        self._matcher = Matcher(self._root)
        self._tags = []

    def apply_hsq(self):
        # for each tag create path from obs to root
        map_of_paths = self._hsq.generate_paths_map(self._root, self._tags)
        # apply hsq on the optional paths
        return self._hsq.apply_hsq(map_of_paths)

    def apply_csq(self, current_optional_obs, t):
        self._tags.append(t)
        self._previous_tagged_nodes = self._csq.apply_csq(current_optional_obs, t, self._previous_tagged_nodes)
        return self._previous_tagged_nodes

    def parse(self, domain_file):
        return self._parser.parse(domain_file)

    def match(self, observation):
        return self._matcher.match(observation)