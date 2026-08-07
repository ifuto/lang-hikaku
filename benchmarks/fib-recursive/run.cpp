#include <cstdio>

long long fib(int n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main() {
    std::printf("%lld\n", fib(35));
    return 0;
}
