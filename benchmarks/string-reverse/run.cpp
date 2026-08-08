#include <cstdio>
#include <string>
#include <algorithm>
int main(){
    int size=10000000;
    int reps=10;
    std::string s(size,'a');
    long long total=0;
    for (int r=0;r<reps;r++){ std::reverse(s.begin(), s.end()); total+=s.size(); }
    std::printf("%lld\n", total);
    return 0;
}
