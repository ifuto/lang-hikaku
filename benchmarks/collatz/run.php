<?php
$N=1000000;
$best=1;
$best_len=0;
for ($i=1;$i<=$N;$i++){
    $n=$i;
    $len=0;
    while($n!=1){ if ($n%2==0) $n/=2; else $n=3*$n+1; $len++; }
    if ($len>$best_len){ $best_len=$len; $best=$i; }
}
echo "$best\n";
