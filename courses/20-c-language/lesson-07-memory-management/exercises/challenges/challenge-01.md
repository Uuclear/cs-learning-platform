# 挑战1：实现内存安全的字符串缓冲区

## 背景
在C语言中，字符串处理是内存错误的重灾区。缓冲区溢出、内存泄漏和悬空指针经常出现在字符串操作中。

## 任务
实现一个内存安全的字符串缓冲区（StringBuffer）结构，支持以下功能：

### 数据结构
```c
typedef struct {
    char* data;      // 字符串数据
    size_t length;   // 当前字符串长度（不包括null终止符）
    size_t capacity; // 当前缓冲区容量
} StringBuffer;
```

### 功能要求
1. **创建函数**：`StringBuffer* sb_create(size_t initial_capacity)`
   - 分配初始容量的缓冲区
   - 确保内存分配失败时正确处理

2. **销毁函数**：`void sb_destroy(StringBuffer* sb)`
   - 安全释放所有内存
   - 处理NULL指针输入

3. **追加函数**：`int sb_append(StringBuffer* sb, const char* str)`
   - 将字符串追加到缓冲区末尾
   - 自动扩容（使用2倍策略）
   - 返回1表示成功，0表示失败

4. **插入函数**：`int sb_insert(StringBuffer* sb, size_t pos, const char* str)`
   - 在指定位置插入字符串
   - 处理边界情况（pos超出范围）

5. **获取长度**：`size_t sb_length(const StringBuffer* sb)`
   - 返回当前字符串长度

6. **获取C字符串**：`const char* sb_cstr(const StringBuffer* sb)`
   - 返回以null终止的C字符串

### 内存安全要求
- 所有函数必须检查输入参数的有效性
- 每个malloc/calloc/realloc必须有对应的free
- realloc必须使用临时指针避免内存泄漏
- free后将指针设为NULL
- 处理所有可能的错误路径

### 测试用例
你的实现应该能通过以下测试：
```c
// 基本功能测试
StringBuffer* sb = sb_create(10);
sb_append(sb, "Hello");
sb_append(sb, " World!");
printf("%s\n", sb_cstr(sb)); // 应该输出 "Hello World!"

// 边界测试
sb_insert(sb, 0, "Start: ");
sb_insert(sb, sb_length(sb), " End");

// 错误处理测试
sb_append(NULL, "test"); // 应该安全处理
sb_insert(sb, 1000, "test"); // 应该安全处理

sb_destroy(sb);
```

### 提交要求
- 文件名：`string_buffer.c`
- 包含完整的头文件保护（如果需要头文件）
- 使用Valgrind验证没有内存泄漏
- 代码要有适当的注释说明关键逻辑

## 评分标准
- 功能完整性（40%）
- 内存安全性（30%）
- 错误处理（20%）
- 代码质量（10%）