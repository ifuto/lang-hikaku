sub powmod {
    my ($a,$b,$m)=@_;
    my $res=1 % $m;
    $a%=$m;
    while($b>0){
        $res=($res*$a)%$m if $b&1;
        $a=($a*$a)%$m;
        $b>>=1;
    }
    return $res;
}
my $x=12345;
my $sum=0;
my $MOD=1000000007;
for (my $i=0;$i<1000000;$i++){
    $x=($x*1664525+1013904223)%4294967296;
    my $a=($x%100000)+2;
    $x=($x*1664525+1013904223)%4294967296;
    my $b=($x%1000)+2;
    $sum+=powmod($a,$b,$MOD);
}
print "$sum\n";
