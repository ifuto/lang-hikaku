#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){
    int a_cnt=5000000, d_cnt=2500000, sp_cnt=1500000, other=1000000;
    int total=a_cnt+d_cnt+sp_cnt+other;
    char *s=malloc(total+1);
    int pos=0;
    for (int i=0;i<a_cnt;i++) s[pos++]='a';
    for (int i=0;i<d_cnt;i++) s[pos++]='0';
    for (int i=0;i<sp_cnt;i++) s[pos++]=' ';
    for (int i=0;i<other;i++) s[pos++]='!';
    s[pos]='\0';
    long long alpha=0, digit=0, space=0;
    for (int i=0;i<total;i++){
        char c=s[i];
        if ((c>='a'&&c<='z')||(c>='A'&&c<='Z')) alpha++;
        else if (c>='0'&&c<='9') digit++;
        else if (c==' ') space++;
    }
    printf("%lld %lld %lld\n", alpha, digit, space);
    free(s);
    return 0;
}
