def is_prime(n)
  return false if n<2
  return n==2 if n%2==0
  d=3
  while d*d<=n
    return false if n%d==0
    d+=2
  end
  true
end
N=300000
cnt=0
(2..N).each{|i| cnt+=1 if is_prime(i)}
puts cnt
