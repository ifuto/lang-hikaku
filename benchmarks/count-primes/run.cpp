#include <cstdio>
bool is_prime(int n){
    if (n<2) return false;
    if (n%2==0) return n==2;
    for (int d=3; (long)d*d<=n; d+=2) if(n%d==0) return false;
    return true;
}
int main(){
    int N=300000;
    int cnt=0;
    for (int i=2;i<=N;i++) if(is_prime(i)) cnt++;
    std::printf("%d\n", cnt);
    return 0;
}
