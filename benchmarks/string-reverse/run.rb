size=10000000
reps=10
s="a"*size
total=0
reps.times do
  s=s.reverse
  total+=s.length
end
puts total
