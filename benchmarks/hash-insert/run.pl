use strict;
use warnings;

my $N = 1_000_000;
my %t;
for my $i (0 .. $N - 1) {
    $t{sprintf("k%07d", $i)} = $i;
}
print "$N\n";
