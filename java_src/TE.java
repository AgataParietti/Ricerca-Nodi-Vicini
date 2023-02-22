import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase2;

import java.util.HashMap;

public class TE extends FunctionBase2{
    private final Embeddings e;
    static HashMap<String, float[]> coordinates_te = new HashMap<>();

    public TE() {
        super();
        e = new Embeddings();
    }

    @Override
    public NodeValue exec(NodeValue nv1, NodeValue nv2) {
        if (coordinates_te.isEmpty()) {
            e.readCSV("embedding_transe.csv", coordinates_te);
        }
        double dist = e.exec(nv1, nv2, coordinates_te);
        return NodeValue.makeDouble(dist);
    }
}
