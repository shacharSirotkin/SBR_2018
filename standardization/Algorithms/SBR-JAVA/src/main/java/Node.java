import java.util.ArrayList;
import java.util.List;

/**
 * Created by ran on 12.8.2017.
 *
 */
public abstract class Node {

    protected int ID;

    protected String label;

    protected boolean isRoot;

    protected boolean isComplete = false;

    protected List<Integer> tags = new ArrayList<Integer>();

    protected List<Integer> seqOf = new ArrayList<Integer>();

    protected List<Integer> seq = new ArrayList<Integer>();

    /****************************************
     * method: root
     * input:
     * output: boolean isroot.
     * operation: return True if this is root, false otherwise.
     ****************************************/
    public boolean root() {
        return isRoot;
    }

    /****************************************
     * method: tag
     * input:
     * 		int n - time_stamp.
     * 		String s - 'soft' or 'hard', depends on kind of tag.
     * output:
     * operation: checks string, and assign tag accordingly.
     ****************************************/
    public void tag(int n) {
        tags.add(n);
    }

    /****************************************
     * method: delete_tag
     * input:
     * 		Integer n - time_stamp to remove from tags.
     * output:
     * operation: removes according tag.
     ****************************************/
    public void delete_tag(Integer n) {
        tags.remove(n);
    }

    /****************************************
     * method: tagged
     * input:
     * 		Integer n - time_stamp.
     * 		String s - 'soft' or 'hard'.
     * output:
     * 		boolean value - True if this is tagged, False accordingly.
     * operation: checks given String, then checks according list to find a match to time_stamp.
     ****************************************/
    public boolean tagged(Integer n) {
        return tags.contains(n);
    }

    /****************************************
     * method: NoSeqEdges
     * input:
     * output:
     * 		boolean value - True if no sequential edges exist, False otherwise.
     * operation: checks if there are sequential edges.
     ****************************************/
    public boolean NoSeqEdges() {
        return this.seqOf.isEmpty();
    }

    public void addSeqOf(int ID, Node p) {
        this.seqOf.add(ID);
        p.seq.add(this.ID);
    }

    /****************************************
     * method: getLabel
     * input:
     * output:
     * 		String label.
     * operation: getter.
     ****************************************/
    public String getLabel() {
        return label;
    }

    public void setRoot(boolean isRoot)
    {
        this.isRoot = isRoot;
    }

    public List<Integer> getSeq() {
        return seq;
    }

    public List<Integer> getSeqOf() {
        return seqOf;
    }

    public void setComplete(boolean complete) {
        isComplete = complete;
    }

    public boolean getIsComplete() {return isComplete;}

    public List<Integer> getTags()
    {
        return tags;
    }

    public int getID()
    {
        return ID;
    }
}

