
import java.util.ArrayList;
import java.util.List;

/****************************************
 * class CSQ.
 * CSQ algorithm and necessary methods.
*****************************************/
public class CSQ {

	/****************************************
	 * method: csq
	 * input:
	 * 		TreeNode M.
	 * 		TreeNode g.
	 * 		int t - time_stamp.
	 * output:
	 * operation: assign t on according plan, propagates it up, and removes irrelevant tags.
	 ****************************************/
	public List<TreeNode> csq(List<TreeNode> allObs, int t, List<TreeNode> allTaggedPreviousStage) {
		ArrayList<TreeNode> allTaggedThisStage = new ArrayList<TreeNode>();
		for (TreeNode p : allObs) {
			propagateUp(p, t, allTaggedThisStage, allTaggedPreviousStage);
			while (p.tagged(t) && !p.ChildTagged(t)) {
				p.delete_tag(t);
				p = p.parent();
				allTaggedThisStage.remove(p);
			}
		}
		return allTaggedThisStage;
	}

	/****************************************
	 * method: propagateUp
	 * input:
	 * 		TreeNode w.
	 * 		TreeNode pl - plan library.
	 * 		int t - time_stamp.
	 * output:
	 * operation: assign t on plan w from pl,
	 * 			  and propagates up the tag until root is reached.
	 ****************************************/
	private void propagateUp(TreeNode w, int t, List<TreeNode> allTaggedThisStage, List<TreeNode> allTaggedPreviousStage) {
		ArrayList<TreeNode> plansToRemove = new ArrayList<TreeNode>();
		boolean propagateUpSuccess = true;
		TreeNode v = w;
		ArrayList<TreeNode> tagged = new ArrayList<TreeNode>();
		while (!v.root() && propagateUpSuccess && !v.tagged(t)) {
				if (isConsistent(v, allTaggedPreviousStage, t)) {
					v.tag(t);
					tagged.add(v);
					allTaggedThisStage.add(v);
					v = v.parent();
					propagateUpSuccess = true;
				}

			else {
				propagateUpSuccess = false;
			}
		}

		if (!propagateUpSuccess) {
			for (TreeNode a: tagged) {
				a.delete_tag(t);
				plansToRemove.add(a);
			}

			allTaggedThisStage.removeAll(plansToRemove);
			tagged.removeAll(plansToRemove);
		}
	}

	/****************************************
	 * method: isConsistent
	 * input:
	 * 		TreeNode v.
	 * 		TreeNode g.
	 * 		int t - time_stamp.
	 * output:
	 * 		boolean value - True if plan is consistent with time_stamp, False otherwise.
	 * operation:
	 ****************************************/
	private boolean isConsistent(TreeNode v, List<TreeNode> allTaggedPreviousStage, int t) {
			if (v.tagged(t-1) || v.PreviousSeqEdgeTagged(allTaggedPreviousStage) || v.NoSeqEdges()) {
				return true;
			}
		return false;
	}

}
