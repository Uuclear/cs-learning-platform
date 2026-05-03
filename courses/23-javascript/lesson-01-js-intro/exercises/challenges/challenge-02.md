# 挑战2：数据类型侦探

## 任务描述

创建一个JavaScript程序，能够检测和分析不同变量的数据类型，并提供详细的类型信息。

## 具体要求

1. 创建包含各种数据类型的变量：
   - 数字（整数、小数、负数）
   - 字符串（单引号、双引号、空字符串）
   - 布尔值（true、false）
   - 特殊值（null、undefined）
   - 对象（普通对象、数组）

2. 为每个变量创建一个分析函数，输出以下信息：
   - 变量的值
   - 使用 `typeof` 得到的类型
   - 是否为数组（使用 `Array.isArray()`）
   - 是否为对象（排除null的情况）
   - 转换为布尔值的结果

3. 格式化输出，使其易于阅读

4. 额外挑战：创建一个通用的类型检测函数，能够准确识别所有JavaScript数据类型

## 提示

- 记住 `typeof null` 返回 `"object"`，这是一个历史bug
- 数组在JavaScript中也是对象，但可以用 `Array.isArray()` 区分
- 空字符串、0、null、undefined、NaN 转换为布尔值都是 `false`
- 可以使用函数来封装重复的逻辑

## 示例输出

```
=== 数据类型分析 ===

变量: 42
- 值: 42
- typeof: number
- 是数组: false
- 是对象: false
- 布尔值: true

变量: "hello"
- 值: hello
- typeof: string
- 是数组: false
- 是对象: false
- 布尔值: true

变量: null
- 值: null
- typeof: object
- 是数组: false
- 是对象: false (特殊处理)
- 布尔值: false

变量: [1, 2, 3]
- 值: 1,2,3
- typeof: object
- 是数组: true
- 是对象: true
- 布尔值: true
===================
```