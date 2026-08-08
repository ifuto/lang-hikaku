class Program {
    static void Main() {
        int N=300;
        uint x=12345;
        long[,] a=new long[N,N];
        long[,] b=new long[N,N];
        long[,] c=new long[N,N];
        for(int i=0;i<N;i++) for(int j=0;j<N;j++){ x = x*1664525u + 1013904223u; a[i,j]=(long)(x%100); }
        for(int i=0;i<N;i++) for(int j=0;j<N;j++){ x = x*1664525u + 1013904223u; b[i,j]=(long)(x%100); }
        for(int i=0;i<N;i++) for(int k=0;k<N;k++){ long aik=a[i,k]; for(int j=0;j<N;j++) c[i,j]+=aik*b[k,j]; }
        long s=0; for(int i=0;i<N;i++) for(int j=0;j<N;j++) s+=c[i,j];
        System.Console.WriteLine(s);
    }
}
