fn main() {
    // 元组解构
    let point = (3, 5);
    match point {
        (0, 0) => println!("原点"),
        (0, y) => println!("在Y轴上，y = {}", y),
        (x, 0) => println!("在X轴上，x = {}", x),
        (x, y) => println!("在({}, {})点", x, y),
    }

    // 结构体解构
    struct Point {
        x: i32,
        y: i32,
    }

    let p = Point { x: 0, y: 7 };
    match p {
        Point { x: 0, y: 0 } => println!("结构体原点"),
        Point { x: 0, y } => println!("结构体Y轴，y = {}", y),
        Point { x, y: 0 } => println!("结构体X轴，x = {}", x),
        Point { x, y } => println!("结构体点({}, {})", x, y),
    }

    // 使用..忽略部分字段
    struct Color {
        red: u8,
        green: u8,
        blue: u8,
        alpha: u8,
    }

    let color = Color { red: 255, green: 165, blue: 0, alpha: 255 };
    match color {
        Color { red: 255, green: _, blue: _, alpha: _ } => println!("这是红色系！"),
        Color { red: _, green: 255, blue: _, alpha: _ } => println!("这是绿色系！"),
        Color { red, green, blue, .. } => println!("RGB: ({}, {}, {})", red, green, blue),
    }
}