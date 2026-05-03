# 挑战 1：实现健壮的文件处理器

## 背景
你正在开发一个配置文件处理器，需要从多个文件中读取数据并进行处理。这个处理器将用于生产环境，因此必须能够优雅地处理各种错误情况。

## 要求
1. 创建一个 `FileProcessor` 结构体，包含以下方法：
   - `new()` - 创建新的处理器实例
   - `read_config_file(&self, filename: &str) -> Result<String, CustomError>` - 读取配置文件
   - `parse_numbers(&self, content: &str) -> Result<Vec<i32>, CustomError>` - 解析数字列表
   - `process_data(&self, filename: &str) -> Result<Vec<i32>, CustomError>` - 完整的处理流程

2. 实现一个自定义错误类型 `CustomError`，它应该能够处理：
   - 文件不存在或无法读取（IO 错误）
   - 数字解析失败（ParseIntError）
   - 空文件或无效格式（自定义验证错误）

3. 使用 `?` 操作符来传播错误，不要在中间函数中使用 `unwrap()` 或 `expect()`

4. 在 `main` 函数中演示：
   - 成功处理有效文件
   - 优雅处理不存在的文件
   - 优雅处理包含无效数据的文件

## 示例输入文件
创建两个测试文件：

**valid_data.txt**:
```
10
20
30
40
50
```

**invalid_data.txt**:
```
10
abc
30
```

## 提示
- 使用 `enum` 来定义你的自定义错误类型
- 实现 `From` trait 来自动转换标准库错误
- 实现 `Display` 和 `Error` trait
- 记住：生产代码应该避免 panic！

## 验收标准
- 所有错误都被正确捕获和处理
- 不会出现程序崩溃（panic）
- 错误信息清晰有用
- 代码结构清晰，职责分离