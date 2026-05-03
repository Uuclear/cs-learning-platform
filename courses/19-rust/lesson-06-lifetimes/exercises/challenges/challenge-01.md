# 挑战 1：实现带生命周期的缓存结构

## 背景
在实际应用中，我们经常需要实现一个简单的缓存结构来存储对数据的引用。但是当涉及到生命周期时，这可能会变得复杂。

## 任务
实现一个 `RefCache` 结构体，它能够存储对字符串切片的引用，并提供以下功能：

1. 构造函数 `new()` 创建空缓存
2. `insert(&mut self, key: &str, value: &'a str)` 方法存储键值对
3. `get(&self, key: &str) -> Option<&'a str>` 方法获取值
4. `clear(&mut self)` 方法清空缓存

## 要求
- `RefCache` 必须正确处理生命周期，确保存储的引用在其源数据有效期间内使用
- 缓存应该使用 `HashMap<String, &'a str>` 作为内部存储
- 所有方法都应该有正确的生命周期标注

## 提示
- 考虑 `RefCache` 结构体本身需要什么样的生命周期参数
- `insert` 方法的 `value` 参数和返回的引用应该具有相同的生命周期
- 你可能需要为 `RefCache` 实现泛型生命周期参数

## 测试用例
你的实现应该能够通过以下测试：

```rust
fn main() {
    let data1 = String::from("cached value 1");
    let data2 = String::from("cached value 2");
    
    let mut cache = RefCache::new();
    cache.insert("key1", &data1);
    cache.insert("key2", &data2);
    
    assert_eq!(cache.get("key1"), Some(&data1.as_str()));
    assert_eq!(cache.get("key2"), Some(&data2.as_str()));
    assert_eq!(cache.get("nonexistent"), None);
    
    cache.clear();
    assert_eq!(cache.get("key1"), None);
}
```

## 额外挑战
如果可能的话，尝试让 `RefCache` 支持任意类型的引用，而不仅仅是字符串切片。