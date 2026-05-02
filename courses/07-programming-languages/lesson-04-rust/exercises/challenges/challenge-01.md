# 编程挑战 1：实现安全的字符串缓冲区

## 背景
在系统编程中，经常需要处理动态大小的字符串缓冲区。传统的C语言方法容易导致缓冲区溢出等安全问题。

## 任务
实现一个 `SafeBuffer` 结构体，它能够安全地管理字符串缓冲区，支持以下操作：

1. 创建一个新的缓冲区（指定初始容量）
2. 向缓冲区追加字符串
3. 获取当前内容的不可变引用
4. 清空缓冲区
5. 获取缓冲区的当前长度和容量

## 要求
- 使用Rust的所有权和借用规则确保内存安全
- 不允许缓冲区溢出
- 所有方法都应该有适当的文档注释
- 实现 `Display` trait 以便可以直接打印缓冲区内容

## 提示
- 考虑使用 `Vec<u8>` 或 `String` 作为内部存储
- 注意区分长度（已使用空间）和容量（总分配空间）
- 使用生命周期确保返回的引用是安全的

## 测试用例
```rust
fn main() {
    let mut buffer = SafeBuffer::new(10);
    buffer.append("Hello");
    buffer.append(" World!");
    
    println!("缓冲区内容: {}", buffer);
    println!("长度: {}, 容量: {}", buffer.len(), buffer.capacity());
    
    buffer.clear();
    assert_eq!(buffer.len(), 0);
}
```