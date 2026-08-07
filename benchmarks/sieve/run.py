N = 10_000_000
s = bytearray(b"\x01") * (N + 1)
s[0] = s[1] = 0
i = 2
while i * i <= N:
    if s[i]:
        for j in range(i * i, N + 1, i):
            s[j] = 0
    i += 1
print(sum(s))
