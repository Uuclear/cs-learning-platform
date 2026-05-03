// example-01.rs - Hello World 程序详解
// 这是 Rust 中最经典的入门程序

// main 函数是程序的入口点
fn main() {
    // println! 是一个宏（macro），不是函数
    // 宏在编译时展开，提供零成本抽象
    // ! 表示这是一个宏调用
    println!("Hello, world!");

    // 我们也可以打印更复杂的信息
    println!("欢迎来到 Rust 编程世界！");
    println!("Rust 让系统编程既安全又高效！");
}