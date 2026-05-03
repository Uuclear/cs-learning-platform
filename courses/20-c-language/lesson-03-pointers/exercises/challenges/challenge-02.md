# 挑战2：实现字符串分割函数

## 目标
实现一个类似 `strtok` 的字符串分割函数，但更加安全和灵活。

## 要求
1. 函数不应修改原始字符串（与 `strtok` 不同）
2. 支持自定义分隔符字符集
3. 返回分割后的子字符串数组
4. 正确处理连续分隔符、开头和结尾的分隔符
5. 动态分配内存并提供清理函数

## 接口设计
```c
// 分割字符串，返回子字符串数组
char** split_string(const char *str, const char *delimiters, int *count);

// 释放分割结果的内存
void free_split_result(char **tokens, int count);
```

参数说明：
- `str`: 要分割的源字符串（不修改）
- `delimiters`: 包含所有分隔符字符的字符串（如 " ,;\t"）
- `count`: 输出参数，返回分割后的子字符串数量
- 返回值：指向子字符串指针数组的指针，如果失败返回NULL

## 示例行为
```c
const char *text = "apple,banana;cherry:grape";
const char *delims = ",;:";

int token_count;
char **tokens = split_string(text, delims, &token_count);

// tokens 应该包含: ["apple", "banana", "cherry", "grape"]
// token_count 应该是 4
```

## 边界情况处理
- 空字符串输入
- 只包含分隔符的字符串
- 连续分隔符（如 "a,,b"）
- 开头或结尾的分隔符（如 ",a,b,"）
- 内存分配失败的情况

## 测试要点
1. 基本功能测试（正常分割）
2. 边界情况测试（上述各种情况）
3. 内存泄漏检查
4. 错误输入处理（NULL指针等）

## 提示
- 使用 `strchr` 函数检查字符是否在分隔符集中
- 需要两次遍历：第一次计算需要多少个子字符串，第二次实际分配和复制
- 为每个子字符串使用 `malloc` + `memcpy` 或 `strndup`
- 记得为指针数组本身也分配内存
- 在清理函数中要释放每个子字符串和指针数组