a_cnt=5000000
d_cnt=2500000
sp_cnt=1500000
other=1000000
s="a"*a_cnt + "0"*d_cnt + " "*sp_cnt + "!"*other
alpha=digit=space=0
s.each_char do |c|
  if ('a'..'z').include?(c) || ('A'..'Z').include?(c)
    alpha+=1
  elsif ('0'..'9').include?(c)
    digit+=1
  elsif c==' '
    space+=1
  end
end
puts "#{alpha} #{digit} #{space}"
