def is_prime(n):
    if n<2:
        return False
    if n%2==0:
        return n==2
    d=3
    while d*d<=n:
        if n%d==0:
            return False
        d+=2
    return True

N=300000
cnt=0
for i in range(2,N+1):
    if is_prime(i):
        cnt+=1
print(cnt)
