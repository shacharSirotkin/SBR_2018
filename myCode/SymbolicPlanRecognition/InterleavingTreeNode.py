from TreeNode import TreeNode


class InterleavingTreeNode(TreeNode):

    def __init__(self, ID, label, parent=None, children=None, is_root=False,
                 is_complete=False, tags=None, seq_of=None, seq=None):
        self._last_leaved_node_id = -1
        self._first_sequential = None
        TreeNode.__init__(ID, label, parent, children, is_root, is_complete, tags, seq_of, seq)

    def set_last_leaved_nodes(self, last_leaved_id):
        self._last_leaved_node_id = last_leaved_id

    def set_first_sequential(self, first):
        self._first_sequential = first

    def get_first_sequential(self):
        if not self._first_sequential:
            return self
        else:
            return self._first_sequential.get_first_sequential()

    def get_last_leaved_node(self):
        if self.is_first():
            return self._last_leaved_node_id
        else:
            return self._first_sequential.get_last_leaved_node