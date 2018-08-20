import sys

from DurationTreeNode import DurationTreeNode
from InterleavingTreeNode import InterleavingTreeNode
from TreeNode import TreeNode


def create_duration_node(ID, node_attributes):
    if 'maxDuration' in node_attributes.keys():
        return DurationTreeNode(ID, node_attributes.get("id"), int(node_attributes.get("minDuration")),
                                         int(node_attributes.get("maxDuration")))
    else:
        return DurationTreeNode(ID, node_attributes.get("id"))


def create_tree_node(ID, node_attributes):
    return TreeNode(ID, node_attributes.get("id"))


def create_interleaving_tree_node(ID, label, parent=None, children=None,
                              is_root=False, is_complete=False, tags=None, seq_of=None, seq=None):
    return InterleavingTreeNode(ID, label, parent, children, is_root, is_complete, tags, seq_of, seq)
