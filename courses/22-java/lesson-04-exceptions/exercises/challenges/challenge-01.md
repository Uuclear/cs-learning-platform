# 挑战 1：文件读取器异常处理

## 任务描述
创建一个文件读取器类 `SafeFileReader`，它能够安全地读取文本文件并处理各种可能的异常情况。

## 要求
1. 创建一个名为 `SafeFileReader` 的类
2. 实现 `readFile(String filename)` 方法，该方法：
   - 如果文件不存在，抛出自定义的 `FileNotFoundException`（继承自 `IOException`）
   - 如果文件存在但无法读取（权限问题等），抛出 `IOException`
   - 如果文件内容包含非UTF-8编码的字符，能够优雅处理而不崩溃
   - 正常情况下返回文件的完整内容作为字符串
3. 使用 try-with-resources 确保文件资源被正确关闭
4. 在 `main` 方法中测试各种情况：
   - 读取存在的文件
   - 读取不存在的文件
   - 读取空文件

## 提示
- 需要创建自定义异常类 `FileNotFoundException`
- 使用 `java.nio.file.Files` 和 `java.nio.charset.StandardCharsets.UTF_8`
- 考虑使用 `StringBuilder` 来构建返回的字符串

## 评估标准
- 正确处理所有异常情况
- 使用适当的异常类型（受检 vs 非受检）
- 资源管理正确（无内存泄漏）
- 代码结构清晰，有适当的注释
