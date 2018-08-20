import SymbolicPlanRecognition.IsConsistent as isConsistent


class BasicTagManager(object):
    def __init__(self, self_cycle=False, interleaving=False):
        if not self_cycle:
            if interleaving:
                self._is_consistent = isConsistent.interleaved
            else:
                self._is_consistent = isConsistent.basic
        elif interleaving:
            self._is_consistent = isConsistent.self_cycle_interleaved
        else:
            self._is_consistent = isConsistent.self_cycle

    def manage_tag(self, node, time_stamp, all_tagged_previous_stage, all_tagged_this_stage, tagged):
        if self._is_consistent(node, all_tagged_previous_stage, time_stamp):
            node.tag(time_stamp)
            all_tagged_this_stage.append(node)
            tagged.append(node)
            return node.parent(), True
        else:
            return None, False


class DurationTagManager(object):
    def __init__(self, interleaving=False):
        if not interleaving:
            self._is_consistent = isConsistent.duration
        else:
            self._is_consistent = isConsistent.self_cycle_interleaved

    def manage_tag(self, node, time_stamp, all_tagged_previous_stage, all_tagged_this_stage, tagged):
        if node.soft_tagged(time_stamp):
            return node.parent(), True
        duration = self._calc_duration(node, time_stamp)
        if duration <= node.get_max_duration():
            if self._is_consistent(node, all_tagged_previous_stage, time_stamp):
                if duration < node.get_min_duration():
                    node.soft_tag(time_stamp)
                    if duration + 1 == node.get_min_duration():
                        node.tag(time_stamp)
                else:
                    node.tag(time_stamp)
                all_tagged_this_stage.append(node)
                tagged.append(node)
                return node.parent(), True
            else:
                return None, False
        else:
            return None, False

    def _calc_duration(self, node, time_stamp):
        duration = 0
        time = time_stamp
        while time > 0:
            if node.soft_tagged(time - 1):
                duration += 1
                time -= 1
            else:
                break
        return duration


class InterleavingTagManager(object):
    def __init__(self, self_cycle):
        if not self_cycle:
            self._is_consistent = isConsistent.interleaved
        else:
            self._is_consistent = isConsistent.self_cycle_interleaved

    def manage_tag(self, node, time_stamp, all_tagged_previous_stage, all_tagged_this_stage, tagged):
        if self._is_consistent(node, all_tagged_previous_stage, time_stamp):
            node.tag(time_stamp)
            node.set_last_leaved_node(node._id)
            all_tagged_this_stage.append(node)
            tagged.append(node)
            return node.parent(), True
        else:
            return None, False
