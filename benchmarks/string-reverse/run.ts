let size=10000000;
let reps=10;
let s="a".repeat(size);
let total=0;
for (let r=0;r<reps;r++){
    s=s.split('').reverse().join('');
    total+=s.length;
}
console.log(total);
