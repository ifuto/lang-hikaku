x=12345
mod=1000000000
s=0
MASK=2**32
5000000.times do
  x=(x*1664525+1013904223)%MASK
  a=(x%mod)+1
  x=(x*1664525+1013904223)%MASK
  b=(x%mod)+1
  s+=a.gcd(b)
end
puts s
