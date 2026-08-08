my $a_cnt=5000000; my $d_cnt=2500000; my $sp_cnt=1500000; my $other=1000000;
my $s="a" x $a_cnt . "0" x $d_cnt . " " x $sp_cnt . "!" x $other;
my ($alpha,$digit,$space)=(0,0,0);
for my $c (split //, $s){
    if (($c ge 'a' && $c le 'z')||($c ge 'A' && $c le 'Z')){ $alpha++; }
    elsif ($c ge '0' && $c le '9'){ $digit++; }
    elsif ($c eq ' '){ $space++; }
}
print "$alpha $digit $space\n";
