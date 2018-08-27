class CSQ(object):
    def apply_csq(self, all_obs, t, all_tagged_previous_stage):
        all_tagged_this_stage = []
        for p in all_obs:
            all_tagged_this_stage = self.propagate_up(p, t, all_tagged_this_stage, all_tagged_previous_stage)
            while p.tagged(t) and (not p.child_tagged(t)):
                p.delete_tag(t)
                p = p.parent()
                all_tagged_this_stage.remove(p)
        return all_tagged_this_stage

    def propagate_up(self, w, t, all_tagged_this_stage, all_tagged_previous_stage):
        plans_to_remove = []
        propagate_up_success = True
        tagged = []
        while (not w.root()) and propagate_up_success and (not w.tagged(t)):
            if self.is_consistent(w, all_tagged_previous_stage, t):
                w.tag(t)
                tagged.append(w)
                all_tagged_this_stage.append(w)
                w = w.parent()
                propagate_up_success = True
            else:
                propagate_up_success = False

        if not propagate_up_success:
            for a in tagged:
                a.delete_tag(t)
                plans_to_remove.append(a)
            all_tagged_this_stage = [x for x in all_tagged_this_stage if x not in plans_to_remove]
        return all_tagged_this_stage

    def is_consistent(self, w, all_tagged_previous_stage, t):
        if w.tagged(t - 1) or w.previous_tagged(all_tagged_previous_stage) or w.is_first():
            return True
        else:
            return False
