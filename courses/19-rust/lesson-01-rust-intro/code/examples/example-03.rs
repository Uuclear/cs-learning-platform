// example-03.rs - 基本数据类型和控制流

fn main() {
    // 标量类型（Scalar Types）

    // 整数类型
    let age: u8 = 25; // 8位无符号整数 (0-255)
    let temperature: i32 = -10; // 32位有符号整数

    // 浮点数类型
    let pi: f64 = 3.14159;
    let price: f32 = 19.99;

    // 布尔类型
    let is_rust_safe = true;
    let is_hard_to_learn = false;

    // 字符类型（Unicode 标量值）
    let emoji = '🚀';
    let letter = 'A';

    println!("年龄: {}, 温度: {}", age, temperature);
    println!("π ≈ {}, 价格: ${}", pi, price);
    println!("Rust 安全吗？{}", if is_rust_safe { "是的！" } else { "不是" });
    println!("表情符号: {}, 字母: {}", emoji, letter);

    // 复合类型

    // 元组（Tuple）- 固定长度，不同类型
    let person = ("Alice", 30, true);
    println!("姓名: {}, 年龄: {}, 已婚: {}", person.0, person.1, person.2);

    // 数组（Array）- 固定长度，相同类型
    let colors = ["红", "绿", "蓝"];
    println!("第一个颜色: {}", colors[0]);

    // 控制流

    // if 表达式
    let number = 6;
    if number % 4 == 0 {
        println!("{} 能被 4 整除", number);
    } else if number % 3 == 0 {
        println!("{} 能被 3 整除", number);
    } else {
        println!("{} 不能被 4 或 3 整除", number);
    }

    // loop 循环
    let mut counter = 0;
    loop {
        counter += 1;
        if counter == 3 {
            break;
        }
        println!("循环计数: {}", counter);
    }

    // while 循环
    let mut num = 3;
    while num != 0 {
        println!("{}!", num);
        num -= 1;
    }
    println!("起飞！");

    // for 循环
    for i in 1..=5 {
        println!("计数: {}", i);
    }

    // 遍历数组
    let fruits = ["苹果", "香蕉", "橙子"];
    for fruit in fruits.iter() {
        println!("我喜欢吃 {}", fruit);
    }
}