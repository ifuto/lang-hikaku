#include <stdio.h>
int is_prime(int n){
    if (n<2) return 0;
    if (n%2==0) return n==2;
    for (int d=3; (long)d*d<=n; d+=2) if (n%d==0) return 0;
    return 1;
}
int main(void){
    int N=300000;
    int cnt=0;
    for (int i=2;i<=N;i++) if(is_prime(i)) cnt++;
    printf("%d\n", cnt);
    return 0;
}
