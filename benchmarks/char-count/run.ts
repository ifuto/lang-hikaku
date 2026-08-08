let a_cnt=5000000, d_cnt=2500000, sp_cnt=1500000, other=1000000;
let s="a".repeat(a_cnt)+"0".repeat(d_cnt)+" ".repeat(sp_cnt)+"!".repeat(other);
let alpha=0,digit=0,space=0;
for (let i=0;i<s.length;i++){
    let c=s[i];
    if ((c>='a'&&c<='z')||(c>='A'&&c<='Z')) alpha++;
    else if (c>='0'&&c<='9') digit++;
    else if (c==' ') space++;
}
console.log(alpha+" "+digit+" "+space);
