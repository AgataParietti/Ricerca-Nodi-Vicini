import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase2;

import java.util.HashMap;

public class W2V extends FunctionBase2{
    private final Embeddings e;
    static HashMap<String, float[]> coordinates_w2v = new HashMap<>();

    public W2V() {
        super();
        e = new Embeddings();
    }

    @Override
    public NodeValue exec(NodeValue nv1, NodeValue nv2) {
        if (coordinates_w2v.isEmpty()) {
            e.readCSV("embedding_w2v.csv", coordinates_w2v);
        }
        double dist = e.exec(nv1, nv2, coordinates_w2v);
        return NodeValue.makeDouble(dist);
    }
}
