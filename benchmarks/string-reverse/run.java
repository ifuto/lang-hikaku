public class run{
    public static void main(String[] args){
        int size=10000000;
        int reps=10;
        StringBuilder sb=new StringBuilder(size);
        for (int i=0;i<size;i++) sb.append('a');
        long total=0;
        for (int r=0;r<reps;r++){ sb.reverse(); total+=sb.length(); }
        System.out.println(total);
    }
}
