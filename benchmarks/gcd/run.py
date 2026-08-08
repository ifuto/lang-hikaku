import math
x=12345
mod=1000000000
s=0
MASK=2**32
for _ in range(5000000):
    x=(x*1664525+1013904223)%MASK
    a=(x%mod)+1
    x=(x*1664525+1013904223)%MASK
    b=(x%mod)+1
    s+=math.gcd(a,b)
print(s)
