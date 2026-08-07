#include <cstdio>
#include <cstdint>

constexpr int N = 300;
static long long a[N][N], b[N][N], c[N][N];

int main() {
    uint32_t x = 12345;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            x = x * 1664525u + 1013904223u;
            a[i][j] = x % 100;
        }
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            x = x * 1664525u + 1013904223u;
            b[i][j] = x % 100;
        }
    for (int i = 0; i < N; i++)
        for (int k = 0; k < N; k++) {
            long long aik = a[i][k];
            for (int j = 0; j < N; j++)
                c[i][j] += aik * b[k][j];
        }
    long long s = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            s += c[i][j];
    std::printf("%lld\n", s);
    return 0;
}
