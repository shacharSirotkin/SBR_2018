import com.itextpdf.awt.PdfGraphics2D;
import com.itextpdf.text.*;
import com.itextpdf.text.Document;
import com.itextpdf.text.pdf.PdfContentByte;
import com.itextpdf.text.pdf.PdfTemplate;
import com.itextpdf.text.pdf.PdfWriter;
import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.algorithms.layout.TreeLayout;
import edu.uci.ics.jung.graph.DelegateTree;
import edu.uci.ics.jung.graph.DirectedOrderedSparseMultigraph;
import edu.uci.ics.jung.visualization.BasicTransformer;
import edu.uci.ics.jung.visualization.RenderContext;
import edu.uci.ics.jung.visualization.VisualizationImageServer;
import edu.uci.ics.jung.visualization.VisualizationViewer;
import edu.uci.ics.jung.visualization.decorators.ToStringLabeller;
import edu.uci.ics.jung.visualization.renderers.Renderer;
import edu.uci.ics.jung.visualization.transform.shape.GraphicsDecorator;
import javafx.util.Pair;

import java.awt.*;
import java.awt.Font;
import java.awt.font.FontRenderContext;
import java.awt.geom.AffineTransform;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Point2D;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Visualizer {

    public static void makeTreeGraph(TreeNode finalRoot, String fileName) throws DocumentException, IOException {
        List<DelegateTree<TreeNode, Pair<TreeNode, TreeNode>>> trees = new ArrayList<DelegateTree<TreeNode, Pair<TreeNode, TreeNode>>>();
        for (TreeNode expRoot : finalRoot.getChildren()) {
            DelegateTree<TreeNode, Pair<TreeNode, TreeNode>> g = new DelegateTree<>(
                    new DirectedOrderedSparseMultigraph<TreeNode, Pair<TreeNode, TreeNode>>());
            g.addVertex(expRoot);
            createSubTrees(expRoot, g, expRoot);
            trees.add(g);
        }
        printGraphToPDF(trees, fileName);
    }

    private static void printGraphToPDF(List<DelegateTree<TreeNode, Pair<TreeNode, TreeNode>>> trees, String fileName)
            throws IOException, DocumentException {

        BasicTransformer vertexSize = new BasicTransformer() {
            public Shape transform(TreeNode node) {
                Ellipse2D circle = new Ellipse2D.Double(-15, -15, 30, 30);
                AffineTransform affinetransform = new AffineTransform();
                FontRenderContext frc = new FontRenderContext(affinetransform, true, true);
                Font font = new Font("Calibri", Font.BOLD, 14);
                int textwidth = (int) (font.getStringBounds(node.toString(), frc).getWidth());

                return AffineTransform.getScaleInstance(textwidth / 14, 1).createTransformedShape(circle);
            }
        };

        Document document = new Document();
        PdfWriter writer = PdfWriter.getInstance(document, new FileOutputStream(fileName));
        for (int i = 0; i < trees.size(); i++) {
            TreeLayout<TreeNode, Pair<TreeNode, TreeNode>> layout1 = new TreeLayout<TreeNode, Pair<TreeNode, TreeNode>>(
                    (DelegateTree<TreeNode, Pair<TreeNode, TreeNode>>) trees.get(i));
            VisualizationViewer<TreeNode, Pair<TreeNode, TreeNode>> vv = new VisualizationViewer<TreeNode, Pair<TreeNode, TreeNode>>(layout1);
            vv.setGraphLayout(layout1);
            VisualizationImageServer<TreeNode, Pair<TreeNode, TreeNode>> vis = new VisualizationImageServer<TreeNode, Pair<TreeNode, TreeNode>>(
                    vv.getGraphLayout(), vv.getGraphLayout().getSize());
            if (i == 0) {
                document.open();
                document.setPageSize(new com.itextpdf.text.Rectangle((vis.getWidth() + 20) * 10,
                        (vis.getHeight() + 20) * 10));
            }
            vis.getRenderContext().setVertexLabelTransformer(new ToStringLabeller());
            vis.setBackground(Color.WHITE);
            vis.getRenderer().getVertexLabelRenderer().setPosition(Renderer.VertexLabel.Position.CNTR);
            vis.getRenderer().setVertexRenderer(new MyRenderer());
            vis.getRenderContext().setVertexLabelTransformer((x) -> x.getLabel());
            PdfContentByte canvas = writer.getDirectContent();
            PdfTemplate template = canvas.createTemplate(vis.getWidth() + 20, vis.getHeight() + 20);
            Graphics2D g2d = new PdfGraphics2D(template, vis.getWidth() + 20, vis.getHeight() + 20);
            //PdfContentByte contentByte = writer.getDirectContent();
            Container container = new Container();
            container.addNotify();
            container.add(vis);
            container.setVisible(true);
            container.paintComponents(g2d);
            // Dispose of the graphics and close the document
            g2d.dispose();
            com.itextpdf.text.Image img = com.itextpdf.text.Image.getInstance(template);
            img.scaleToFit((vis.getWidth() + 20) * 10, (vis.getHeight() + 20) * 10);
            document.newPage();
            document.add(img);
            //contentByte.addTemplate(template, 0, 0);
        }
        document.close();
    }

    static class MyRenderer implements Renderer.Vertex<TreeNode, Pair<TreeNode, TreeNode>> {
        @Override
        public void paintVertex(RenderContext<TreeNode, Pair<TreeNode, TreeNode>> rc,
                                Layout<TreeNode, Pair<TreeNode, TreeNode>> layout, TreeNode vertex) {
            GraphicsDecorator graphicsContext = rc.getGraphicsContext();
            Point2D center = layout.apply(vertex);
            Shape shape = null;
            Color color = null;
            shape = new Ellipse2D.Double(center.getX() - 10, center.getY() - 10, 40, 40);
            color = new Color(0, 127, 127);
            graphicsContext.setPaint(color);
            graphicsContext.fill(shape);
        }
    }

    private static void createSubTrees(TreeNode root, DelegateTree<TreeNode, Pair<TreeNode, TreeNode>> g, TreeNode parent) {
        if (!root.getChildren().isEmpty()) {
            for (TreeNode child : root.getChildren()) {
                g.addChild(new Pair(parent, child), parent, child);
                createSubTrees(child, g, child);
            }
        }
    }

}
