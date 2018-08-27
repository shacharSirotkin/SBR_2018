class Node(object):
    def __init__(self, ID, label, is_root, tags, seq_of, seq):
        self._label = label
        self._is_root = is_root
        self._id = ID
        self._tags = tags
        self._prev_seqs = seq_of
        self._next_seqs = seq

    def root(self):
        return self._is_root

    def tag(self, time_stamp):
        self._tags.append(time_stamp)

    def delete_tag(self, time_stamp):
        self._tags.remove(time_stamp)

    def tagged(self, time_stamp):
        return time_stamp in self._tags

    def is_first(self):
        return self._prev_seqs == []

    def add_seq_of(self, ID, p):
        self._prev_seqs.append(ID)
        p.get_next_seqs().append(self.get_ID())

    def get_label(self):
        return self._label

    def set_root(self, is_root):
        self._is_root = is_root

    def get_next_seqs(self):
        return self._next_seqs

    def get_prev_seqs(self):
        return self._prev_seqs

    def get_tags(self):
        return self._tags

    def get_ID(self):
        return self._id

    def set_ID(self, ID):
        self._id = ID

    def get_is_root(self):
        return self._is_root
