// example-01.rs - async/await 基础（异步函数调用）
use tokio;

#[tokio::main]
async fn main() {
    println!("=== 异步编程基础示例 ===");

    // 调用异步函数并等待结果
    let result = simple_async_function().await;
    println!("简单异步函数结果: {}", result);

    // 链式调用多个异步函数
    let final_result = chain_async_functions().await;
    println!("链式调用结果: {}", final_result);
}

// 简单的异步函数
async fn simple_async_function() -> i32 {
    // 模拟异步操作（如网络请求、文件读取等）
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
    42
}

// 链式调用异步函数
async fn chain_async_functions() -> String {
    let num1 = simple_async_function().await;
    let num2 = another_async_function().await;

    format!("结果: {} + {} = {}", num1, num2, num1 + num2)
}

async fn another_async_function() -> i32 {
    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
    18
}