from SymbolicPlanRecognition.TagManagers import BasicTagManager


class CSQ(object):

    def __init__(self, tag_manager=None,is_consistent=None):
        if not tag_manager:
            self._tag_manager = BasicTagManager(is_consistent)
        else:
            self._tag_manager = tag_manager

    def apply_csq(self, all_obs, t, all_tagged_previous_stage):
        all_tagged_this_stage = []
        for p in all_obs:
            all_tagged_this_stage = self._propagate_up(p, t, all_tagged_this_stage, all_tagged_previous_stage)
            while p.tagged(t) and (not p.child_tagged(t)):
                p.delete_tag(t)
                p = p.parent()
                all_tagged_this_stage.remove(p)
        return all_tagged_this_stage

    def _propagate_up(self, w, t, all_tagged_this_stage, all_tagged_previous_stage):
        plans_to_remove = []
        propagate_up_success = True
        tagged = []
        while propagate_up_success and (not w.root()) and (not w.tagged(t)):
            w, propagate_up_success = self._tag_manager.manage_tag(w, t, all_tagged_previous_stage,
                                                                   all_tagged_this_stage, tagged)
        if not propagate_up_success:
            for a in tagged:
                a.delete_tag(t)
                plans_to_remove.append(a)
            all_tagged_this_stage = [x for x in all_tagged_this_stage if x not in plans_to_remove]
        return all_tagged_this_stage
