#include <cstdio>
int main(){
    long long N=1000000000LL;
    long long s=0;
    for (long long i=0;i<N;i++) s+=i;
    std::printf("%lld\n", s);
    return 0;
}
