import org.apache.jena.sparql.expr.NodeValue;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Embeddings {

    public Double exec(NodeValue nv1, NodeValue nv2, String file) {
        List<List<String>> data = readCSV(file);

        //search nodes coordinates
        String node1Name = nv1.toString();
        String node2Name = nv2.toString();

        List<String> node1 = find_coords(node1Name, data);
        List<String> node2 = find_coords(node2Name, data);

        //convert to vector
        float[] node1V = convert2Vector(node1);
        float[] node2V = convert2Vector(node2);

        //calculate cosine distance and return
        return cosineDist(node1V, node2V);
    }

    private float[] convert2Vector(List<String> node) {
        float[] vector = new float[node.size() - 1];
        for (int j = 1; j < node.size(); j++) {
            vector[j-1] = Float.parseFloat(node.get(j));
        }
        return vector;
    }

    private static List<String> find_coords(String nodeName, List<List<String>> data) {
        List<String> node = new ArrayList<>();
        for(int i = 1; i < data.size(); i++) {
            if (nodeName.equals((data.get(i)).get(0))) {
                node = data.get(i);
                break;
            }
        }
        return node;
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

    private static List<List<String>> readCSV(String file) {
        InputStream is = TE.class.getResourceAsStream(file);
        List<List<String>> lines = new ArrayList<>();
        String delimiter = ",";
        String line;
        try {
            assert is != null;
            try (BufferedReader br = new BufferedReader(new InputStreamReader(is))) {
                while((line = br.readLine()) != null){
                    List<String> values = Arrays.asList(line.split(delimiter));
                    lines.add(values);
                }
                return lines;

            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
