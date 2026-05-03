// solution-01.rs - Result 类型与 match/ ? 处理（完整解决方案）

use std::fs;
use std::io;
use std::num::ParseIntError;

// 基本的 Result 使用
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("除数不能为零".to_string())
    } else {
        Ok(a / b)
    }
}

// 使用 match 处理 Result
fn handle_division_with_match() {
    let result = divide(10, 2);
    match result {
        Ok(value) => println!("结果: {}", value),
        Err(e) => println!("错误: {}", e),
    }

    let result = divide(10, 0);
    match result {
        Ok(value) => println!("结果: {}", value),
        Err(e) => println!("错误: {}", e),
    }
}

// 使用 ? 操作符传播错误
fn read_number_from_file(filename: &str) -> Result<i32, Box<dyn std::error::Error>> {
    let contents = fs::read_to_string(filename)?;
    let number: i32 = contents.trim().parse()?;
    Ok(number)
}

// 链式错误处理
fn process_file_data(filename: &str) -> Result<String, Box<dyn std::error::Error>> {
    let number = read_number_from_file(filename)?;
    let doubled = divide(number, 1)? * 2; // 这里确保不会除零
    Ok(format!("处理后的数字: {}", doubled))
}

// 自定义错误处理函数
fn safe_parse_int(s: &str) -> Result<i32, ParseIntError> {
    s.parse::<i32>()
}

fn main() {
    println!("=== Result 类型与错误处理演示 ===\n");

    println!("1. 使用 match 处理 Result:");
    handle_division_with_match();

    println!("\n2. 创建测试文件用于演示文件读取:");
    fs::write("test_number.txt", "42").expect("无法创建测试文件");

    println!("\n3. 使用 ? 操作符处理文件读取:");
    match read_number_from_file("test_number.txt") {
        Ok(num) => println!("从文件读取的数字: {}", num),
        Err(e) => println!("读取文件失败: {}", e),
    }

    println!("\n4. 链式错误处理:");
    match process_file_data("test_number.txt") {
        Ok(result) => println!("{}", result),
        Err(e) => println!("处理失败: {}", e),
    }

    println!("\n5. 安全的字符串解析:");
    let test_strings = vec!["123", "abc", "456"];
    for s in test_strings {
        match safe_parse_int(s) {
            Ok(num) => println!("'{}' 解析为: {}", s, num),
            Err(e) => println!("'{}' 解析失败: {}", s, e),
        }
    }

    // 清理测试文件
    fs::remove_file("test_number.txt").ok();
}