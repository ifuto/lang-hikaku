<?php
$size=10000000;
$reps=10;
$s=str_repeat("a",$size);
$total=0;
for ($r=0;$r<$reps;$r++){ $s=strrev($s); $total+=strlen($s); }
echo "$total\n";
