use std::collections::HashMap;
fn main() {
    const N: usize = 1_000_000;
    let mut t: HashMap<String, i32> = HashMap::with_capacity(N*2);
    for i in 0..N {
        t.insert(format!("k{:07}", i), i as i32);
    }
    println!("{}", N);
}
