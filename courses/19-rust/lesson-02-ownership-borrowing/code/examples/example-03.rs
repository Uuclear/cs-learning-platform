// example-03.rs - 悬垂引用与作用域演示

fn main() {
    // 正确的引用使用
    let s = String::from("hello");
    let r = &s; // r 是对 s 的引用
    println!("Reference: {}", r);
    // s 和 r 都在作用域内，所以这是安全的

    // 尝试创建悬垂引用（会被编译器阻止）
    // let r2 = dangle(); // error: dangling reference

    // 字符串切片的例子
    let my_string = String::from("hello world");
    let word = first_word(&my_string[..]); // 传递字符串切片
    println!("First word: {}", word);

    // 注意：在获取了切片引用后，不能再修改原字符串
    // my_string.clear(); // error: cannot borrow `my_string` as mutable because it is also borrowed as immutable
}

// 这个函数试图返回一个悬垂引用
fn dangle() -> &String {
    let s = String::from("hello");
    &s // error: `s` does not live long enough
    // s 在这里离开作用域并被 drop，所以返回的引用指向无效内存
}

// 正确的版本：返回所有权而不是引用
fn no_dangle() -> String {
    let s = String::from("hello");
    s // 返回所有权，不是引用
}

fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
