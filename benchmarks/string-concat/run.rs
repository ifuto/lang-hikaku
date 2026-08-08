fn main(){
    let n=100000;
    let mut s=String::with_capacity(n);
    for _ in 0..n { s.push('a'); }
    println!("{}", s.len());
}
