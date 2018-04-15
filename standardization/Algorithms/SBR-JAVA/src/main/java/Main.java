import com.itextpdf.text.DocumentException;
import org.xml.sax.SAXException;
import javax.xml.parsers.ParserConfigurationException;
import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/****************************************
 * class Main.
 * gets two command line arguments - 
 * 		1. path to FDT output file.
 * 		2. path to plan library.
 * the program parse the plan library into a tree of plans,
 * and then CSQ algorithm is applied on each plan found in FDT output file and the plan library.
 * the program outputs "time_stamp plan" format file.  
 ****************************************/

public class Main {

    public static boolean readOneObs = false;
    public static int numberOfNodeCreations = 0;
    public static String inputFolderName = "/Users/ran/Desktop/Plan_recognition/";
    public static String outputFolderName = "/Users/ran/Desktop/Plan_recognition/SBR_OUTPUTS/";
    public static String[] domains =
            {
                     "full-20-1-5-1-2-3",
                    "full-20-1-5-1-5-1",
                     "full-20-1-5-3-2-1",
                    "full-100",
                     "1-5-2-3-2-full-100_baseline",
                     "1-5-2-3-4-full-100_or",
                    "1-5-2-5-2-full-100_and",
                    "1-5-3-3-2-full-100_depth",
                    //"temp"
            };

    public static List<String> allObs = new ArrayList<String>();

    public static int PLTreeDepth;

    public static HashMap<PathNode, TreeNode> pathNodeToTreeNode;

    public static void main(String[] args) throws IOException, ParserConfigurationException, SAXException, DocumentException {
        //System.in.read();
        for (String domainName : domains) {
            File newFolder = new File(outputFolderName + domainName);
            newFolder.mkdir();
            File newFile = new File(newFolder + "/" + domainName + "profile - time - SBR.csv");
            BufferedWriter writer = new BufferedWriter(new FileWriter(newFile));
            writer.write("file name,domain reading time,observations reading time" + "\n");
            File folder = new File(inputFolderName + "Domains/" + domainName + "/");
            File[] listOfFiles = folder.listFiles();
            for (int i = 0; i < listOfFiles.length; i++) {
                File file = listOfFiles[i];
                if (file.isFile() && file.getName().endsWith(".xml") /*&& file.getName().contains("Domain-71.")*/) {
                    CSQ csq = new CSQ();
                    HSQ hsq = new HSQ();
                    Parser parser = new Parser();
                    run(file.getPath(), file.getPath().replace("Domains", "Observations").replace("BaselineDomain", "Observations").replace(".xml", ".txt"), csq, hsq, parser, writer, newFolder.getPath());
                    System.out.println(file.getName());
                }
            }

            writer.close();
        }
        System.out.println(numberOfNodeCreations);
    }

    public static void run(String domainFileName, String obsFileName, CSQ csq, HSQ h, Parser parser, BufferedWriter writer, String folderName)
            throws IOException, ParserConfigurationException, SAXException, DocumentException {
        readOneObs = false;
        System.out.println(domainFileName + " " + obsFileName);

        long startReadingDomain = System.nanoTime();
        TreeNode root = parser.parse(domainFileName);
        long endReadingDomain = System.nanoTime();

        //Visualizer.makeTreeGraph(root, "/Users/ran/Desktop/Plan_Recognition/Observations/temp/TinkerPlots.pdf");

        List<TreeNode> plans = root.search();

        long startReadingObs = System.nanoTime();
        //System.out.println(obsFileName);
        ArrayList<Integer> allTags = readObservationsAndApplyCSQ(obsFileName, plans, csq);
        long endReadingObs = System.nanoTime();

        PLTreeDepth = depthOfPL(root);

        String[] obsDomainAndNumber = obsFileName.replace(".txt", "").split("/");
        String pdfFileName = folderName + "/" + obsDomainAndNumber[obsDomainAndNumber.length - 2] + obsDomainAndNumber[obsDomainAndNumber.length - 1] + ".pdf";
        String xmlFileName = folderName + "/" + obsDomainAndNumber[obsDomainAndNumber.length - 2] + obsDomainAndNumber[obsDomainAndNumber.length - 1] + ".xml";
        HashMap<Integer, List<PathNode>> mapOfPaths = generatePathsMap(allTags, root);
        ArrayList<ArrayList<PathNode>> allPaths = h.hsq(mapOfPaths);
        System.out.println(allPaths);
        vizualizeAndWriteToXML(allPaths, pdfFileName, xmlFileName);


        String res = new String();
        res += (obsDomainAndNumber[obsDomainAndNumber.length - 2] + obsDomainAndNumber[obsDomainAndNumber.length - 1] + ",");
        Long resInt = endReadingDomain - startReadingDomain;
        res += (resInt.toString() + ",");
        resInt = endReadingObs - startReadingObs;
        res += (resInt.toString() + ",");
        res += allPaths.size() + "\n";
        writer.write(res);

    }

