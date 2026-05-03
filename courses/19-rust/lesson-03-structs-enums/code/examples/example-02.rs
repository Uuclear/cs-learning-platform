// example-02.rs - 枚举与 match 模式匹配（Message 类型）

// 定义一个枚举，每个变体可以携带不同类型的数据
enum Message {
    Quit,                    // 不携带数据
    Move { x: i32, y: i32 }, // 携带匿名结构体
    Write(String),          // 携带字符串
    ChangeColor(i32, i32, i32), // 携带元组
}

// 为 Message 枚举实现方法
impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("退出程序"),
            Message::Move { x, y } => println!("移动到位置 ({}, {})", x, y),
            Message::Write(text) => println!("写入文本: {}", text),
            Message::ChangeColor(r, g, b) => println!("改变颜色为 RGB({}, {}, {})", r, g, b),
        }
    }
}

// 另一个枚举示例：WebEvent
enum WebEvent {
    PageLoad,
    PageUnload,
    KeyPress(char),
    Paste(String),
    Click { x: i64, y: i64 },
}

fn inspect(event: WebEvent) {
    match event {
        WebEvent::PageLoad => println!("页面加载"),
        WebEvent::PageUnload => println!("页面卸载"),
        WebEvent::KeyPress(c) => println!("按键: {}", c),
        WebEvent::Paste(s) => println!("粘贴内容: {}", s),
        WebEvent::Click { x, y } => println!("点击位置: ({}, {})", x, y),
    }
}

fn main() {
    // 创建不同的 Message 实例
    let messages = vec![
        Message::Quit,
        Message::Move { x: 10, y: 20 },
        Message::Write(String::from("Hello, Rust!")),
        Message::ChangeColor(255, 0, 0),
    ];

    // 调用每个消息的 call 方法
    for msg in messages {
        msg.call();
    }

    println!("\n--- Web Event 示例 ---");

    // 使用 WebEvent
    let events = vec![
        WebEvent::PageLoad,
        WebEvent::KeyPress('a'),
        WebEvent::Paste(String::from("粘贴的文本")),
        WebEvent::Click { x: 100, y: 200 },
    ];

    for event in events {
        inspect(event);
    }
}