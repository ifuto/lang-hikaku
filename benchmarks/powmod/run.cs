class Program{
    static long Powmod(long a, long b, long m){
        long res=1 % m;
        a%=m;
        while(b>0){ if ((b&1)==1) res=(res*a)%m; a=(a*a)%m; b>>=1; }
        return res;
    }
    static void Main(){
        uint x=12345;
        long sum=0;
        long MOD=1000000007L;
        for (int i=0;i<1000000;i++){
            x=x*1664525u+1013904223u;
            long a=(x%100000)+2;
            x=x*1664525u+1013904223u;
            long b=(x%1000)+2;
            sum+=Powmod(a,b,MOD);
        }
        System.Console.WriteLine(sum);
    }
}
