class Node(object):

    def __init__(self, ID ,label, is_root , is_complete, tags, seq_of, seq):
        self._label = label
        self._is_root = is_root
        self._id = ID
        self._is_complete = is_complete
        self._tags = tags
        self._seq_of = seq_of
        self._seq = seq

    def root(self):
        return self._is_root

    def tag(self, t):
        self._tags.append(t)

    def delete_tag(self, t):
        self._tags.remove(t)

    def tagged(self, t):
        return t in self._tags

    def no_seq_edges(self):
        return self._seq_of == []

    def add_seq_of(self, ID, p):
        self._seq_of.append(ID)
        p._seq.append(self._id)

    def get_label(self):
        return self._label

    def set_root(self, is_root):
        self._is_root = is_root

    def get_seq(self):
        return self._seq

    def get_seq_of(self):
        return self._seq_of

    def set_complete(self, complete):
        self._is_complete = complete

    def get_is_complete(self):
        return self._is_complete

    def get_tags(self):
        return self._tags

    def get_ID(self):
        return self._id

    def get_root(self):
        return self._is_root

    def set_ID(self, ID):
        self._id = ID