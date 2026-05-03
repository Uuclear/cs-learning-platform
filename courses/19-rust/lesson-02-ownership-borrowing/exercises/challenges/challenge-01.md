# 挑战 1：实现一个安全的字符串缓冲区

## 背景
在很多应用中，我们需要构建和操作字符串。Rust的所有权系统可以帮助我们避免内存错误，但需要正确使用。

## 任务
实现一个 `StringBuffer` 结构体，它应该支持以下操作：

1. 创建一个新的空缓冲区
2. 向缓冲区追加字符串（不获取所有权，使用引用）
3. 获取缓冲区的当前内容（返回引用）
4. 清空缓冲区
5. 获取缓冲区长度

## 要求
- 使用合适的借用规则，确保所有方法都能通过编译
- 避免不必要的所有权转移
- 确保不会产生悬垂引用

## 提示
- 考虑哪些方法需要 `&self`，哪些需要 `&mut self`
- 注意返回引用时的生命周期问题
- 可以参考标准库中的 `String` 类型设计

## 测试代码
```rust
fn main() {
    let mut buffer = StringBuffer::new();
    
    buffer.append("Hello");
    buffer.append(" ");
    buffer.append("World");
    
    println!("Buffer content: {}", buffer.content());
    println!("Buffer length: {}", buffer.len());
    
    buffer.clear();
    println!("After clear - length: {}", buffer.len());
}
```

## 扩展挑战
- 添加一个方法来获取缓冲区的子字符串（类似切片）
- 实现 `Display` trait 来支持直接打印缓冲区
