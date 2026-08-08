function powmod(a,b,m){
    let res=1n % BigInt(m);
    let am=BigInt(a) % BigInt(m);
    let bb=BigInt(b);
    let mm=BigInt(m);
    while(bb>0n){
        if (bb & 1n) res=(res*am)%mm;
        am=(am*am)%mm;
        bb>>=1n;
    }
    return res;
}
let x=12345>>>0;
let sum=0n;
const MOD=1000000007;
for (let i=0;i<1000000;i++){
    x=(Math.imul(x,1664525)+1013904223)>>>0;
    let a=(x%100000)+2;
    x=(Math.imul(x,1664525)+1013904223)>>>0;
    let b=(x%1000)+2;
    sum+=powmod(a,b,MOD);
}
console.log(sum.toString());
