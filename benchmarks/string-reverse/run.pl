my $size=10000000;
my $reps=10;
my $s="a" x $size;
my $total=0;
for (my $r=0;$r<$reps;$r++){ $s=reverse($s); $total+=length($s); }
print "$total\n";
