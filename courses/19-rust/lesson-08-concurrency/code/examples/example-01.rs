// example-01.rs - 多线程创建与 join 处理
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== Rust 并发编程示例 1: 线程创建与管理 ===\n");

    // 创建多个线程
    let handles: Vec<_> = (0..5).map(|i| {
        thread::spawn(move || {
            println!("线程 {} 开始执行", i);
            thread::sleep(Duration::from_millis(100 * i));
            println!("线程 {} 执行完成", i);
            i * 2 // 返回值
        })
    }).collect();

    // 等待所有线程完成并获取返回值
    for (i, handle) in handles.into_iter().enumerate() {
        match handle.join() {
            Ok(result) => println!("主线程收到线程 {} 的结果: {}", i, result),
            Err(e) => println!("线程 {} 执行出错: {:?}", i, e),
        }
    }

    println!("\n所有线程执行完毕！");
}