import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.util.*;

public class Parser {

    private int idCounter = 0;

    private Document doc;

    private HashMap<String, TreeNode> hmap = new HashMap<String, TreeNode>();

    private ArrayList<String> goals = new ArrayList<String>();

    private LinkedList<org.w3c.dom.Node> Recipes = new LinkedList<org.w3c.dom.Node>();

    private ArrayList<String> arrayOfUnauthorizedLetters = new ArrayList<>(Arrays.asList("MU","RB","S","SA","SAB","SwA","MR","ChC","CRT","DS","DT","MS"));

    public TreeNode parse(String path) throws ParserConfigurationException, SAXException, IOException {
        TreeNode root = new TreeNode("root", generateID());
        root.setRoot(true);
        File fXmlFile = new File(path);
        DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
        doc = dBuilder.parse(fXmlFile);
        doc.getDocumentElement().normalize();
        readNonTerminalLetters(root);
        readRecipes(root);
        System.out.println(root);
        return root;
}

    private void readNonTerminalLetters(TreeNode root) {
        NodeList nonTerminalLetters = ((Element) doc.getElementsByTagName("Non-Terminals").item(0)).getElementsByTagName("Letter");
        for (int i = 0; i < nonTerminalLetters.getLength(); i++) {
            if (((Element) nonTerminalLetters.item(i)).getAttribute("goal").equals("yes")) {
                goals.add(((Element) nonTerminalLetters.item(i)).getAttribute("id"));
                TreeNode p = new TreeNode(((Element) nonTerminalLetters.item(i)).getAttribute("id"), generateID());
                root.addChild(p);
                hmap.put(((Element) nonTerminalLetters.item(i)).getAttribute("index"), p);
            }
        }
    }

    private void readRecipes(TreeNode root) {
        NodeList RecipesAsNodeList = doc.getElementsByTagName("Recipe");
        for (int i = 0; i < RecipesAsNodeList.getLength(); i++) {
            Recipes.add(RecipesAsNodeList.item(i));
        }
        while (!Recipes.isEmpty()) {
            //Recipes.forEach(element -> System.out.println(((Element) element).getAttribute("lhs")));
            //System.out.println("-----------------------------");
            Element Recipe = (Element) Recipes.removeFirst();
            TreeNode p;
            if (root.findByLabel(Recipe.getAttribute("lhs")) != null) {
                p = root.findByLabel(Recipe.getAttribute("lhs"));
            } else {
                if (!arrayOfUnauthorizedLetters.contains(Recipe.getAttribute("lhs"))) {
                    Recipes.addLast(Recipe);
                }
                continue;
            }

            readSingleRecipe(Recipe, p);

            readOrderCons(Recipe);
        }
    }

    private void readSingleRecipe(Element Recipe, TreeNode p)
    {
        //parse the Letters - children's of recipe.
        int j = 0;
        Element Letter = (Element) Recipe.getElementsByTagName("Letter").item(j);
        while (Letter != null) {
            //add plan children's
            int ID = generateID();
            TreeNode child = new TreeNode((Letter.getAttribute("id")), ID);

            p.addChild(child);

            hmap.put(Letter.getAttribute("index"), child);

            //parse next letter
            j += 1;

            Letter = (Element) Recipe.getElementsByTagName("Letter").item(j);
        }
    }

    private void readOrderCons(Element Recipe) {
        int k = 0;
        Element OrderCons = (Element) Recipe.getElementsByTagName("OrderCons").item(k);

        //parse the OrderCons - seq edges.

        while (OrderCons != null) {
            //add seq edges

            TreeNode p = hmap.get(OrderCons.getAttribute("firstIndex"));
            hmap.get(OrderCons.getAttribute("secondIndex")).addSeqOf(p.getID(), p);

            //System.out.println( "second index " +  hmap.get(OrderCons.getAttribute("secondIndex")) +  "first index " + hmap.get(OrderCons.getAttribute("firstIndex")));

            k += 1;
            OrderCons = (Element) Recipe.getElementsByTagName("OrderCons").item(k);
        }
    }

    private int generateID() {
        idCounter++;
        return idCounter;
    }
}