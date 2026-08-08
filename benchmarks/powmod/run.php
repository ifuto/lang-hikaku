<?php
function powmod($a,$b,$m){
    $res=1 % $m;
    $a%=$m;
    while($b>0){
        if ($b&1) $res=($res*$a)%$m;
        $a=($a*$a)%$m;
        $b>>=1;
    }
    return $res;
}
$x=12345;
$sum=0;
$MOD=1000000007;
for ($i=0;$i<1000000;$i++){
    $x=($x*1664525+1013904223)%4294967296;
    $a=($x%100000)+2;
    $x=($x*1664525+1013904223)%4294967296;
    $b=($x%1000)+2;
    $sum+=powmod($a,$b,$MOD);
}
echo "$sum\n";
