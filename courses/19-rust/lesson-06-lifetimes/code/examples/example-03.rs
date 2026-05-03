// example-03.rs - 生命周期省略规则演示

// Rust 有三条生命周期省略规则，让我们看看它们如何工作

// 规则1：每个引用参数都有自己的生命周期参数
// fn foo(s: &str) -> &str  // 实际上是 fn foo<'a>(s: &'a str) -> &'a str

// 规则2：如果只有一个输入生命周期参数，那么它被赋予所有输出生命周期参数
fn first_word(s: &str) -> &str {
    // 这里不需要显式标注，因为只有一个输入引用
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}

// 规则3：如果有多个输入生命周期参数，但其中一个是 &self 或 &mut self，
// 那么 self 的生命周期被赋予所有输出生命周期参数
struct TextProcessor<'a> {
    text: &'a str,
}

impl<'a> TextProcessor<'a> {
    fn new(text: &'a str) -> Self {
        TextProcessor { text }
    }

    // 这里返回的引用自动获得与 self 相同的生命周期
    fn get_text(&self) -> &str {
        self.text
    }

    // 多个参数的情况 - 需要显式标注
    fn compare_with<'b>(&self, other: &'b str) -> &'a str {
        if self.text.len() > other.len() {
            self.text
        } else {
            // 这里不能返回 other，因为它的生命周期 'b 可能比 'a 短
            // 编译器会报错！
            self.text // 所以我们总是返回 self.text
        }
    }
}

// 没有省略规则适用的情况 - 需要显式标注
fn longest_str<'a, 'b>(x: &'a str, y: &'b str) -> &'a str
where
    'b: 'a  // 'b 至少和 'a 一样长
{
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let s = String::from("Hello world this is a test");

    // 规则1和2的应用
    let word = first_word(&s);
    println!("第一个单词: {}", word);

    // 规则3的应用
    let processor = TextProcessor::new(&s);
    let text = processor.get_text();
    println!("处理器中的文本: {}", text);

    let other = "short";
    let result = processor.compare_with(other);
    println!("比较结果: {}", result);

    // 显式生命周期标注
    let long_string = "this is a very long string indeed";
    let short_string = "hi";
    let longest_result = longest_str(long_string, short_string);
    println!("最长字符串: {}", longest_result);
}