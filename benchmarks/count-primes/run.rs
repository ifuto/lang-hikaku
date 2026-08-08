fn is_prime(n: i32)->bool{
    if n<2 {return false}
    if n%2==0 {return n==2}
    let mut d=3;
    while (d as i64)*(d as i64) <= n as i64 {
        if n % d ==0 {return false}
        d+=2;
    }
    true
}
fn main(){
    let n=300000;
    let mut cnt=0;
    for i in 2..=n { if is_prime(i) {cnt+=1;} }
    println!("{}", cnt);
}
