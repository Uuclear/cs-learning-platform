// solution-03.rs - Option 和 Result 练习解决方案

// 定义一个安全的数组访问函数
fn safe_get_element<T>(vec: &[T], index: usize) -> Option<&T> {
    if index < vec.len() {
        Some(&vec[index])
    } else {
        None
    }
}

// 定义一个安全的字符串转换函数
fn safe_string_to_number(text: &str) -> Result<i32, String> {
    text.trim()
        .parse::<i32>()
        .map_err(|_| format!("无法将 '{}' 转换为整数", text))
}

// 定义一个复合操作函数，使用 ? 操作符
fn process_user_input(input: &str) -> Result<String, String> {
    let number = safe_string_to_number(input)?;
    let doubled = number * 2;

    // 模拟一些可能失败的操作
    if doubled > 100 {
        return Err(String::from("结果太大"));
    }

    Ok(format!("输入 {} 的两倍是 {}", number, doubled))
}

// 使用 Option 的链式操作
fn find_and_process_data(data: Vec<Option<i32>>) -> Option<i32> {
    data.into_iter()
        .filter_map(|x| x) // 过滤掉 None，提取 Some 中的值
        .map(|x| x * 2)    // 对每个值乘以 2
        .find(|&x| x > 10) // 找到第一个大于 10 的值
}

fn main() {
    // 测试安全数组访问
    let numbers = vec![1, 2, 3, 4, 5];

    if let Some(value) = safe_get_element(&numbers, 2) {
        println!("索引 2 的值: {}", value);
    }

    match safe_get_element(&numbers, 10) {
        Some(value) => println!("索引 10 的值: {}", value),
        None => println!("索引 10 超出范围"),
    }

    println!("\n=== 字符串转数字 ===");

    // 测试字符串转换
    let test_inputs = vec!["42", "  123  ", "abc", ""];

    for input in test_inputs {
        match safe_string_to_number(input) {
            Ok(num) => println!("'{}' -> {}", input, num),
            Err(e) => println!("'{}' -> 错误: {}", input, e),
        }
    }

    println!("\n=== 复合操作 ===");

    // 测试复合操作
    let user_inputs = vec!["25", "60", "abc", "50"];

    for input in user_inputs {
        match process_user_input(input) {
            Ok(result) => println!("处理 '{}': {}", input, result),
            Err(e) => println!("处理 '{}' 失败: {}", input, e),
        }
    }

    println!("\n=== Option 链式操作 ===");

    // 测试 Option 链式操作
    let mixed_data = vec![Some(3), None, Some(7), Some(2), None, Some(8)];

    match find_and_process_data(mixed_data) {
        Some(result) => println!("找到的结果: {}", result),
        None => println!("没有找到符合条件的值"),
    }
}