// solution-01.rs - 修复生命周期错误的解决方案

// 原始问题代码：
// fn main() {
//     let string1 = String::from("long string is long");
//     let result;
//     {
//         let string2 = String::from("xyz");
//         result = longest(string1.as_str(), string2.as_str());
//     }
//     println!("The longest string is {}", result);
// }

// 问题分析：string2 在内部作用域结束时被销毁，
// 但 result 试图引用它，这会导致悬空指针。

// 解决方案1：确保两个字符串的生命周期都足够长
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let string1 = String::from("long string is long");
    let string2 = String::from("xyz"); // 移到外部作用域

    let result = longest(string1.as_str(), string2.as_str());
    println!("The longest string is {}", result);

    // 现在 string1 和 string2 都在 result 使用时仍然有效
}

// 解决方案2：如果确实需要在内部作用域创建 string2，
// 可以返回所有权而不是引用
fn longest_owned(x: &str, y: &str) -> String {
    if x.len() > y.len() {
        x.to_string()
    } else {
        y.to_string()
    }
}

// 或者使用其他策略，比如只在内部作用域使用结果