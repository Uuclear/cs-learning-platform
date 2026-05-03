// solution-01.rs - 多线程创建与 join 处理（完整解决方案）
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== 解决方案 1: 线程创建与管理 ===\n");

    // 使用 Vec 存储线程句柄以便后续 join
    let mut handles = Vec::new();

    // 创建 5 个线程，每个线程执行不同的任务
    for i in 0..5 {
        let handle = thread::spawn(move || {
            // 模拟一些工作
            println!("线程 {} 开始工作", i);
            thread::sleep(Duration::from_millis(50 * (i + 1)));

            // 返回计算结果
            let result = i * i + 2 * i + 1;
            println!("线程 {} 完成工作，结果: {}", i, result);
            result
        });

        handles.push(handle);
    }

    // 收集所有线程的结果
    let mut results = Vec::new();
    for (i, handle) in handles.into_iter().enumerate() {
        match handle.join() {
            Ok(result) => {
                results.push(result);
                println!("主线程成功获取线程 {} 的结果: {}", i, result);
            }
            Err(_) => {
                println!("线程 {} 执行失败", i);
            }
        }
    }

    println!("\n所有线程执行完毕！");
    println!("最终结果数组: {:?}", results);
}