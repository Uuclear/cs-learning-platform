// example-02.rs - 通道（mpsc）消息传递
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== Rust 并发编程示例 2: 通道消息传递 ===\n");

    // 创建通道：sender 发送端，receiver 接收端
    let (sender, receiver) = mpsc::channel();

    // 启动生产者线程
    let sender_clone = sender.clone();
    let producer1 = thread::spawn(move || {
        for i in 0..3 {
            sender_clone.send(format!("消息 {}", i)).unwrap();
            println!("生产者1发送: 消息 {}", i);
            thread::sleep(Duration::from_millis(200));
        }
    });

    let sender_clone2 = sender.clone();
    let producer2 = thread::spawn(move || {
        for i in 3..6 {
            sender_clone2.send(format!("消息 {}", i)).unwrap();
            println!("生产者2发送: 消息 {}", i);
            thread::sleep(Duration::from_millis(300));
        }
    });

    // 主线程作为消费者接收消息
    drop(sender); // 显式释放主发送端，避免消费者永远等待

    println!("\n开始接收消息...");
    for received in receiver {
        println!("消费者收到: {}", received);
    }

    // 等待生产者线程完成
    producer1.join().unwrap();
    producer2.join().unwrap();

    println!("\n所有消息处理完毕！");
}