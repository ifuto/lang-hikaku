function gcd(a,b){ while(b){ let t=a%b; a=b; b=t; } return a; }
let x=12345>>>0;
const mod=1000000000;
let sum=0;
for (let i=0;i<5000000;i++){
    x=(Math.imul(x,1664525)+1013904223)>>>0;
    let a=(x%mod)+1;
    x=(Math.imul(x,1664525)+1013904223)>>>0;
    let b=(x%mod)+1;
    sum+=gcd(a,b);
}
console.log(sum);
