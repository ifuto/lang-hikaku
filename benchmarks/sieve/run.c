#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const int N = 10000000;
    unsigned char *s = malloc((size_t)N + 1);
    memset(s, 1, (size_t)N + 1);
    s[0] = s[1] = 0;
    for (int i = 2; (long long)i * i <= N; i++) {
        if (s[i]) {
            for (long long j = (long long)i * i; j <= N; j += i)
                s[j] = 0;
        }
    }
    long long cnt = 0;
    for (int i = 0; i <= N; i++) cnt += s[i];
    printf("%lld\n", cnt);
    return 0;
}
