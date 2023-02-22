import org.apache.jena.sparql.expr.NodeValue;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.*;

public class Embeddings {

    public Double exec(NodeValue nv1, NodeValue nv2, HashMap<String, float[]> coordinates) {
        String node1Name = nv1.toString();
        String node2Name = nv2.toString();

        //calculate cosine distance and return
        return cosineDist(coordinates.get(node1Name), coordinates.get(node2Name));
    }

    private static float[] convert2Vector(List<String> node) {
        float[] vector = new float[node.size() - 1];
        for (int j = 1; j < node.size(); j++) {
            vector[j - 1] = Float.parseFloat(node.get(j));
        }
        return vector;
    }


    private double cosineDist(float[] vectorA, float[] vectorB) {
        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i = 0; i < vectorA.length; i++) {
            dotProduct += vectorA[i] * vectorB[i];
            normA += Math.pow(vectorA[i], 2);
            normB += Math.pow(vectorB[i], 2);
        }
        double dist = (1 - (dotProduct / (Math.sqrt(normA) * Math.sqrt(normB))));
        if (dist < 0) {
            return 0.;
        } else if (dist > 2) {
            return 2.;
        } else {
            return dist;
        }
    }

    protected void readCSV(String file, HashMap<String, float[]> coordinates) {
        InputStream is = Embeddings.class.getResourceAsStream(file);
        String delimiter = ";";
        String line;
        try {
            assert is != null;
            try (BufferedReader br = new BufferedReader(new InputStreamReader(is))) {
                while((line = br.readLine()) != null){
                    List<String> values = Arrays.asList(line.split(delimiter));
                    coordinates.put(values.get(0), convert2Vector(values));
                }

            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
