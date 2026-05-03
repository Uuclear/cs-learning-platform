// example-02.rs - 变量、常量和可变性演示

fn main() {
    // Rust 中的变量默认是不可变的（immutable）
    let x = 5;
    println!("x 的值是: {}", x);

    // 如果尝试修改不可变变量，会编译错误
    // x = 6; // 这行会报错！

    // 使用 mut 关键字声明可变变量
    let mut y = 10;
    println!("y 的初始值是: {}", y);
    y = 15; // 这是可以的！
    println!("y 的新值是: {}", y);

    // 常量使用 const 声明，必须指定类型
    // 常量在编译时计算，可以在全局作用域声明
    const MAX_POINTS: u32 = 100_000;
    println!("最大分数是: {}", MAX_POINTS);

    // 变量遮蔽（shadowing）- 重新声明同名变量
    let z = 5;
    println!("z 的第一个值是: {}", z);

    let z = z + 1; // 遮蔽了之前的 z
    println!("z 的第二个值是: {}", z);

    let z = z * 2; // 再次遮蔽
    println!("z 的最终值是: {}", z);
}