#include <cstdio>
int main(){
    int N=1000000;
    int best=1;
    int best_len=0;
    for (int i=1;i<=N;i++){
        long long n=i;
        int len=0;
        while(n!=1){ if(n%2==0) n/=2; else n=3*n+1; len++; }
        if (len>best_len){ best_len=len; best=i; }
    }
    std::printf("%d\n", best);
    return 0;
}
