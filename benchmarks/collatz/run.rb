N=1000000
best=1
best_len=0
(1..N).each do |i|
  n=i
  l=0
  while n!=1
    n = n.even? ? n/2 : 3*n+1
    l+=1
  end
  if l>best_len
    best_len=l
    best=i
  end
end
puts best
