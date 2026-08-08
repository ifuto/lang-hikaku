class Program{
    static void Main(){
        int a_cnt=5000000, d_cnt=2500000, sp_cnt=1500000, other=1000000;
        var sb=new System.Text.StringBuilder(10000000);
        sb.Append('a', a_cnt);
        sb.Append('0', d_cnt);
        sb.Append(' ', sp_cnt);
        sb.Append('!', other);
        string s=sb.ToString();
        long alpha=0,digit=0,space=0;
        foreach(char c in s){
            if ((c>='a'&&c<='z')||(c>='A'&&c<='Z')) alpha++;
            else if (c>='0'&&c<='9') digit++;
            else if (c==' ') space++;
        }
        System.Console.WriteLine($"{alpha} {digit} {space}");
    }
}
