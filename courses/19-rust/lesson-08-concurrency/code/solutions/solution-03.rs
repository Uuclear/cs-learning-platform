// solution-03.rs - Arc + Mutex 共享计数器（完整解决方案）
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== 解决方案 3: 线程安全的共享状态 ===\n");

    // 创建线程安全的共享数据结构
    let shared_data = Arc::new(Mutex::new(vec![1, 2, 3, 4, 5]));

    // 启动多个工作线程修改共享数据
    let mut handles = vec![];

    for worker_id in 0..4 {
        let data_clone = Arc::clone(&shared_data);
        let handle = thread::spawn(move || {
            println!("👷 工人 {} 开始工作", worker_id);

            // 每个工人执行多次操作
            for operation in 0..3 {
                // 获取锁并修改数据
                let mut data = data_clone.lock().unwrap();
                data.push(worker_id * 10 + operation);
                println!("   👷 工人 {} 执行操作 {}: 数据长度 {}", worker_id, operation, data.len());
                drop(data); // 显式释放锁（虽然不是必需的，但更清晰）
                thread::sleep(Duration::from_millis(50));
            }

            println!("✅ 工人 {} 完成所有操作", worker_id);
        });

        handles.push(handle);
    }

    // 等待所有工人完成
    for handle in handles {
        handle.join().unwrap();
    }

    // 显示最终结果
    let final_data = shared_data.lock().unwrap();
    println!("\n📊 最终共享数据: {:?}", final_data);
    println!("📊 数据总长度: {}", final_data.len());
    println!("📊 预期长度: 5 (初始) + 4 (工人) × 3 (操作) = 17");
}