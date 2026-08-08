fn powmod(mut a: u64, mut b: u64, m: u64)->u64{
    let mut res=1 % m;
    a%=m;
    while b>0 { if b&1==1 { res=(res*a)%m; } a=(a*a)%m; b>>=1; }
    res
}
fn main(){
    let mut x: u32 = 12345;
    let mut sum: u64 = 0;
    const MOD: u64 = 1000000007;
    for _ in 0..1000000 {
        x = x.wrapping_mul(1664525).wrapping_add(1013904223);
        let a = (x % 100000) as u64 + 2;
        x = x.wrapping_mul(1664525).wrapping_add(1013904223);
        let b = (x % 1000) as u64 + 2;
        sum += powmod(a,b,MOD);
    }
    println!("{}", sum);
}
