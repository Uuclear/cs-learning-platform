# 编程挑战 1：复杂度分析

## 题目描述

给定以下三个函数，请分析每个函数的时间复杂度和空间复杂度，并解释你的分析过程。

## 待分析的函数

```python
def function_a(arr):
    """函数A"""
    n = len(arr)
    total = 0
    for i in range(n):
        for j in range(n):
            total += arr[i] * arr[j]
    return total

def function_b(arr):
    """函数B"""
    n = len(arr)
    result = []
    for i in range(n):
        sub_result = []
        for j in range(i, n):
            sub_result.append(arr[j])
        result.append(sub_result)
    return result

def function_c(n):
    """函数C"""
    if n <= 1:
        return 1
    return n * function_c(n - 1)
```

## 要求

1. **时间复杂度分析**：为每个函数确定准确的时间复杂度（使用大O表示法）
2. **空间复杂度分析**：为每个函数确定准确的空间复杂度（使用大O表示法）
3. **详细解释**：说明你是如何得出这些结论的，包括循环次数、递归深度等分析
4. **优化建议**：如果可能，提出优化建议并说明优化后的复杂度

## 提交格式

请将你的答案写在一个Python文件中，包含详细的注释说明。

## 难度：⭐⭐

## 预期学习目标

- 掌握嵌套循环的复杂度分析
- 理解递归函数的复杂度分析
- 学会区分时间和空间复杂度
- 培养算法优化思维