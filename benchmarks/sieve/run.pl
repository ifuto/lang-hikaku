use strict;
use warnings;

my $N = 10_000_000;
my @s = (1) x ($N + 1);
$s[0] = $s[1] = 0;
for (my $i = 2; $i * $i <= $N; $i++) {
    if ($s[$i]) {
        for (my $j = $i * $i; $j <= $N; $j += $i) { $s[$j] = 0; }
    }
}
my $cnt = 0;
$cnt += $_ for @s;
print "$cnt\n";
