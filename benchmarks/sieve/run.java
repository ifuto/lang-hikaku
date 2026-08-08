public class run {
    public static void main(String[] args) {
        int N = 10000000;
        byte[] s = new byte[N+1];
        for (int i=0;i<=N;i++) s[i]=1;
        s[0]=0; s[1]=0;
        for (int i=2; (long)i*i<=N; i++) {
            if (s[i]==1) {
                for (long j=(long)i*i; j<=N; j+=i) s[(int)j]=0;
            }
        }
        long cnt=0;
        for (int i=0;i<=N;i++) cnt+=s[i];
        System.out.println(cnt);
    }
}
