#include <cstdio>
#include <string>
int main(){
    int a_cnt=5000000, d_cnt=2500000, sp_cnt=1500000, other=1000000;
    std::string s;
    s.reserve(10000000);
    s.append(a_cnt,'a');
    s.append(d_cnt,'0');
    s.append(sp_cnt,' ');
    s.append(other,'!');
    long long alpha=0,digit=0,space=0;
    for(char c: s){
        if ((c>='a'&&c<='z')||(c>='A'&&c<='Z')) alpha++;
        else if (c>='0'&&c<='9') digit++;
        else if (c==' ') space++;
    }
    std::printf("%lld %lld %lld\n", alpha, digit, space);
    return 0;
}
