from DurationTreeNode import DurationTreeNode
from InterleavingTreeNode import InterleavingTreeNode
from TreeNode import TreeNode


def create_tree_node(ID, node_attributes):
    return TreeNode(ID, node_attributes.get("id"))


def create_duration_node(ID, node_attributes):
    if 'maxDuration' in node_attributes.keys():
        return DurationTreeNode(ID, node_attributes.get("id"), int(node_attributes.get("minDuration")),
                                int(node_attributes.get("maxDuration")))
    else:
        return DurationTreeNode(ID, node_attributes.get("id"))


def create_interleaving_tree_node(ID, node_attributes):
    return InterleavingTreeNode(ID, node_attributes.get("id"))

