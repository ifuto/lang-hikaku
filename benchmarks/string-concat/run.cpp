#include <cstdio>
#include <string>
int main(){
    int N=100000;
    std::string s;
    s.reserve(N);
    for (int i=0;i<N;i++) s.push_back('a');
    std::printf("%zu\n", s.size());
    return 0;
}
