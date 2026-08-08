fn gcd(mut a: u64, mut b: u64)->u64{ while b!=0 { let t=a % b; a=b; b=t; } a }
fn main(){
    let mut x: u32 = 12345;
    let modu: u32 = 1000000000;
    let mut sum: i64 = 0;
    for _ in 0..5000000 {
        x = x.wrapping_mul(1664525).wrapping_add(1013904223);
        let a = (x % modu) as u64 + 1;
        x = x.wrapping_mul(1664525).wrapping_add(1013904223);
        let b = (x % modu) as u64 + 1;
        sum += gcd(a,b) as i64;
    }
    println!("{}", sum);
}
