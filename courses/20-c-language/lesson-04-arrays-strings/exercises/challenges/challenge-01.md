# 挑战 1：安全的字符串处理库

## 背景
在实际项目中，我们经常需要处理用户输入的字符串。不安全的字符串操作可能导致严重的安全漏洞。

## 任务
创建一个安全的字符串处理库，包含以下函数：

1. `safe_strcpy(dest, dest_size, src)` - 安全复制字符串
2. `safe_strcat(dest, dest_size, src)` - 安全连接字符串  
3. `safe_strncmp(str1, str2, n, max_len)` - 安全比较前n个字符（但不超过max_len）

## 要求
- 所有函数必须进行参数验证（检查NULL指针）
- 必须确保目标缓冲区不会溢出
- 必须保证结果字符串始终以`\0`结尾
- 函数应该返回适当的错误码或状态

## 测试用例
```c
// 测试安全复制
char buffer[10];
safe_strcpy(buffer, sizeof(buffer), "Hello World"); // 应该只复制"Hello Wor"并添加\0

// 测试边界情况
safe_strcpy(NULL, 10, "test"); // 应该安全处理NULL指针
safe_strcpy(buffer, 0, "test"); // 应该安全处理大小为0的情况
```

## 提示
- 使用`strncpy`作为基础，但要记住手动添加结束符
- 考虑使用`memcpy`来提高性能
- 返回值可以用来指示操作是否成功或截断了多少字符