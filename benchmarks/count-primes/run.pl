sub is_prime {
    my $n=shift;
    return 0 if $n<2;
    return $n==2 if $n%2==0;
    for (my $d=3; $d*$d<=$n; $d+=2) {
        return 0 if $n % $d==0;
    }
    return 1;
}
my $N=300000;
my $cnt=0;
for my $i (2..$N) { $cnt++ if is_prime($i); }
print "$cnt\n";
