// example-03.rs - panic! 与 unwrap 的正确使用场景

use std::collections::HashMap;
use std::env;

// 正确使用 unwrap 的场景：不可能失败的操作
fn get_program_name() -> String {
    // env::args().next() 永远不会返回 None，因为程序总是有至少一个参数（程序名）
    env::args().next().unwrap()
}

// 使用 expect 提供更好的错误信息
fn parse_required_env_var(var_name: &str) -> String {
    env::var(var_name).expect(&format!("环境变量 {} 必须设置", var_name))
}

// 在测试中使用 panic 是合适的
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_division_by_zero_should_panic() {
        let result = std::panic::catch_unwind(|| {
            let _ = 10 / 0; // 这会 panic!
        });
        assert!(result.is_err());
    }

    #[test]
    fn test_unwrap_on_some() {
        let x = Some(42);
        assert_eq!(x.unwrap(), 42); // 在测试中 unwrap Some 是安全的
    }
}

// 在原型开发或快速脚本中使用 unwrap
fn quick_script_example() {
    println!("=== 快速脚本示例 ===");

    // 创建一些测试数据
    let mut data = HashMap::new();
    data.insert("name", "Alice");
    data.insert("age", "30");

    // 在我们知道键一定存在的情况下，unwrap 是可以接受的
    let name = data.get("name").unwrap();
    let age = data.get("age").unwrap().parse::<u32>().unwrap();

    println!("姓名: {}, 年龄: {}", name, age);
}

// 使用 panic! 进行不可恢复的错误处理
fn validate_critical_config(config: &str) -> bool {
    if config.is_empty() {
        panic!("关键配置不能为空！程序无法继续运行。");
    }
    true
}

// 对比：生产代码中的安全处理 vs 快速原型中的 unwrap
fn production_vs_prototype() {
    println!("\n=== 生产代码 vs 原型代码 ===");

    let test_data = vec!["10", "20", "invalid", "30"];

    println!("生产代码风格（安全处理）:");
    for (i, item) in test_data.iter().enumerate() {
        match item.parse::<i32>() {
            Ok(num) => println!("项目 {}: 成功解析为 {}", i, num),
            Err(e) => println!("项目 {}: 解析失败 - {}", i, e),
        }
    }

    println!("\n原型代码风格（使用 unwrap）:");
    // 注意：这里只在我们知道数据有效时才使用 unwrap
    let safe_data = vec!["10", "20", "30"];
    for item in safe_data {
        let num = item.parse::<i32>().unwrap(); // 我们知道这些数据是有效的
        println!("解析结果: {}", num);
    }
}

fn main() {
    println!("=== panic! 与 unwrap 的正确使用场景 ===\n");

    println!("1. 程序名称: {}", get_program_name());

    // 设置一个测试环境变量
    env::set_var("TEST_ENV_VAR", "test_value");
    println!("2. 环境变量值: {}", parse_required_env_var("TEST_ENV_VAR"));

    println!("\n3. 验证关键配置:");
    validate_critical_config("valid_config"); // 这不会 panic
    // validate_critical_config(""); // 这会 panic!

    quick_script_example();
    production_vs_prototype();

    // 清理环境变量
    env::remove_var("TEST_ENV_VAR");
}