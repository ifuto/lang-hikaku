def powmod(a,b,m):
    res=1 % m
    a%=m
    while b>0:
        if b&1:
            res=(res*a)%m
        a=(a*a)%m
        b>>=1
    return res

x=12345
s=0
MOD=1000000007
MASK=2**32
for _ in range(1000000):
    x=(x*1664525+1013904223)%MASK
    a=(x%100000)+2
    x=(x*1664525+1013904223)%MASK
    b=(x%1000)+2
    s+=powmod(a,b,MOD)
print(s)
