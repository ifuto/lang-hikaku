const N = 300;
let x = 12345;
const a = new Int32Array(N * N);
const b = new Int32Array(N * N);
const c = new Float64Array(N * N);

for (let i = 0; i < N; i++)
    for (let j = 0; j < N; j++) {
        x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
        a[i * N + j] = x % 100;
    }
for (let i = 0; i < N; i++)
    for (let j = 0; j < N; j++) {
        x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
        b[i * N + j] = x % 100;
    }
for (let i = 0; i < N; i++)
    for (let k = 0; k < N; k++) {
        const aik = a[i * N + k];
        for (let j = 0; j < N; j++)
            c[i * N + j] += aik * b[k * N + j];
    }
let s = 0;
for (let i = 0; i < N * N; i++) s += c[i];
console.log(s);
