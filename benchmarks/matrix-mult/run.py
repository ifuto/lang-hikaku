N = 300
x = 12345
MASK = 2**32

a = [[0] * N for _ in range(N)]
b = [[0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        x = (x * 1664525 + 1013904223) % MASK
        a[i][j] = x % 100
for i in range(N):
    for j in range(N):
        x = (x * 1664525 + 1013904223) % MASK
        b[i][j] = x % 100

c = [[0] * N for _ in range(N)]
for i in range(N):
    ci = c[i]
    for k in range(N):
        aik = a[i][k]
        bk = b[k]
        for j in range(N):
            ci[j] += aik * bk[j]

print(sum(sum(row) for row in c))
