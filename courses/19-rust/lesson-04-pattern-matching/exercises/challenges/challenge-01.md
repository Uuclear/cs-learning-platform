# 挑战1：实现一个JSON解析器的简化版

## 目标
创建一个能够解析简单JSON值的枚举和相应的模式匹配函数。

## 要求
1. 定义一个`JsonValue`枚举，支持以下类型：
   - Null
   - Boolean(bool)
   - Number(f64)
   - String(String)
   - Array(Vec<JsonValue>)
   - Object(HashMap<String, JsonValue>)

2. 实现以下函数：
   ```rust
   fn get_type_name(value: &JsonValue) -> &'static str;
   fn is_primitive(value: &JsonValue) -> bool;
   fn stringify(value: &JsonValue) -> String;
   ```

3. 使用模式匹配实现所有函数，不要使用if-else语句。

## 提示
- 使用`std::collections::HashMap`存储对象
- 字符串化时注意正确处理引号和转义
- 数组和对象的字符串化需要递归处理

## 扩展挑战
- 添加类型转换函数，如`as_bool() -> Option<bool>`
- 实现路径查询功能，如`get_path(&self, path: &str) -> Option<&JsonValue>`