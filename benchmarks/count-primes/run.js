function isPrime(n){
    if (n<2) return false;
    if (n%2===0) return n===2;
    for (let d=3; d*d<=n; d+=2) if (n%d===0) return false;
    return true;
}
let N=300000;
let cnt=0;
for (let i=2;i<=N;i++) if (isPrime(i)) cnt++;
console.log(cnt);
