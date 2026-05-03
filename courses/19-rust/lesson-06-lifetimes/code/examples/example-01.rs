// example-01.rs - 生命周期标注基础：最长公共子串函数

// 这个例子展示了为什么我们需要生命周期标注
// 编译器需要知道返回的引用应该和哪个输入参数的生命周期一样长

// ❌ 这样的代码会编译失败：
// fn longest(x: &str, y: &str) -> &str {
//     if x.len() > y.len() { x } else { y }
// }

// ✅ 正确的写法：使用生命周期参数 'a
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";

    // 调用 longest 函数
    let result = longest(string1.as_str(), string2);
    println!("最长的字符串是: {}", result);

    // 另一个例子：确保引用的有效性
    {
        let string3 = String::from("hello");
        let result2 = longest(string1.as_str(), string3.as_str());
        println!("最长的字符串是: {}", result2);
        // string3 在这里结束生命周期，但 result2 仍然有效，
        // 因为它实际上指向的是 string1（更长的那个）
    }

    // 这里 string1 仍然有效，所以之前的 result 也有效
    println!("原始结果仍然有效: {}", result);
}