# 挑战 2：解析器中的生命周期管理

## 背景
在编写解析器（parser）时，我们经常需要返回对输入数据的引用而不是复制数据。这可以提高性能，但需要正确处理生命周期。

## 任务
实现一个简单的 CSV 行解析器 `CsvRowParser`，它能够解析 CSV 格式的字符串行并返回对字段的引用。

## 要求
1. 实现 `CsvRowParser<'a>` 结构体，持有对输入 CSV 行的引用
2. 实现 `parse(&self) -> Vec<&'a str>` 方法，返回所有字段的引用向量
3. 处理基本的 CSV 规则：
   - 字段用逗号分隔
   - 支持空字段（连续逗号）
   - 不需要处理带引号的字段（简化版）

## 示例
对于输入 `"name,age,city"`，`parse()` 应该返回 `vec!["name", "age", "city"]`

对于输入 `"hello,,world"`，`parse()` 应该返回 `vec!["hello", "", "world"]`

## 生命周期考虑
- 返回的字段引用必须与输入的 CSV 行具有相同的生命周期
- 解析器本身应该只存储对输入数据的引用，不拥有数据
- 确保在所有可能的输入情况下都不会产生悬空引用

## 测试用例
你的实现应该能够处理以下情况：

```rust
fn main() {
    let csv_line = "Alice,30,New York";
    let parser = CsvRowParser::new(csv_line);
    let fields = parser.parse();
    
    assert_eq!(fields.len(), 3);
    assert_eq!(fields[0], "Alice");
    assert_eq!(fields[1], "30");
    assert_eq!(fields[2], "New York");
    
    // 测试空字段
    let empty_fields_line = "start,,end";
    let parser2 = CsvRowParser::new(empty_fields_line);
    let fields2 = parser2.parse();
    
    assert_eq!(fields2.len(), 3);
    assert_eq!(fields2[0], "start");
    assert_eq!(fields2[1], "");
    assert_eq!(fields2[2], "end");
}
```

## 额外挑战
- 扩展解析器以支持带引号的字段（如 `"John \"Doe\"",25,"San Francisco"`）
- 实现迭代器模式，允许逐个获取字段而不是一次性返回所有字段
- 添加错误处理，当 CSV 格式无效时返回适当的错误类型