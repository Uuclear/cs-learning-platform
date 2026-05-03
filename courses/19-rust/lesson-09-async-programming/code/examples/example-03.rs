// example-03.rs - Tokio 任务管理与取消
use tokio;
use std::time::Duration;

#[tokio::main]
async fn main() {
    println!("=== Tokio 任务管理与取消示例 ===");

    // 示例1: 基本任务取消
    println!("\n--- 基本任务取消 ---");
    basic_cancellation().await;

    // 示例2: 超时控制
    println!("\n--- 超时控制 ---");
    timeout_example().await;

    // 示例3: 优雅关闭
    println!("\n--- 优雅关闭 ---");
    graceful_shutdown().await;
}

// 基本任务取消示例
async fn basic_cancellation() {
    let handle = tokio::spawn(async {
        for i in 0..10 {
            println!("任务运行中... {}", i);
            tokio::time::sleep(Duration::from_millis(500)).await;
        }
        println!("任务完成！");
    });

    // 等待2秒后取消任务
    tokio::time::sleep(Duration::from_secs(2)).await;
    handle.abort();
    println!("任务已取消");

    // 等待任务完全终止
    let _ = handle.await;
}

// 超时控制示例
async fn timeout_example() {
    // 创建一个可能长时间运行的任务
    let long_task = async {
        tokio::time::sleep(Duration::from_secs(5)).await;
        "任务完成"
    };

    // 使用超时包装任务
    match tokio::time::timeout(Duration::from_secs(2), long_task).await {
        Ok(result) => println!("任务成功: {}", result),
        Err(_) => println!("任务超时！"),
    }
}

// 优雅关闭示例
async fn graceful_shutdown() {
    // 创建一个可以响应关闭信号的任务
    let (shutdown_tx, mut shutdown_rx) = tokio::sync::oneshot::channel::<()>();

    let worker = tokio::spawn(async move {
        loop {
            tokio::select! {
                // 检查是否收到关闭信号
                _ = &mut shutdown_rx => {
                    println!("收到关闭信号，正在清理...");
                    break;
                }
                // 正常工作
                _ = tokio::time::sleep(Duration::from_millis(300)) => {
                    println!("工作进行中...");
                }
            }
        }
        println!("工作线程已安全退出");
    });

    // 让工作线程运行几秒钟
    tokio::time::sleep(Duration::from_secs(3)).await;

    // 发送关闭信号
    let _ = shutdown_tx.send(());

    // 等待工作线程完全退出
    let _ = worker.await;
}