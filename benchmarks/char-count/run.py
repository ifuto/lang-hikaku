a_cnt=5000000
d_cnt=2500000
sp_cnt=1500000
other=1000000
s="a"*a_cnt + "0"*d_cnt + " "*sp_cnt + "!"*other
alpha=digit=space=0
for c in s:
    if ('a'<=c<='z') or ('A'<=c<='Z'):
        alpha+=1
    elif '0'<=c<='9':
        digit+=1
    elif c==' ':
        space+=1
print(f"{alpha} {digit} {space}")
