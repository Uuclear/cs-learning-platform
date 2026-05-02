// example-01-ownership.rs
// 所有权规则演示

fn main() {
    // 字符串字面量存储在程序二进制中，不需要动态分配
    let s1 = "Hello";

    // String类型在堆上分配内存
    let s2 = String::from("World");

    // 将s2的所有权转移给s3，s2不再可用
    let s3 = s2;

    println!("s1: {}", s1);
    // println!("s2: {}", s2); // 这行会编译错误！s2已经失效了

    println!("s3: {}", s3);

    // 函数调用也会转移所有权
    takes_ownership(s3);
    // println!("s3: {}", s3); // 这行也会编译错误！
}

fn takes_ownership(s: String) {
    println!("在函数中: {}", s);
    // s在这里离开作用域，内存被自动释放
}