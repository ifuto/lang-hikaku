N=1_000_000
t={}
(0...N).each do |i|
  t[sprintf("k%07d", i)]=i
end
puts N
