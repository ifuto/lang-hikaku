use strict;
use warnings;
sub gcd {
    my ($a,$b)=@_;
    while($b){ ($a,$b)=($b,$a % $b); }
    return $a;
}
my $x=12345;
my $mod=1000000000;
my $sum=0;
for (my $i=0;$i<5000000;$i++){
    $x=($x*1664525+1013904223)%4294967296;
    my $a=($x%$mod)+1;
    $x=($x*1664525+1013904223)%4294967296;
    my $b=($x%$mod)+1;
    $sum+=gcd($a,$b);
}
print "$sum\n";
