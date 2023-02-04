import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase2;

public class TE extends FunctionBase2{
    private final Embeddings e;

    public TE() {
        super();
        e = new Embeddings();
    }

    @Override
    public NodeValue exec(NodeValue nv1, NodeValue nv2) {
        double dist = e.exec(nv1, nv2, "embedding_transe.csv");
        return NodeValue.makeDouble(dist);
    }
}
