<?php
$N=1000000;
$t=[];
for ($i=0;$i<$N;$i++) {
    $t[sprintf("k%07d", $i)]=$i;
}
echo "$N\n";
