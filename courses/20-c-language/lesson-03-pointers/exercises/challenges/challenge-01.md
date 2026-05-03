# 挑战1：实现动态数组

## 目标
使用指针和动态内存分配实现一个简单的动态整数数组，支持以下操作：

- 创建动态数组（指定初始容量）
- 向数组末尾添加元素（如果容量不足则自动扩容）
- 获取指定索引的元素
- 获取数组当前大小和容量
- 释放数组内存

## 要求
1. 使用 `malloc`、`realloc` 和 `free` 进行动态内存管理
2. 实现合理的扩容策略（例如容量翻倍）
3. 包含适当的错误检查（空指针、越界访问等）
4. 提供清晰的API接口

## 接口设计建议
```c
typedef struct {
    int *data;      // 指向实际数据的指针
    int size;       // 当前元素个数
    int capacity;   // 当前容量
} DynamicArray;

// 创建动态数组
DynamicArray* create_array(int initial_capacity);

// 添加元素
int append(DynamicArray *arr, int value);

// 获取元素（返回是否成功）
int get(DynamicArray *arr, int index, int *value);

// 获取大小和容量
int get_size(DynamicArray *arr);
int get_capacity(DynamicArray *arr);

// 释放内存
void destroy_array(DynamicArray *arr);
```

## 测试用例
- 创建容量为5的数组，添加10个元素（需要自动扩容）
- 验证扩容后的容量是否合理
- 测试越界访问的错误处理
- 验证内存正确释放，无内存泄漏

## 提示
- 在 `append` 函数中检查是否需要扩容
- 使用 `realloc` 时要小心处理返回值（可能为NULL）
- 始终检查指针参数是否为NULL
- 考虑使用工具如 `valgrind` 检查内存泄漏