# 挑战 2：设计一个内存安全的配置管理器

## 背景
配置管理是大多数应用程序的核心部分。我们需要安全地存储、访问和修改配置数据，同时确保线程安全和内存安全。

## 任务
实现一个 `ConfigManager` 结构体，支持以下功能：

1. 存储键值对配置（键为 `String`，值为 `String`）
2. 根据键获取配置值（返回引用）
3. 设置或更新配置值
4. 检查配置是否存在
5. 获取所有配置键的列表

## 要求
- 使用 HashMap 来存储配置
- 正确处理所有权和借用，避免编译错误
- 确保方法签名合理，不会导致悬垂引用
- 考虑如何处理不存在的键的情况

## 提示
- 使用 `Option<&String>` 来处理可能不存在的键
- 考虑返回切片而不是所有权来提高效率
- 注意可变和不可变引用的使用时机

## 测试代码
```rust
fn main() {
    let mut config = ConfigManager::new();
    
    config.set("database_url", "postgres://localhost:5432");
    config.set("debug", "true");
    
    if let Some(url) = config.get("database_url") {
        println!("Database URL: {}", url);
    }
    
    let keys = config.keys();
    println!("Config keys: {:?}", keys);
    
    println!("Debug enabled: {}", config.exists("debug"));
    println!("Missing config: {}", config.exists("missing_key"));
}
```

## 扩展挑战
- 添加类型安全的配置获取方法（如 `get_bool`, `get_int`）
- 实现从文件加载配置的功能
- 添加配置变更的回调通知机制

## 思考题
1. 为什么在配置管理器中返回引用比返回所有权更合适？
2. 如何设计 API 来平衡易用性和内存安全性？
3. 在并发场景下，这个设计需要做哪些修改？
