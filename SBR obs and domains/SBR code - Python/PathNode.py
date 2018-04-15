import Node

class PathNode(Node.Node):

    def __init__(self, tree_node):
        self._parent = None
        self._child = None
        Node.Node.__init__(self, tree_node._id, tree_node._label, tree_node._is_root, is_complete=False, tags=list(tree_node._tags), seq_of=list(tree_node._seq_of), seq=list(tree_node._seq))

    def set_parent(self, parent):
        self._parent = parent
        parent._child = self

    def get_child(self):
        return self._child

    def search(self):
        lst = []
        lst.append(self)
        if self._child != None:
            lst.extend(self._child.search())
        return lst

    def __repr__(self):
        res = self._label
        res += "\n"
        if self._child != None:
                res += self._child.to_string("    ")
        return res

    def to_string(self, init):
        res = init + self._label
        res +="\n"
        if self._child != None:
            res += self._child.to_string(init + "    ")
        return res

    def has_seq_child(self, child_of_root_1):
        child_of_root_2 = self
        root2 = child_of_root_2
        root1 = child_of_root_1
        children_of_root1 = root1.search()
        children_of_root2 = root2.search()

        p = None

        for child1 in children_of_root1:
            for child2 in children_of_root2:
                if child2._id in child1._seq_of:
                    p = child2
                    break

        level = -1

        pCheck = root2

        if p != None:
            while pCheck != p:
                level += 1
                pCheck = pCheck._child

        return level

    def __eq__(self, other):
        return other.__repr__() == self.__repr__()