/**
 * Created by ran on 11.8.2017.
 * This class represents a node in the Plan Library
 */

import java.util.*;

public class TreeNode extends Node {

	private List<TreeNode> children = new ArrayList<TreeNode>();

	private TreeNode parent;


	/****************************************
	 * method: TreeNode
	 * input: String s - label.
	 * output:
	 * operation: constructor.
	 ****************************************/
	public TreeNode(String s, int ID) {
		if (!Main.readOneObs) {
			Main.numberOfNodeCreations++;
		}
		parent = null;
		label = s;
		isRoot = false;
		this.ID = ID;
	}


	/****************************************
	 * method: TreeNode
	 * input: TreeNode other.
	 * output:
	 * operation: constructor.
	 ****************************************/
	public TreeNode(Node other) {
		if (!Main.readOneObs) {
			Main.numberOfNodeCreations++;
		}
		label = other.getLabel();
		isRoot = other.isRoot;
		tags = new ArrayList<Integer>(other.tags);
		seqOf = other.seqOf;
		seq = other.seq;
		this.ID = other.ID;
	}

	/****************************************
	 * method: ChildTagged
	 * input:
	 * 		int t - time_stamp.
	 * output:
	 * 		boolean value - True if this has a child with a given time_stamp, False otherwise.
	 * operation: Iterates over list of children, and checks for a match.
	 ****************************************/
	public boolean ChildTagged(int t) {
		for (TreeNode d: children) {
			if (d.tagged(t)) {
				return true;
			}
		}
		if (children.isEmpty()) {
			return true;
		}
		return false;
	}

	/****************************************
	 * method: setParent
	 * input:
	 * 		TreeNode parent.
	 * output:
	 * operation: setter.
	 ****************************************/
	public void setParent(TreeNode parent) {
		this.parent = parent;
		parent.children.add(this);
	}


	public List<TreeNode> search() {
		List<TreeNode> lst = new ArrayList<TreeNode>();
		lst.add(this);
		for (TreeNode n: children) {
			lst.addAll(n.search());
		}
		return lst;
	}

	/****************************************
	 * method: getLeaves
	 * input:
	 * output:
	 * 		List<TreeNode> of all leaves
	 * operation: uses search(), and remove from it all nodes that have children.
	 ****************************************/
	public List<TreeNode> getLeaves() {
		List<TreeNode> leaves = new ArrayList<TreeNode>();
		for (TreeNode p: this.search()) {
			if (p.getChildren().isEmpty()) {
				leaves.add(p);
			}
		}
		return leaves;
	}

	/****************************************
	 * method: getChildren
	 * input:
	 * output:
	 * 		List<TreeNode> children.
	 * operation: getter.
	 ****************************************/
	public List<TreeNode> getChildren() {
		return children;
	}

	/****************************************
	 * method: addChild
	 * input:
	 * 		TreeNode child.
	 * output:
	 * operation: add a plan to list of children.
	 ****************************************/
	public TreeNode addChild(TreeNode child) {
		children.add(child);
		child.parent = this;
		return child;
	}

	/****************************************
	 * method: search
	 * input:
	 * output:
	 * 		List<TreeNode> - all descendant of a plan.
	 * operation: recursive calls to all children.
	 ****************************************/

	public String toString()
	{
		String res = new String(label);
		res+="\n";
		if (!this.getChildren().isEmpty())
			for (TreeNode child : this.getChildren())
			{
				res+=child.toString("  ");
			}
		return res;
	}

	private String toString(String init)
	{
		String res = new String(init+this.label);
		res+="\n";
		if (!this.getChildren().isEmpty())
			for (TreeNode child : this.getChildren())
			{
				res+=child.toString(init+"  ");
			}
		return res;
	}

	public TreeNode firstChildOfNode()
	{
		return this.getChildren().get(0);
	}

	public boolean isNotLeaf()
	{
		return !this.children.isEmpty();
	}

	/****************************************
	 * method: PreviousSeqEdgeTaggedWithHard
	 * input:
	 * 		int t.
	 * output:
	 * 		boolean value - True if there is a sequential edge of a certain range, False otherwise.
	 * operation: iterates over sequential edges and looks for a match.
	 ****************************************/
	public boolean PreviousSeqEdgeTagged(List<TreeNode> allTaggedPreviousStage) {
		for (TreeNode p: allTaggedPreviousStage) {
			if (seqOf.contains(p.getID())) {
				return true;
			}
		}
		return false;
	}

	/****************************************
	 * method: parent
	 * input:
	 * output:
	 * 		TreeNode parent.
	 * operation: return this's parent.
	 ****************************************/
	public TreeNode parent() {
		return parent;
	}

	/****************************************
	 * method: findByLabel
	 * input:
	 * 		String s.
	 * output:
	 * 		TreeNode - a plan that matches a given String.
	 * operation: checks for accordance between a given string and this's label,
	 * 			  and if not found - done recursively on this's children.
	 ****************************************/
	public TreeNode findByLabel(String s) {
		for (TreeNode p: this.search()) {
			if (p.getLabel().equals(s)) {
				return p;
			}
		}
		return null;
	}
}

