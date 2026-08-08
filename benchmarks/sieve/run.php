<?php
$N = 10000000;
$s = array_fill(0, $N+1, 1);
$s[0]=0; $s[1]=0;
for ($i=2; $i*$i <= $N; $i++) {
    if ($s[$i]) {
        for ($j=$i*$i; $j<=$N; $j+=$i) $s[$j]=0;
    }
}
$cnt=0;
foreach ($s as $v) $cnt+=$v;
echo $cnt . "\n";
