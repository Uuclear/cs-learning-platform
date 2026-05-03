// example-02.rs - 结构体中的生命周期：字符串引用存储

// 当结构体包含引用时，必须标注生命周期
// 这告诉编译器引用的有效期

// ❌ 这样的结构体会编译失败：
// struct ImportantExcerpt {
//     part: &str,
// }

// ✅ 正确的写法：为结构体字段添加生命周期参数
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    // 构造函数
    fn new(part: &'a str) -> ImportantExcerpt<'a> {
        ImportantExcerpt { part }
    }

    // 方法也可以使用相同的生命周期
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("注意: {}", announcement);
        self.part
    }

    // 返回一个总是有效的字符串字面量
    fn level(&self) -> &'static str {
        "初级"
    }
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().expect("无法找到句号");

    // 创建 ImportantExcerpt 实例
    let excerpt = ImportantExcerpt::new(first_sentence);
    println!("摘录的内容: {}", excerpt.part);

    // 调用方法
    let announced_part = excerpt.announce_and_return_part("这是重要摘录！");
    println!("返回的部分: {}", announced_part);

    // 'static 生命周期的例子
    println!("级别: {}", excerpt.level());

    // 注意：novel 必须在 excerpt 之后才结束生命周期
    // 否则会编译错误！
}