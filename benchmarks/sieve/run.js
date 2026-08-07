const N = 10000000;
const s = new Uint8Array(N + 1).fill(1);
s[0] = 0; s[1] = 0;
for (let i = 2; i * i <= N; i++) {
    if (s[i]) {
        for (let j = i * i; j <= N; j += i) s[j] = 0;
    }
}
let cnt = 0;
for (let i = 0; i <= N; i++) cnt += s[i];
console.log(cnt);
