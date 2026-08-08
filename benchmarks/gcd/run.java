public class run{
    static long gcd(long a, long b){ while(b!=0){ long t=a%b; a=b; b=t;} return a;}
    public static void main(String[] args){
        long x=12345;
        long mod=1000000000L;
        long sum=0;
        for (int i=0;i<5000000;i++){
            x=(x*1664525+1013904223) & 0xFFFFFFFFL;
            long a=(x % mod)+1;
            x=(x*1664525+1013904223) & 0xFFFFFFFFL;
            long b=(x % mod)+1;
            sum+=gcd(a,b);
        }
        System.out.println(sum);
    }
}
