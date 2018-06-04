def self_cycle_is_consistent(w, all_tagged_previous_stage, t):
    if w.tagged(t - 1) or w.previous_seq_edge_tagged(all_tagged_previous_stage) or w.is_first():
        return True
    else:
        return False


def no_self_cycle_is_consistent(w, all_tagged_previous_stage, t):
    if w.previous_seq_edge_tagged(all_tagged_previous_stage) or w.is_first():
        return True
    else:
        return False


def interleaved_is_consistent(w, all_tagged_previous_stage, t):
    if w.tagged(t - 1) or w.is_first() or w.previous_seq_edge_tagged(all_tagged_previous_stage) or\
            w.is_previous_seq_tagged(w.get_last_leaved_node):
        return True
    else:
        return False
