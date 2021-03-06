from CSQ import CSQ
from HSQ import HSQ
from BasicMatcher import BasicMatcher
from Parser import Parser
from SymbolicPlanRecognition.InterleavingHSQ import InterleavingHSQ
from TagManagers import DurationTagManager, BasicTagManager, InterleavingTagManager
from SequentialsParser import read_interleaving_order_cons, read_order_cons
from NodeFactory import create_tree_node, create_duration_node, create_interleaving_tree_node


# Note: I did not test running with Duration and Interleaving together
class SymbolicPlanRecognition(object):
    def __init__(self, duration=False, self_cycle=True, interleaving=False):
        # TODO: dill with interrupt
        if not duration:
            if not interleaving:
                cons_reader = read_order_cons
                node_creator = create_tree_node
                tag_manager = BasicTagManager(self_cycle)
            else:
                cons_reader = read_interleaving_order_cons
                node_creator = create_interleaving_tree_node
                tag_manager = InterleavingTagManager(self_cycle)
        else:
            cons_reader = read_order_cons
            node_creator = create_duration_node
            tag_manager = DurationTagManager(interleaving)
        if interleaving:
            self._hsq = InterleavingHSQ()
        else:
            self._hsq = HSQ()
        self._csq = CSQ(tag_manager)
        self._previous_tagged_nodes = []
        self._parser = Parser(node_creator, cons_reader)
        self._tags = []
        self._root = None
        self._plans = None
        self._matcher = None

    def set_domain(self, domain_file):
        self._root = self._parse(domain_file)
        # get list of any node in the plan library
        self._plans = self._root.search()
        self._matcher = BasicMatcher(self._root)
        self._tags = []
        self._hsq.reset()

    def apply_hsq(self):
        if not self._root:
            raise Exception('Domain does not exist')
        # for each tag create path from obs to root
        map_of_paths = self._hsq.generate_paths_map(self._root, self._tags)
        # apply hsq on the optional paths
        return self._hsq.apply_hsq(map_of_paths)

    def apply_csq(self, current_optional_obs, t):
        if not self._root:
            raise Exception('Domain does not exist')
        self._tags.append(t)
        self._previous_tagged_nodes = self._csq.apply_csq(current_optional_obs, t, self._previous_tagged_nodes)
        return self._previous_tagged_nodes

    def _parse(self, domain_file):
        return self._parser.parse(domain_file)

    def match(self, observation):
        if not self._root:
            raise Exception('Domain does not exist')
        return self._matcher.match(observation)
