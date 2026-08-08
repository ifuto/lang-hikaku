size=10000000
reps=10
s="a"*size
total=0
for _ in range(reps):
    s=s[::-1]
    total+=len(s)
print(total)
