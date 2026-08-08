#include <stdio.h>
#include <stdint.h>
uint64_t powmod(uint64_t a, uint64_t b, uint64_t m){
    uint64_t res=1 % m;
    a%=m;
    while(b){ if(b&1) res=(res*a)%m; a=(a*a)%m; b>>=1; }
    return res;
}
int main(void){
    uint32_t x=12345;
    uint64_t sum=0;
    const uint64_t MOD=1000000007ULL;
    for (int i=0;i<1000000;i++){
        x = x*1664525u + 1013904223u;
        uint64_t a = (x % 100000) + 2;
        x = x*1664525u + 1013904223u;
        uint64_t b = (x % 1000) + 2;
        sum += powmod(a,b,MOD);
    }
    printf("%llu\n", (unsigned long long)sum);
    return 0;
}
