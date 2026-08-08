<?php
$N=300;
$x=12345;
$a=array_fill(0,$N,array_fill(0,$N,0));
$b=array_fill(0,$N,array_fill(0,$N,0));
$c=array_fill(0,$N,array_fill(0,$N,0));
for($i=0;$i<$N;$i++) for($j=0;$j<$N;$j++){ $x=($x*1664525+1013904223)%4294967296; $a[$i][$j]=$x%100; }
for($i=0;$i<$N;$i++) for($j=0;$j<$N;$j++){ $x=($x*1664525+1013904223)%4294967296; $b[$i][$j]=$x%100; }
for($i=0;$i<$N;$i++) for($k=0;$k<$N;$k++){ $aik=$a[$i][$k]; for($j=0;$j<$N;$j++) $c[$i][$j]+=$aik*$b[$k][$j]; }
$s=0; for($i=0;$i<$N;$i++) for($j=0;$j<$N;$j++) $s+=$c[$i][$j];
echo "$s\n";
