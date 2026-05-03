// solution-02.rs - 变量、常量和可变性演示（解决方案）

fn main() {
    let x = 5;
    println!("x 的值是: {}", x);

    let mut y = 10;
    println!("y 的初始值是: {}", y);
    y = 15;
    println!("y 的新值是: {}", y);

    const MAX_POINTS: u32 = 100_000;
    println!("最大分数是: {}", MAX_POINTS);

    let z = 5;
    println!("z 的第一个值是: {}", z);

    let z = z + 1;
    println!("z 的第二个值是: {}", z);

    let z = z * 2;
    println!("z 的最终值是: {}", z);
}