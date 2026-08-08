fn main(){
    let n: i64 = 1000000000;
    let mut s: i64 = 0;
    for i in 0..n { s+=i; }
    println!("{}", s);
}
