// example-03.rs - Option 和 Result 的常见用法

// Option 枚举示例
fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

fn find_user_by_id(id: u32) -> Option<String> {
    match id {
        1 => Some(String::from("Alice")),
        2 => Some(String::from("Bob")),
        3 => Some(String::from("Charlie")),
        _ => None,
    }
}

// Result 枚举示例
fn parse_number(text: &str) -> Result<i32, String> {
    match text.parse::<i32>() {
        Ok(num) => Ok(num),
        Err(_) => Err(format!("无法将 '{}' 解析为数字", text)),
    }
}

fn safe_divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err(String::from("除数不能为零"))
    } else {
        Ok(a / b)
    }
}

// 使用 Option 的不同方式
fn demonstrate_option_usage() {
    println!("=== Option 用法演示 ===");

    // 使用 match 处理 Option
    let result1 = divide(10.0, 2.0);
    match result1 {
        Some(value) => println!("10.0 / 2.0 = {}", value),
        None => println!("除法失败"),
    }

    let result2 = divide(10.0, 0.0);
    match result2 {
        Some(value) => println!("10.0 / 0.0 = {}", value),
        None => println!("10.0 / 0.0 失败（除零错误）"),
    }

    // 使用 if let
    if let Some(username) = find_user_by_id(1) {
        println!("找到用户: {}", username);
    }

    if let Some(username) = find_user_by_id(999) {
        println!("找到用户: {}", username);
    } else {
        println!("未找到 ID 为 999 的用户");
    }

    // 使用 unwrap_or 提供默认值
    let user_name = find_user_by_id(2).unwrap_or_else(|| String::from("未知用户"));
    println!("用户名称: {}", user_name);

    let unknown_user = find_user_by_id(999).unwrap_or_else(|| String::from("访客"));
    println!("未知用户: {}", unknown_user);
}

// 使用 Result 的不同方式
fn demonstrate_result_usage() {
    println!("\n=== Result 用法演示 ===");

    // 使用 match 处理 Result
    let num1 = parse_number("42");
    match num1 {
        Ok(num) => println!("成功解析: {}", num),
        Err(e) => println!("解析错误: {}", e),
    }

    let num2 = parse_number("abc");
    match num2 {
        Ok(num) => println!("成功解析: {}", num),
        Err(e) => println!("解析错误: {}", e),
    }

    // 使用 ? 操作符（在函数中）
    let division_result = perform_calculations();
    match division_result {
        Ok(result) => println!("计算结果: {}", result),
        Err(e) => println!("计算错误: {}", e),
    }
}

// 使用 ? 操作符的函数
fn perform_calculations() -> Result<i32, String> {
    let a = parse_number("10")?;
    let b = parse_number("2")?;
    let c = safe_divide(a, b)?;
    Ok(c * 3)
}

fn main() {
    demonstrate_option_usage();
    demonstrate_result_usage();
}