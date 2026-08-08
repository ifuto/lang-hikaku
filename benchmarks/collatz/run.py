N=1000000
best=1
best_len=0
for i in range(1,N+1):
    n=i
    l=0
    while n!=1:
        if n%2==0:
            n//=2
        else:
            n=3*n+1
        l+=1
    if l>best_len:
        best_len=l
        best=i
print(best)
