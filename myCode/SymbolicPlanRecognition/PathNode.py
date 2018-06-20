from Node import Node


class PathNode(Node):
    def __init__(self, tree_node):
        self._parent = None
        self._child = None
        Node.__init__(self, tree_node._id, tree_node._label, tree_node._is_root, is_complete=False,
                      tags=list(tree_node._tags), seq_of=list(tree_node._prev_seqs), seq=list(tree_node._next_seqs))

    def set_parent(self, parent):
        self._parent = parent
        parent._child = self

    def get_child(self):
        return self._child

    def search(self):
        lst = [self]
        if self._child is not None:
            lst.extend(self._child.search())
        return lst

    # return the depth where there is a node of the given path which is a prev_seq of node in this path
    def get_seq_child_depth(self, another_path):
        # get all nodes in both paths
        path1_nodes = another_path.search()
        path2_nodes = self.search()

        p = None

        for node1 in path1_nodes:
            for node2 in path2_nodes:
                if node2._id in node1._prev_seqs:
                    p = node2
                    break

        level = -1

        p_check = self

        if p is not None:
            while p_check != p:
                level += 1
                p_check = p_check._child

        return level

    def __repr__(self):
        res = self._label
        res += "\n"
        if self._child is not None:
                res += self._child.to_string("    ")
        return res

    def to_string(self, init):
        res = init + self._label
        res += "\n"
        if self._child is not None:
            res += self._child.to_string(init + "    ")
        return res

    def __eq__(self, other):
        return other.__repr__() == self.__repr__()