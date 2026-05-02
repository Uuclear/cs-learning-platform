// solution-01.rs
// 练习1解答：实现字符串连接函数

fn concatenate_strings(s1: &str, s2: &str) -> String {
    format!("{}{}", s1, s2)
    // 或者使用：
    // let mut result = String::from(s1);
    // result.push_str(s2);
    // result
}

fn main() {
    let str1 = "Hello, ";
    let str2 = "Rust!";
    let result = concatenate_strings(str1, str2);
    println!("连接结果: {}", result);

    // 验证原始字符串仍然可用
    println!("原始字符串1: {}", str1);
    println!("原始字符串2: {}", str2);
}