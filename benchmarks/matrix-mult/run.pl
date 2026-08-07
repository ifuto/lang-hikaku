use strict;
use warnings;

my $N = 300;
my $x = 12345;
my @a;
my @b;
my @c;

for my $i (0 .. $N - 1) {
    for my $j (0 .. $N - 1) {
        $x = ($x * 1664525 + 1013904223) % 4294967296;
        $a[$i][$j] = $x % 100;
    }
}
for my $i (0 .. $N - 1) {
    for my $j (0 .. $N - 1) {
        $x = ($x * 1664525 + 1013904223) % 4294967296;
        $b[$i][$j] = $x % 100;
    }
}
for my $i (0 .. $N - 1) {
    for my $k (0 .. $N - 1) {
        my $aik = $a[$i][$k];
        for my $j (0 .. $N - 1) {
            $c[$i][$j] += $aik * $b[$k][$j];
        }
    }
}
my $s = 0;
for my $i (0 .. $N - 1) {
    for my $j (0 .. $N - 1) {
        $s += $c[$i][$j];
    }
}
print "$s\n";
