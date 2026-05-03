// example-02.rs - 并发网络请求（多个 URL 同时获取）
use tokio;
use std::time::Instant;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("=== 并发网络请求示例 ===");

    // 模拟的 URL 列表（使用 httpbin.org 的延迟端点）
    let urls = vec![
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
    ];

    // 顺序执行（用于对比）
    println!("\n--- 顺序执行 ---");
    let start = Instant::now();
    sequential_fetch(&urls).await?;
    println!("顺序执行耗时: {:?}", start.elapsed());

    // 并发执行
    println!("\n--- 并发执行 ---");
    let start = Instant::now();
    concurrent_fetch(&urls).await?;
    println!("并发执行耗时: {:?}", start.elapsed());

    Ok(())
}

// 顺序执行所有请求
async fn sequential_fetch(urls: &[&str]) -> Result<(), reqwest::Error> {
    for url in urls {
        let response = reqwest::get(url).await?;
        let status = response.status();
        println!("URL: {} - 状态: {}", url, status);
    }
    Ok(())
}

// 并发执行所有请求
async fn concurrent_fetch(urls: &[&str]) -> Result<(), reqwest::Error> {
    // 为每个 URL 创建一个任务
    let tasks: Vec<_> = urls
        .iter()
        .map(|&url| {
            tokio::spawn(async move {
                let response = reqwest::get(url).await?;
                let status = response.status();
                Ok::<_, reqwest::Error>((url, status))
            })
        })
        .collect();

    // 等待所有任务完成
    for task in tasks {
        match task.await {
            Ok(Ok((url, status))) => println!("URL: {} - 状态: {}", url, status),
            Ok(Err(e)) => eprintln!("请求失败: {}", e),
            Err(e) => eprintln!("任务错误: {}", e),
        }
    }

    Ok(())
}