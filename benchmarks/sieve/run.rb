N = 10_000_000
s = Array.new(N+1, 1)
s[0]=0; s[1]=0
i=2
while i*i <= N
  if s[i]==1
    j=i*i
    while j<=N
      s[j]=0
      j+=i
    end
  end
  i+=1
end
cnt=0
s.each{|v| cnt+=v}
puts cnt
