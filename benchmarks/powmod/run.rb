def powmod(a,b,m)
  res=1 % m
  a%=m
  while b>0
    res=(res*a)%m if (b&1)==1
    a=(a*a)%m
    b>>=1
  end
  res
end
x=12345
s=0
MOD=1000000007
MASK=2**32
1000000.times do
  x=(x*1664525+1013904223)%MASK
  a=(x%100000)+2
  x=(x*1664525+1013904223)%MASK
  b=(x%1000)+2
  s+=powmod(a,b,MOD)
end
puts s
