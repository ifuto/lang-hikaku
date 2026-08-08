fn main(){
    let a_cnt=5_000_000;
    let d_cnt=2_500_000;
    let sp_cnt=1_500_000;
    let other=1_000_000;
    let mut s=String::with_capacity(10_000_000);
    s.push_str(&"a".repeat(a_cnt));
    s.push_str(&"0".repeat(d_cnt));
    s.push_str(&" ".repeat(sp_cnt));
    s.push_str(&"!".repeat(other));
    let mut alpha=0i64; let mut digit=0i64; let mut space=0i64;
    for c in s.chars(){
        if c.is_ascii_alphabetic(){ alpha+=1; }
        else if c.is_ascii_digit(){ digit+=1; }
        else if c==' '{ space+=1; }
    }
    println!("{} {} {}", alpha, digit, space);
}
