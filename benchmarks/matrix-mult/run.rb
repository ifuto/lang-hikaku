N=300
x=12345
MASK=2**32
a=Array.new(N){Array.new(N,0)}
b=Array.new(N){Array.new(N,0)}
c=Array.new(N){Array.new(N,0)}
N.times do |i|
  N.times do |j|
    x=(x*1664525+1013904223)%MASK
    a[i][j]=x%100
  end
end
N.times do |i|
  N.times do |j|
    x=(x*1664525+1013904223)%MASK
    b[i][j]=x%100
  end
end
N.times do |i|
  N.times do |k|
    aik=a[i][k]
    N.times do |j|
      c[i][j]+=aik*b[k][j]
    end
  end
end
s=0
N.times do |i|
  N.times do |j|
    s+=c[i][j]
  end
end
puts s
