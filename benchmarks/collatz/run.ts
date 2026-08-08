let N=1000000;
let best=1;
let best_len=0;
for (let i=1;i<=N;i++){
    let n=i;
    let len=0;
    while(n!==1){ if (n%2===0) n/=2; else n=3*n+1; len++; }
    if (len>best_len){ best_len=len; best=i; }
}
console.log(best);
