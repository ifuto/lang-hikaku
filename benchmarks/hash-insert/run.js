const N = 1000000;
const t = new Map();
for (let i = 0; i < N; i++) {
    t.set("k" + String(i).padStart(7, "0"), i);
}
console.log(N);
