<?php
$a_cnt=5000000; $d_cnt=2500000; $sp_cnt=1500000; $other=1000000;
$s=str_repeat("a",$a_cnt).str_repeat("0",$d_cnt).str_repeat(" ",$sp_cnt).str_repeat("!",$other);
$alpha=$digit=$space=0;
for ($i=0;$i<strlen($s);$i++){
    $c=$s[$i];
    if (($c>='a'&&$c<='z')||($c>='A'&&$c<='Z')) $alpha++;
    else if ($c>='0'&&$c<='9') $digit++;
    else if ($c==' ') $space++;
}
echo "$alpha $digit $space\n";
