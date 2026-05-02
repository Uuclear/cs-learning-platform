# 编程挑战 2：实现并发安全的计数器

## 背景
在并发编程中，多个线程同时访问共享资源时容易出现数据竞争问题。Rust的所有权系统和类型系统可以帮助我们构建线程安全的代码。

## 任务
实现一个 `ThreadSafeCounter` 结构体，它能够在多线程环境中安全地进行计数操作。要求支持以下功能：

1. 创建一个新的计数器（初始值为0）
2. 增加计数器的值（支持指定增量）
3. 获取当前计数值
4. 重置计数器为0

## 要求
- 必须是线程安全的，可以在多个线程中同时使用
- 使用Rust的标准库同步原语（如 `Mutex`, `Arc` 等）
- 所有方法都应该处理可能的错误情况
- 提供完整的文档注释

## 高级要求（可选）
- 实现原子操作版本，比较性能差异
- 添加计数器的最大值限制，防止溢出

## 测试用例
```rust
use std::thread;
use std::sync::Arc;

fn main() {
    let counter = Arc::new(ThreadSafeCounter::new());
    let mut handles = vec![];
    
    // 创建10个线程，每个线程增加计数器100次
    for _ in 0..10 {
        let counter_clone = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            for _ in 0..100 {
                counter_clone.increment(1).unwrap();
            }
        });
        handles.push(handle);
    }
    
    // 等待所有线程完成
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("最终计数值: {}", counter.get().unwrap());
    assert_eq!(counter.get().unwrap(), 1000);
}
```

## 思考题
1. 为什么简单的 `i32` 字段不能直接在线程间共享？
2. `Mutex` 和 `RwLock` 在这个场景下有什么区别？
3. 如何在保证线程安全的同时最大化并发性能？