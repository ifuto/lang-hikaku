fn main() {
    const N: usize = 300;
    let mut x: u32 = 12345;
    let mut a = vec![vec![0i64; N]; N];
    let mut b = vec![vec![0i64; N]; N];
    let mut c = vec![vec![0i64; N]; N];
    for i in 0..N {
        for j in 0..N {
            x = x.wrapping_mul(1664525).wrapping_add(1013904223);
            a[i][j] = (x % 100) as i64;
        }
    }
    for i in 0..N {
        for j in 0..N {
            x = x.wrapping_mul(1664525).wrapping_add(1013904223);
            b[i][j] = (x % 100) as i64;
        }
    }
    for i in 0..N {
        for k in 0..N {
            let aik = a[i][k];
            for j in 0..N {
                c[i][j] += aik * b[k][j];
            }
        }
    }
    let mut s: i64 = 0;
    for i in 0..N { for j in 0..N { s += c[i][j]; } }
    println!("{}", s);
}
