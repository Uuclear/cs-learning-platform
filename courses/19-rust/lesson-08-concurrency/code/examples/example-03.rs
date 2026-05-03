// example-03.rs - Arc + Mutex 共享计数器
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== Rust 并发编程示例 3: Arc + Mutex 共享状态 ===\n");

    // 创建共享的计数器：Arc 允许多个所有者，Mutex 提供互斥访问
    let counter = Arc::new(Mutex::new(0));

    // 创建多个线程来修改共享计数器
    let mut handles = vec![];

    for i in 0..5 {
        let counter_clone = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            println!("线程 {} 开始增加计数器", i);

            // 获取 Mutex 锁并修改值
            for _ in 0..100 {
                let mut num = counter_clone.lock().unwrap();
                *num += 1;
                // MutexGuard 在这里自动释放锁
            }

            println!("线程 {} 完成计数器增加", i);
        });

        handles.push(handle);
    }

    // 等待所有线程完成
    for handle in handles {
        handle.join().unwrap();
    }

    // 打印最终结果
    println!("\n最终计数器值: {}", *counter.lock().unwrap());
    println!("期望值: 500 (5个线程 × 每个100次)");
}