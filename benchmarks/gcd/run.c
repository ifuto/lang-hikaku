#include <stdio.h>
#include <stdint.h>
uint64_t gcd(uint64_t a, uint64_t b){ while(b){ uint64_t t=a%b; a=b; b=t;} return a; }
int main(void){
    uint32_t x=12345;
    const uint32_t mod=1000000000;
    long long sum=0;
    for (int i=0;i<5000000;i++){
        x = x*1664525u + 1013904223u;
        uint64_t a = (x % mod) + 1;
        x = x*1664525u + 1013904223u;
        uint64_t b = (x % mod) + 1;
        sum += gcd(a,b);
    }
    printf("%lld\n", sum);
    return 0;
}
