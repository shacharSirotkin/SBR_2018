import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by ran on 11.8.2017.
 * This class represents a path for root to leaf (one leaf only)! in the Plan Library Tree
 * Extends: TreeNode class
 */
public class PathNode extends Node {

    private PathNode child;

    private PathNode parent;

    public PathNode(TreeNode treeNode)
    {
        if (!Main.readOneObs) {
            Main.numberOfNodeCreations++;
        }
        label = treeNode.getLabel();
        isRoot = treeNode.isRoot;
        tags = new ArrayList<Integer>(treeNode.tags);
        seqOf = new ArrayList<Integer>(treeNode.seqOf);
        seq = new ArrayList<Integer>(treeNode.seq);
        this.ID = treeNode.ID;
    }

    /****************************************
     * method: setParent
     * input:
     * 		TreeNode parent.
     * output:
     * operation: setter.
     ****************************************/
    public void setParent(PathNode parent) {
        this.parent = parent;
        parent.child = this;
    }

    /****************************************
     * method: parent
     * input:
     * output:
     * 		TreeNode parent.
     * operation: return this's parent.
     ****************************************/
    public PathNode parent() {
        return parent;
    }

    public PathNode getChild()
    {
        return child;
    }

    public List<PathNode> search() {
        List<PathNode> lst = new ArrayList<PathNode>();
        lst.add(this);
        if (child != null) {
            lst.addAll(child.search());
        }
        return lst;
    }

    @Override
    public String toString()
    {
        String res = new String(label);
        res+="\n";
        if (this.child != null) {
            res += child.toString("  ");
        }
        return res;
    }

    private String toString(String init)
    {
        String res = new String(init+this.label);
        res+="\n";
        if (this.child != null) {
            res += child.toString(init + "  ");
        }
        return res;
    }

    public int hasSeqChild(PathNode childOfRoot1) {
        PathNode childOfRoot2 = this;
        PathNode root2 = childOfRoot2;
        PathNode root1 = childOfRoot1;

        List<PathNode> childrenOfRoot1 = root1.search();
        List<PathNode> childrenOfRoot2 = root2.search();

        PathNode p = null;

        for (PathNode child1 : childrenOfRoot1) {
            for (PathNode child2 : childrenOfRoot2) {
                if (child1.seqOf.contains(child2.ID)) {
                    p = child2;
                    break;
                }
            }
        }

        int level = -1;
        PathNode pCheck  = root2;
        if (p != null)
        {
            while(!pCheck.equals(p))
            {
                level++;
                pCheck = pCheck.child;
            }
        }

        return level;
    }

    @Override
    public boolean equals(Object other)
    {
        return other.toString().equals(this.toString());
    }
}
