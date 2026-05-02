// example-02-borrowing.rs
// 借用和引用演示

fn main() {
    let s = String::from("Hello, Rust!");

    // 不可变借用 - 只读访问
    let len = calculate_length(&s);
    println!("字符串 '{}' 的长度是 {}", s, len);

    // 可变借用 - 读写访问
    let mut s2 = String::from("Hello");
    change_string(&mut s2);
    println!("修改后的字符串: {}", s2);

    // 借用规则演示
    let mut s3 = String::from("Rust");
    let r1 = &s3; // 不可变引用1
    let r2 = &s3; // 不可变引用2
    println!("{} and {}", r1, r2);
    // 此时r1和r2离开作用域

    let r3 = &mut s3; // 现在可以创建可变引用了
    println!("{}", r3);
}

// 接收不可变引用，不获取所有权
fn calculate_length(s: &String) -> usize {
    s.len()
}

// 接收可变引用，可以修改内容
fn change_string(s: &mut String) {
    s.push_str(", World!");
}