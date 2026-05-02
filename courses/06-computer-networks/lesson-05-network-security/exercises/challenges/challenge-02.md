# 编程挑战2: 文件完整性监控器 ⭐⭐

## 背景
文件完整性监控是系统安全的重要组成部分。通过定期检查关键文件的哈希值，可以及时发现恶意软件篡改或未经授权的修改。

## 任务
实现一个简单的文件完整性监控系统，包含以下功能：
1. 计算指定文件的SHA-256哈希值
2. 将哈希值保存到同名的 `.sha256` 文件中
3. 提供验证函数，比较当前文件哈希与保存的哈希值
4. 支持批量处理多个文件

## 要求
- 使用Python标准库 `hashlib`
- 函数设计：
  - `calculate_file_hash(filepath: str) -> str`
  - `save_hash_file(filepath: str, hash_value: str) -> None`
  - `verify_file_integrity(filepath: str) -> bool`
  - `monitor_files(file_list: list) -> dict`
- 处理大文件时使用分块读取（每次4096字节）
- 添加适当的错误处理和日志输出

## 示例用法
```python
# 监控配置文件
config_files = ["/etc/passwd", "/etc/hosts", "important_config.json"]
results = monitor_files(config_files)

for filepath, status in results.items():
    print(f"{filepath}: {'✅ 正常' if status else '❌ 已修改'}")
```

## 安全考虑
- 如何保护存储的哈希文件不被攻击者同时修改？
- 在实际生产环境中，还需要考虑哪些因素？
- 如何实现定期自动监控？

## 扩展挑战
- 添加邮件通知功能，当检测到文件被修改时发送警报
- 实现增量监控，只对发生变化的文件重新计算哈希
- 支持多种哈希算法（SHA-256, SHA-3, BLAKE2）