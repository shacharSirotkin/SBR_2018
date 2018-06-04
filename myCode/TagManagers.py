class BasicTagManager(object):
    def __init__(self, is_consistent_func):
        self.is_consistent = is_consistent_func

    def manage_tag(self, node, time_stamp, all_tagged_previous_stage, all_tagged_this_stage, tagged):
        if self.is_consistent(node, all_tagged_previous_stage, time_stamp):
            node.tag(time_stamp)
            all_tagged_this_stage.append(node)
            tagged.append(node)
            return node.parent(), True
        else:
            return None, False


class DurationTagManager(object):
    def __init__(self, is_consistent_func):
        self.is_consistent = is_consistent_func

    def manage_tag(self, node, time_stamp, all_tagged_previous_stage, all_tagged_this_stage, tagged):
        duration = self._calc_duration(node,time_stamp)
        if duration <= node.get_max_duration():
            if self.is_consistent(node, all_tagged_previous_stage, time_stamp):
                if duration < node.get_min_duration():
                    node.soft_tag(time_stamp)
                else:
                    node.tag(time_stamp)
                all_tagged_this_stage.append(node)
                tagged.append(node)
                return node.parent(),True
            else:
                return None,False
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