from DurationTreeNode import DurationTreeNode
from TreeNode import TreeNode


def create_tree_node(ID, label, parent=None, children=None, is_root=False,
                     is_complete=False, tags=None, seq_of=None, seq=None):
    return TreeNode(ID, label, parent, children, is_root, is_complete, tags, seq_of, seq)


def create_duration_tree_node(ID, label, min_duration=1, max_duration=1, parent=None, children=None,
                              is_root=False, is_complete=False, tags=None, seq_of=None, seq=None):
    return DurationTreeNode(ID, label, min_duration, max_duration, parent,
                    children, is_root, is_complete, tags, seq_of, seq)
