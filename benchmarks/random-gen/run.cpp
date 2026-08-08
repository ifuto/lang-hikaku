#include <cstdio>
#include <cstdint>
int main(){
    uint32_t x=12345;
    uint64_t sum=0;
    for (int i=0;i<50000000;i++){
        x = x*1664525u + 1013904223u;
        sum += x % 100;
    }
    std::printf("%llu\n", (unsigned long long)sum);
    return 0;
}
