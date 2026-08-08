using System;
class Program{
    static void Main(){
        int size=10000000;
        int reps=10;
        char[] s=new char[size];
        for (int i=0;i<size;i++) s[i]='a';
        long total=0;
        for (int r=0;r<reps;r++){ Array.Reverse(s); total+=s.Length; }
        Console.WriteLine(total);
    }
}
