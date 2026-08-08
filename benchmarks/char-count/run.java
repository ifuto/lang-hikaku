public class run{
    public static void main(String[] args){
        int a_cnt=5000000, d_cnt=2500000, sp_cnt=1500000, other=1000000;
        StringBuilder sb=new StringBuilder(10000000);
        for(int i=0;i<a_cnt;i++) sb.append('a');
        for(int i=0;i<d_cnt;i++) sb.append('0');
        for(int i=0;i<sp_cnt;i++) sb.append(' ');
        for(int i=0;i<other;i++) sb.append('!');
        String s=sb.toString();
        long alpha=0,digit=0,space=0;
        for(int i=0;i<s.length();i++){
            char c=s.charAt(i);
            if ((c>='a'&&c<='z')||(c>='A'&&c<='Z')) alpha++;
            else if (c>='0'&&c<='9') digit++;
            else if (c==' ') space++;
        }
        System.out.println(alpha+" "+digit+" "+space);
    }
}
