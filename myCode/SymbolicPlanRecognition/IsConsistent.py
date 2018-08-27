def basic(w, all_tagged_previous_stage, t):
    if w.previous_tagged(all_tagged_previous_stage) or w.is_first():
        return True
    else:
        return False


def duration(w, all_tagged_previous_stage, t):
    if w.soft_tagged(t - 1) or w.previous_tagged(all_tagged_previous_stage) or w.is_first():
        return True
    else:
        return False


def self_cycle(w, all_tagged_previous_stage, t):
    if w.tagged(t - 1) or w.previous_tagged(all_tagged_previous_stage) or w.is_first():
        return True
    else:
        return False


def interleaved(w, all_tagged_previous_stage, t):
    if w.is_first() or w.previous_tagged(all_tagged_previous_stage) or\
            w.is_previous_seq_tagged(w.get_last_leaved_node):
        return True
    else:
        return False


def self_cycle_interleaved(w, all_tagged_previous_stage, t):
    if w.tagged(t - 1) or w.is_first() or w.previous_tagged(all_tagged_previous_stage) or\
            w.single_previous_tagged_by_ID(w.get_last_leaved_node()):
        return True
    else:
        return False
