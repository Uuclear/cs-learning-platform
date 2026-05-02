// example-03-lifetimes.rs
// 生命周期标注演示

fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        // longest函数返回两个字符串中较长的那个的引用
        result = longest(string1.as_str(), string2.as_str());
    }
    println!("最长的字符串是: {}", result);

    // 结构体中的生命周期示例
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().expect("Could not find a '.'");
    let i = ImportantExcerpt {
        part: first_sentence,
    };
    println!("重要摘录: {}", i.part);
}

// 生命周期标注：返回值的生命周期不能超过任何一个参数的生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// 结构体中的引用必须有生命周期标注
struct ImportantExcerpt<'a> {
    part: &'a str,
}