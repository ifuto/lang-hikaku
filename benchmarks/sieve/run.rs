fn main() {
    const N: usize = 10_000_000;
    let mut s = vec![1u8; N+1];
    s[0] = 0; s[1] = 0;
    let limit = (N as f64).sqrt() as usize;
    for i in 2..=limit {
        if s[i] == 1 {
            let mut j = i*i;
            while j <= N {
                s[j] = 0;
                j += i;
            }
        }
    }
    let cnt: usize = s.iter().map(|&v| v as usize).sum();
    println!("{}", cnt);
}
