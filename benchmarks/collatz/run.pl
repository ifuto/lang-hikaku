my $N=1000000;
my $best=1;
my $best_len=0;
for my $i (1..$N){
    my $n=$i;
    my $len=0;
    while($n!=1){ if ($n%2==0){ $n/=2; } else { $n=3*$n+1; } $len++; }
    if ($len>$best_len){ $best_len=$len; $best=$i; }
}
print "$best\n";
