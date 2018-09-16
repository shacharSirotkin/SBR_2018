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

    # return The depth where there is a sequential connection from node in this path to node in the given path
    def get_seq_to_next_depth(self, next_path):
        # if the paths are the same, saying that there is a sequential edge between them will be a vacuous truth
        if self == next_path:
            return 0
        # get all nodes in both paths
        next_nodes = next_path.search()
        current_nodes = self.search()

        connection_node = None

        # look for node from path1 and path2 which have a sequential edge from one to the other
        # if two nodes was found connection_node would be the node which the sequential edge come from
        for next_node in next_nodes:
            for current_node in current_nodes:
                if next_node.get_ID() in current_node.get_next_seqs():
                    connection_node = current_node
                    break

        depth = -1

        check_path = self

        # find the depth of connection_node in check_path(which is actually self)
        if connection_node is not None:
            while check_path != connection_node:
                depth += 1
                check_path = check_path.get_child()

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

    def __hash__(self):
        return hash(self.__repr__())
