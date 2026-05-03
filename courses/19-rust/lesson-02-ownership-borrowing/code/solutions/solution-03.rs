// solution-03.rs - 悬垂引用与生命周期解决方案

fn main() {
    // 正确处理字符串切片
    let sentence = String::from("The quick brown fox jumps over the lazy dog");
    let first = first_word(&sentence);
    println!("First word is: {}", first);

    // 安全地处理多个切片
    let words = get_all_words(&sentence);
    for (i, word) in words.iter().enumerate() {
        println!("Word {}: {}", i + 1, word);
    }

    // 处理结构体中的引用（需要显式生命周期）
    let s = String::from("hello");
    let important = ImportantExcerpt { part: &s };
    println!("Important part: {}", important.part);

    // 使用返回所有权的函数避免悬垂引用
    let owned_string = create_string();
    println!("Created string: {}", owned_string);
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

fn get_all_words(s: &str) -> Vec<&str> {
    s.split_whitespace().collect()
}

// 需要生命周期注解的结构体
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn create_string() -> String {
    String::from("I am owned!")
}

// 错误示例的正确版本
fn safe_dangle() -> String {
    String::from("This is safe because we return ownership")
}
