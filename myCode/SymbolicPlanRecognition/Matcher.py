class Matcher(object):
    def __init__(self, root):
        self._plan = root.search()

    def match(self, observation):
        current_obs = []
        for plan_step in self._plan:
            if plan_step.get_label() == observation:
                current_obs.append(plan_step)
        return current_obs
