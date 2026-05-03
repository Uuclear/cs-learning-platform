# 挑战2：内存泄漏检测器

## 背景
虽然Valgrind等工具很强大，但有时我们需要在程序内部实现简单的内存跟踪功能，特别是在嵌入式系统或无法使用外部工具的环境中。

## 任务
实现一个简单的内存分配跟踪器，能够记录所有malloc/calloc/realloc/free调用，并在程序结束时报告未释放的内存块。

### 功能要求

#### 1. 内存跟踪结构
实现以下数据结构来跟踪内存分配：
```c
typedef struct {
    void* ptr;           // 分配的指针地址
    size_t size;         // 分配的大小
    const char* file;    // 分配发生的文件名
    int line;            // 分配发生的行号
    const char* func;    // 分配发生的函数名
} MemoryRecord;
```

#### 2. 宏定义替换
使用宏定义替换标准的内存管理函数：
```c
#define malloc(size) tracked_malloc(size, __FILE__, __LINE__, __func__)
#define calloc(num, size) tracked_calloc(num, size, __FILE__, __LINE__, __func__)
#define realloc(ptr, size) tracked_realloc(ptr, size, __FILE__, __LINE__, __func__)
#define free(ptr) tracked_free(ptr, __FILE__, __LINE__, __func__)
```

#### 3. 核心函数实现
实现以下跟踪函数：
- `void* tracked_malloc(size_t size, const char* file, int line, const char* func)`
- `void* tracked_calloc(size_t num, size_t size, const char* file, int line, const char* func)`
- `void* tracked_realloc(void* ptr, size_t size, const char* file, int line, const char* func)`
- `void tracked_free(void* ptr, const char* file, int line, const char* func)`

#### 4. 报告函数
实现报告函数：
- `void print_memory_report(void)` - 打印当前所有未释放的内存块
- `int check_for_leaks(void)` - 返回未释放内存块的数量

#### 5. 自动报告
使用`atexit()`注册一个函数，在程序正常退出时自动调用`print_memory_report()`。

### 技术要求
- 使用链表或其他数据结构存储MemoryRecord
- 线程安全不是必需的（单线程环境）
- 处理realloc的特殊情况（NULL指针、size为0）
- 正确处理free(NULL)的情况
- 内存跟踪器本身的内存分配不能被自己跟踪（避免无限递归）

### 测试用例
你的实现应该能正确跟踪以下代码：
```c
#include "memory_tracker.h" // 你的头文件

int main() {
    int* ptr1 = malloc(sizeof(int));
    *ptr1 = 42;
    
    int* ptr2 = calloc(10, sizeof(int));
    
    char* str = malloc(20);
    strcpy(str, "Hello");
    
    // 故意不释放ptr1和str，只释放ptr2
    free(ptr2);
    
    return 0; // 程序退出时应该报告2个内存泄漏
}
```

### 输出格式
报告应该包含以下信息：
```
Memory Leak Report:
==================
1. 4 bytes leaked at example.c:10 in main()
2. 20 bytes leaked at example.c:14 in main()

Total: 24 bytes in 2 blocks leaked.
```

### 提交要求
- 文件名：`memory_tracker.c` 和 `memory_tracker.h`
- 头文件包含必要的宏定义和函数声明
- 实现文件包含完整的跟踪逻辑
- 包含测试程序`test_memory_tracker.c`
- 使用标准C库，不依赖外部库

## 评分标准
- 功能正确性（40%）
- 内存跟踪准确性（25%）
- 错误处理完整性（20%）
- 代码设计质量（15%）

## 提示
- 注意避免跟踪器自身分配内存时产生递归
- 可以使用静态变量来存储跟踪数据
- 考虑使用全局标志来控制是否启用跟踪
- realloc处理需要特别小心，要正确更新跟踪记录