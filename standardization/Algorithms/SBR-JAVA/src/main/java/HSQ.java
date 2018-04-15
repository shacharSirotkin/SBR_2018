import com.itextpdf.text.DocumentException;
import edu.uci.ics.jung.graph.*;
import javafx.util.Pair;
import java.io.IOException;
import java.util.*;
import java.util.List;

/****************************************
 * class HSQ.
 * HSQ algorithm.
 *****************************************/
public class HSQ {

    /****************************************
     * method: hsq
     * input:
     * 		HashMap<Integer, List<TreeNode>> plans - hash map of time_stamps and matching plans.
     * 		int serial - used to mark plans. can be replaced with a boolean flag.
     * output:
     * 		TreeNode root.
     * operation: removes plans from original hash map, organizes the remaining plans as a tree.
     ****************************************/

    private static HashMap<String, PathNode> pathStringToPathPlan = new HashMap<>();
    public ArrayList<ArrayList<PathNode>> hsq(HashMap<Integer, List<PathNode>> mapOfPaths)
            throws IOException, DocumentException {
        DirectedSparseGraph<String, Pair<String, String>> g = new DirectedSparseGraph<String, Pair<String, String>>();
        for (int i = mapOfPaths.size(); i > 1; i--) {
            for (PathNode path1 : mapOfPaths.get(i)) {
                boolean isFirstChild = ifIsFirstChild(path1);
                for (PathNode path2 : mapOfPaths.get(i - 1)) {
                   int levelOfSeq = path2.hasSeqChild(path1);
                   boolean hasSeqChild = (levelOfSeq != -1);
                    if (isFirstChild || (hasSeqChild   && allCompletedFromLevel(path2, levelOfSeq + 2)) || path1.equals(path2)) {
                          generateEdge(g, path1, path2, i);
                    }
                }
            }
        }
        ArrayList<ArrayList<PathNode>> allPaths = getAllPaths(mapOfPaths, g);
        return allPaths;
    }

    private void generateEdge(DirectedSparseGraph<String, Pair<String, String>> g, PathNode path1,
                              PathNode path2, int i)
    {
        PathNode rootNode1 = path1;
        PathNode rootNode2 = path2;
        g.addVertex(rootNode1.toString() +  " " + i);
        g.addVertex(rootNode2.toString() +  " " + (i - 1));
        pathStringToPathPlan.put(rootNode1.toString() +  " " + i, rootNode1);
        pathStringToPathPlan.put(rootNode2.toString() +  " " + (i - 1), rootNode2);
        Pair<String, String> edge = new Pair<String, String>(rootNode1.toString() +  " " + i, rootNode2.toString() +  " " + (i - 1));
        g.addEdge(edge, rootNode1.toString() +  " " + i, rootNode2.toString() +  " " + (i - 1));
    }

    public static boolean allCompletedFromLevel(PathNode path, int j)
    {
        List<PathNode> pathChildren = path.search();
        for (int i = j ; i < pathChildren.size() ; i++)
        {
            if (!pathChildren.get(i).getIsComplete() && pathChildren.get(i).getChild() != null)
            {
                return false;
            }
        }

        return true;
    }

    private ArrayList<ArrayList<PathNode>> getAllPaths (HashMap<Integer, List<PathNode>> mapOfPaths, DirectedSparseGraph<String, Pair<String, String>> g){
        ArrayList<ArrayList<PathNode>> allPaths = new ArrayList<ArrayList<PathNode>>();
        for (PathNode path1 : mapOfPaths.get(mapOfPaths.size())) {
            for (PathNode path2 : mapOfPaths.get(1)) {
                PathNode rootNode1 = path1;
                PathNode rootNode2 = path2;
                ArrayList<String> visited = new ArrayList<String>();
                LinkedList<String> currpath = new LinkedList<String>();
                LinkedList<ArrayList<PathNode>> paths = new LinkedList<ArrayList<PathNode>>();
                findAllPaths(rootNode1.toString() + " " + mapOfPaths.size(), rootNode2.toString() + " " + 1, visited, paths, currpath, g);
                for (ArrayList<PathNode> path : paths) {
                    allPaths.add(path);
                }
            }
        }
        return allPaths;
    }

    private void findAllPaths(String start, String end, ArrayList<String> visited, LinkedList<ArrayList<PathNode>> path,
                              LinkedList<String> currpath, Graph<String, Pair<String, String>> g) {

        if (visited.contains(start)) {
            return;
        }

        visited.add(start);

        currpath.addLast(start);

        if (start.equals(end)) {

            ArrayList<PathNode> list = new ArrayList<PathNode>();

            for (String l : currpath) {
                list.add(pathStringToPathPlan.get(l));
            }

                path.add(list);

            currpath.removeLast();
            visited.remove(start);
            return;
        }

        if (g.getOutEdges(start) != null) {
            for (Pair<String, String> edge : g.getOutEdges(start)) {
                String succ = g.getDest(edge);
                findAllPaths(succ, end, visited, path, currpath, g);
            }
        }
        visited.remove(start);
        currpath.removeLast();
    }

    private boolean ifIsFirstChild(PathNode path1)
    {
        boolean isFirstChild = true;
        List<PathNode> search = path1.search();
        for (PathNode child1 : search) {
            if (!child1.getSeqOf().isEmpty()) {
                isFirstChild = false;
                break;
            }
        }
        return isFirstChild;
    }
}
