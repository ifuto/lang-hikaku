fn main(){
    let nmax=1000000;
    let mut best=1;
    let mut best_len=0;
    for i in 1..=nmax {
        let mut n=i as i64;
        let mut len=0;
        while n!=1 { if n%2==0 { n/=2; } else { n=3*n+1; } len+=1; }
        if len>best_len { best_len=len; best=i; }
    }
    println!("{}", best);
}