    public static ArrayList<PathNode> makePaths(List<TreeNode> leaves, int tag) {
        ArrayList<PathNode> paths = new ArrayList<>();
        for (TreeNode p : leaves) {
            PathNode newNode;
            PathNode newParent = null;
            if (p.tagged(tag)) {
                newNode = new PathNode(p);
                while (p.parent() != null) {
                    newParent = new PathNode(p.parent());
                    if (newNode.getSeq().isEmpty()) {
                        newNode.setComplete(true);
                    }
                    newNode.setParent(newParent);
                    p = p.parent();
                    newNode = newParent;
                }
            }
            if (newParent != null) {
                paths.add(newParent);
            }
        }
        return paths;
    }

    public static ArrayList<Integer> readObservationsAndApplyCSQ(String obsFileName, List<TreeNode> plans, CSQ csq) throws IOException {
        ArrayList<Integer> allTags = new ArrayList<>();
        File f = new File(obsFileName);
        //System.out.println(obsFileName);
        BufferedReader br = new BufferedReader(new FileReader(f));
        // extract each time_stamp and plan
        List<TreeNode> listOfPreviousTagged = new ArrayList<TreeNode>();
        String line;
        int i = 0;
        while ((line = br.readLine()) != null) {
            i++;
            int ws = line.indexOf(' ');
            int t = Integer.parseInt(line.substring(0, ws));
            allTags.add(t);
            String label = line.substring(ws + 1, line.length());
            List<TreeNode> allObsCurrentTag = new ArrayList<TreeNode>();
            allObs.add(label);
            for (TreeNode tmp : plans) {
                if (tmp.getLabel().equals(label)) {
                    allObsCurrentTag.add(tmp);
                }
            }
            //apply CSQ algorithm
            listOfPreviousTagged = csq.csq(allObsCurrentTag, t, listOfPreviousTagged);

            if (i == 1)
            {
                readOneObs = true;
            }
        }

        return allTags;
    }

    public static HashMap<Integer, List<PathNode>> generatePathsMap(ArrayList<Integer> allTags, TreeNode root)
            throws IOException, DocumentException {
        HashMap<Integer, List<PathNode>> mapOfPaths = new HashMap<>();
        for (int tag : allTags) {
            for (TreeNode child : root.getChildren()) {
                if (child.tagged(tag)) {
                    List<TreeNode> leaves = child.getLeaves();
                    ArrayList<PathNode> paths = makePaths(leaves, tag);
                    if (mapOfPaths.containsKey(tag)) {
                        mapOfPaths.get(tag).addAll(paths);
                    } else {
                        ArrayList<PathNode> pathsToPutIntoMap = new ArrayList<>(paths);
                        mapOfPaths.put(tag, pathsToPutIntoMap);
                    }
                }
            }
        }
        System.out.println(mapOfPaths);
        return mapOfPaths;
    }

    private static int depthOfPL(TreeNode root) {
        int depth = 0;

        TreeNode rootCheckDepth = root;

        while (rootCheckDepth.isNotLeaf()) {
            rootCheckDepth = rootCheckDepth.firstChildOfNode();
            depth++;
        }

        return depth;
    }

    private static void vizualizeAndWriteToXML(ArrayList<ArrayList<PathNode>> allPaths, String vizualizeFileName, String xmlFileName)
            throws IOException, DocumentException {
        TreeNode root = new TreeNode("Root", 0);
        TreeNode finalRoot = unitePaths(allPaths, root);
        Visualizer.makeTreeGraph(finalRoot, vizualizeFileName);
        XMLOutputWriter.XMLWriter(finalRoot, xmlFileName);
    }

    public static TreeNode unitePaths(ArrayList<ArrayList<PathNode>> allExps, TreeNode root) {
        for (ArrayList<PathNode> exp : allExps) {
            TreeNode expRoot = new TreeNode("expRoot", 1);
            for (int i = exp.size() - 1; i >= 0; i--) {
                expRoot = unitePathWithCurrent(exp.get(i), expRoot);
            }
            root.addChild(expRoot);
        }
        System.out.println(root);
        return root;
    }

    public static TreeNode unitePathWithCurrent(PathNode path1, TreeNode root) {
        TreeNode rootToReturn = root;
        while (path1.getChild() != null) {
            PathNode path1Child = path1.getChild();
            TreeNode rootChild = null;
            if (!root.getChildren().isEmpty()) {
                rootChild = root.getChildren().get(root.getChildren().size() - 1);
            }

            if (rootChild == null || (path1Child != null && !rootChild.getLabel().equals(path1Child.getLabel())) ||
                    (path1Child != null && !rootChild.getLabel().equals(path1Child.getLabel()) && rootChild.getSeq().contains(path1Child.getID())) ||
                    path1Child != null && path1Child.toString().equals(rootChild.toString())) {
                rootChild = root.addChild(new TreeNode(path1Child));
            }
            root = rootChild;
            path1 = path1Child;
        }
        return rootToReturn;
    }
}
