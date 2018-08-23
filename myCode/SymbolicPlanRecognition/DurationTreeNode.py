import sys

from TreeNode import TreeNode


class DurationTreeNode(TreeNode):
    def __init__(self, ID, label, min_duration=1, max_duration=sys.maxint, parent=None, children=None, is_root=False,
                 is_complete=False, tags=None, seq_of=None, seq=None):
        self._min_duration = min_duration
        self._max_duration = max_duration
        self._soft_tags = []
        TreeNode.__init__(self, ID, label, parent, children, is_root, is_complete, tags, seq_of, seq)

    def soft_tag(self, time_stamp):
        self._soft_tags.append(time_stamp)

    def soft_tagged(self, time_stamp):
            return time_stamp in self._soft_tags

    def delete_tag(self, time_stamp):
        if time_stamp in self.get_tags():
            self._soft_tags.remove(time_stamp)
            self._tags.remove(time_stamp)
        else:
            self._soft_tags.remove(time_stamp)

    def get_min_duration(self):
        return self._min_duration

    def get_max_duration(self):
        return self._max_duration

    def tag_retroactively(self,time_stamp):
        in_range = False
        for time in xrange(time_stamp - 1, 1, -1):
            if time in self._soft_tags and time not in self._tags:
                self.tag(time)
                in_range = True
            elif in_range:
                break
