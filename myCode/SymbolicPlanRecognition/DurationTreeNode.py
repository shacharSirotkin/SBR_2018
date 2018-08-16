import sys

from TreeNode import TreeNode


class DurationTreeNode(TreeNode):
    def __init__(self, ID, label, min_duration=1, max_duration=sys.maxint, parent=None, children=None, is_root=False,
                 is_complete=False, tags=None, seq_of=None, seq=None):
        self._min_duration = min_duration
        self._max_duration = max_duration
        self._soft_tags = []
        TreeNode.__init__(self, ID, label, parent, children, is_root, is_complete, tags, seq_of, seq)

    def soft_tag(self,t):
        self._soft_tags.append(t)

    def soft_tagged(self, t):
            return t in self._soft_tags

    def delete_tag(self, t):
        if t in self.get_tags():
            self._tags.remove(t)
        else:
            self._soft_tags.remove(t)

    def get_min_duration(self):
        return self._min_duration

    def get_max_duration(self):
        return self._max_duration