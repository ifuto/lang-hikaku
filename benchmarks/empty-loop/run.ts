let N:number=1000000000;
let s:bigint=0n;
for (let i=0;i<N;i++) s+=BigInt(i);
console.log(s.toString());
