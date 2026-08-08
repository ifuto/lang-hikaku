fn main(){
    let size=10_000_000;
    let reps=10;
    let mut s="a".repeat(size);
    let mut total: i64=0;
    for _ in 0..reps {
        s = s.chars().rev().collect();
        total+= s.len() as i64;
    }
    println!("{}", total);
}
