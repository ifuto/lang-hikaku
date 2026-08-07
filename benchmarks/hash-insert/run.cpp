#include <cstdio>
#include <string>
#include <unordered_map>

int main() {
    const int N = 1000000;
    std::unordered_map<std::string, long long> t;
    t.reserve(N * 2);
    for (int i = 0; i < N; i++) {
        char k[16];
        std::snprintf(k, sizeof k, "k%07d", i);
        t[k] = i;
    }
    std::printf("%d\n", N);
    return 0;
}
