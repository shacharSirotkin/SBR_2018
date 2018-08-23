from Node import Node
import copy


class TreeNode(Node):
    def __init__(self, ID, label, parent=None, children=None, is_root=False,
                 is_complete=False, tags=None, seq_of=None, seq=None):
        self._self_cycle_limitation = None
        self._parent = parent
        if not children:
            self._children = []
        if not tags:
            tags = []
        if not seq_of:
            seq_of = []
        if not seq:
            seq = []
        Node.__init__(self, ID, label, is_root, is_complete, tags, seq_of, seq)

    @staticmethod
    def get_from_path_node(path_node):
        label = path_node.get_label()
        ID = path_node.get_ID()
        tags = copy.deepcopy(path_node.get_tags())
        seq = path_node.get_next_seqs()
        seq_of = path_node.get_seq_of()
        is_root = path_node.root()
        newone = TreeNode(ID, label, is_root=is_root, tags=tags, seq_of=seq_of, seq=seq)
        return newone

    def child_tagged(self, time_stamp):
        for d in self._children:
            if d.tagged(time_stamp):
                return True
        if not self._children:
            return True

    def set_parent(self, parent):
        self._parent = parent
        parent._children.append(self)

    def search(self):
        lst = [self]
        if self._children:
            for n in self._children:
                lst.extend(n.search())
        return lst

    def get_leaves(self):
        leaves = []
        for p in self.search():
            if not p._children:
                leaves.append(p)
        return leaves

    def get_children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)
        child._parent = self
        return child

    def __repr__(self):
        res = self._label
        res += "\n"
        if self._children:
            for child in self._children:
                res += child.to_string("    ")
        return res

    def to_string(self, init):
        res = init + self._label
        res += "\n"
        if self._children:
            for child in self._children:
                res += child.to_string(init + "    ")
        return res

    def first_child_of_node(self):
        return self._children[0]

    def is_not_leaf(self):
        return self._children != []

    def previous_seq_edge_tagged(self, all_tagged_previous_stage):
        for p in all_tagged_previous_stage:
            if p._id in self._prev_seqs:
                return True
        return False

    def parent(self):
        return self._parent

    def find_by_label(self, s):
        for p in self.search():
            if p._label == s:
                return p
        return None

    def set_self_cycle_limitation(self, self_cycle_limitation):
        self._self_cycle_limitation = self_cycle_limitation