fn main() {
    // if let 简化 Option 处理
    let some_option: Option<i32> = Some(5);

    // 传统方式
    match some_option {
        Some(value) => println!("值是: {}", value),
        None => (),
    }

    // 使用 if let 简化
    if let Some(value) = some_option {
        println!("值是: {}", value);
    }

    // while let 处理循环
    let mut stack = vec![1, 2, 3, 4, 5];

    // 传统方式
    while !stack.is_empty() {
        let value = stack.pop().unwrap();
        println!("弹出: {}", value);
    }

    // 使用 while let 更安全
    let mut stack2 = vec![10, 20, 30];
    while let Some(value) = stack2.pop() {
        println!("安全弹出: {}", value);
    }

    // 处理 Result 类型
    let result: Result<i32, &str> = Ok(42);
    if let Ok(value) = result {
        println!("成功获取结果: {}", value);
    }
}