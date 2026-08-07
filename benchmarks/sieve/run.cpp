#include <cstdio>
#include <vector>

int main() {
    const int N = 10000000;
    std::vector<unsigned char> s(N + 1, 1);
    s[0] = s[1] = 0;
    for (int i = 2; (long long)i * i <= N; i++) {
        if (s[i]) {
            for (long long j = (long long)i * i; j <= N; j += i)
                s[j] = 0;
        }
    }
    long long cnt = 0;
    for (int i = 0; i <= N; i++) cnt += s[i];
    std::printf("%lld\n", cnt);
    return 0;
}
