from Node import Node


class PathNode(Node):
    def __init__(self, tree_node):
        self._parent = None
        self._child = None
        Node.__init__(self, tree_node.get_ID(), tree_node.get_label(), tree_node.get_is_root(),
                      tags=tree_node.get_tags(), seq_of=tree_node.get_prev_seqs(),
                      seq=tree_node.get_next_seqs())

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
        # if the paths are the same saying that there is a sequential edge between them will be a vacuous truth
        if self == another_path:
            return 0
        # get all nodes in both paths
        path1_nodes = another_path.search()
        path2_nodes = self.search()

        p = None

        # look for node from path1 and path2 which have a sequential edge from one to the other
        # if two nodes was found p would be the node which the sequential edge come from
        for node1 in path1_nodes:
            for node2 in path2_nodes:
                if node2._id in node1.get_prev_seqs():
                    p = node2
                    break

        depth = -1

        p_check = self

        # find the depth of p in path2(which is actually self)
        if p is not None:
            while p_check != p:
                depth += 1
                p_check = p_check.get_child()

        return depth

    def __repr__(self):
        res = self._label
        if self._child is not None:
                res += self._child.to_string(" ")
        return res

    def to_string(self, init):
        res = init + self._label
        if self._child is not None:
            res += self._child.to_string(init)
        return res

    def __eq__(self, other):
        return other.__repr__() == self.__repr__()
