<?php
function gcd($a,$b){ while($b){ $t=$a%$b; $a=$b; $b=$t; } return $a; }
$x=12345;
$mod=1000000000;
$sum=0;
for ($i=0;$i<5000000;$i++){
    $x=($x*1664525+1013904223)%4294967296;
    $a=($x%$mod)+1;
    $x=($x*1664525+1013904223)%4294967296;
    $b=($x%$mod)+1;
    $sum+=gcd($a,$b);
}
echo "$sum\n";
