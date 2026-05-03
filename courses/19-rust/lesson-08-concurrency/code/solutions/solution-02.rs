// solution-02.rs - 通道（mpsc）消息传递（完整解决方案）
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== 解决方案 2: 生产者-消费者模式 ===\n");

    // 创建有界通道，限制缓冲区大小为 10
    let (sender, receiver) = mpsc::sync_channel(10);

    // 启动多个生产者线程
    let mut producer_handles = vec![];

    for producer_id in 0..3 {
        let sender_clone = sender.clone();
        let handle = thread::spawn(move || {
            for msg_id in 0..5 {
                let message = format!("生产者{}-消息{}", producer_id, msg_id);
                match sender_clone.send(message) {
                    Ok(_) => println!("✅ 生产者 {} 发送消息 {}", producer_id, msg_id),
                    Err(_) => println!("❌ 生产者 {} 发送失败", producer_id),
                }
                thread::sleep(Duration::from_millis(100));
            }
            println!("🏭 生产者 {} 完成生产", producer_id);
        });
        producer_handles.push(handle);
    }

    // 释放主发送端，这样接收端知道何时停止
    drop(sender);

    // 消费者线程处理所有消息
    let consumer_handle = thread::spawn(move || {
        let mut count = 0;
        for message in receiver {
            println!("🛒 消费者收到: {}", message);
            count += 1;
            thread::sleep(Duration::from_millis(50)); // 模拟处理时间
        }
        println!("📦 消费者总共处理了 {} 条消息", count);
        count
    });

    // 等待所有生产者完成
    for handle in producer_handles {
        handle.join().unwrap();
    }

    // 获取消费者结果
    let total_processed = consumer_handle.join().unwrap();
    println!("\n🎯 所有消息处理完成！总共处理: {} 条消息", total_processed);
}