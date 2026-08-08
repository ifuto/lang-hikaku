import java.util.HashMap;
public class run {
    public static void main(String[] args) {
        int N=1000000;
        HashMap<String,Integer> t = new HashMap<>(N*2);
        for (int i=0;i<N;i++) {
            t.put(String.format("k%07d", i), i);
        }
        System.out.println(N);
    }
}
