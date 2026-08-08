using System.Collections.Generic;
class Program {
    static void Main() {
        int N=1000000;
        var t = new Dictionary<string,int>(N*2);
        for (int i=0;i<N;i++) {
            t[string.Format("k{0:D7}", i)]=i;
        }
        System.Console.WriteLine(N);
    }
}
