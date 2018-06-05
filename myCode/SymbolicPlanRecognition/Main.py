from SymbolicPlanRecognition.CSQ2 import CSQ
from SymbolicPlanRecognition.HSQ import HSQ
from SymbolicPlanRecognition.TagManagers import DurationTagManager, BasicTagManager


class SymbolicPlanRecognition(object):
    def __init__(self, duration=False, self_cycle=False, interleaving=False):
        if not duration:
            tag_manager = BasicTagManager(self_cycle, interleaving)
        else:
            tag_manager = DurationTagManager(interleaving)
        self._csq = CSQ(tag_manager)
        self._hsq = HSQ()
        self._previous_tagged_nodes = []

    def apply_one_csq(self, current_optional_obs, t):
        self._previous_tagged_nodes = self._csq.apply_csq(current_optional_obs,t,self._previous_tagged_nodes)
        return self._previous_tagged_nodes

    def apply_csq(self):
        pass