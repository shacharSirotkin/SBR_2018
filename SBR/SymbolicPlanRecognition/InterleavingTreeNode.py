from TreeNode import TreeNode


class InterleavingTreeNode(TreeNode):

    def __init__(self, ID, label, parent=None, children=None, is_root=False,
                 tags=None, seq_of=None, seq=None):
        self._last_leaved_node_id = -1
        self._first_sequential = None
        TreeNode.__init__(self, ID, label, parent, children, is_root, tags, seq_of, seq)

    # save last_leaved_id as the last tagged node in this sequential chain
    def set_last_leaved_node(self, last_leaved_id):
        if not self._first_sequential:
            self._last_leaved_node_id = last_leaved_id
        else:
            self._first_sequential.set_last_leaved_node(last_leaved_id)

    # save the first node in chain
    def set_first_sequential(self, first):
        self._first_sequential = first

    # return the first node in chain
    def get_first_sequential(self):
        if not self._first_sequential:
            return self
        else:
            return self._first_sequential.get_first_sequential()

    # return the last tagged node in this chain
    def get_last_leaved_node(self):
        if self.is_first():
            return self._last_leaved_node_id
        else:
            return self._first_sequential.get_last_leaved_node()
