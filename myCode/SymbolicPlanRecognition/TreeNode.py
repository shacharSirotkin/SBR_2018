from Node import Node
import copy


class TreeNode(Node):
    def __init__(self, ID, label, parent=None, children=None, is_root=False,
                 tags=None, seq_of=None, seq=None):
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
        Node.__init__(self, ID, label, is_root, tags, seq_of, seq)

    @staticmethod
    def get_from_path_node(path_node):
        label = path_node.get_label()
        tags = copy.deepcopy(path_node.get_tags())
        seq = path_node.get_next_seqs()
        seq_of = path_node.get_prev_seqs()
        is_root = path_node.root()
        newone = TreeNode(path_node.get_ID(), label, is_root=is_root, tags=tags, seq_of=seq_of, seq=seq)
        return newone

    def child_tagged(self, time_stamp):
        for d in self._children:
            if d.tagged(time_stamp):
                return True
        if not self._children:
            return True

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

    def previous_tagged(self, all_tagged_previous_stage):
        for p in all_tagged_previous_stage:
            if self.single_previous_tagged_by_ID(p.get_ID()):
                return True
        return False

    def parent(self):
        return self._parent

    def find_by_label(self, s):
        for p in self.search():
            if p.get_label() == s:
                return p
        return None

    def single_previous_tagged_by_ID(self, node_id):
        if node_id in self._prev_seqs:
            return True
        else:
            return False
