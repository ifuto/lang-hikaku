#include <cstdio>
#include <cstdint>
#include <numeric>
int main(){
    uint32_t x=12345;
    const uint32_t mod=1000000000;
    long long sum=0;
    for (int i=0;i<5000000;i++){
        x = x*1664525u + 1013904223u;
        uint64_t a = (x % mod) + 1;
        x = x*1664525u + 1013904223u;
        uint64_t b = (x % mod) + 1;
        sum += std::gcd(a,b);
    }
    std::printf("%lld\n", sum);
    return 0;
}
