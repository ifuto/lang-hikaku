class Program{
    static long Gcd(long a, long b){ while(b!=0){ long t=a%b; a=b; b=t; } return a; }
    static void Main(){
        uint x=12345;
        uint mod=1000000000;
        long sum=0;
        for (int i=0;i<5000000;i++){
            x=x*1664525u+1013904223u;
            long a=(x%mod)+1;
            x=x*1664525u+1013904223u;
            long b=(x%mod)+1;
            sum+=Gcd(a,b);
        }
        System.Console.WriteLine(sum);
    }
}
