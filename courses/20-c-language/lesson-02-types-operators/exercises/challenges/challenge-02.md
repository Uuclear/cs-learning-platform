# 挑战2：浮点数精度计算器

## 背景
浮点数的精度限制在科学计算、金融应用和游戏开发中都是一个重要问题。理解何时使用`float` vs `double`，以及如何正确处理浮点比较，是每个C程序员的必备技能。

## 任务
创建一个程序来分析和演示浮点数的精度特性：

1. **精度测试函数**：编写一个函数来确定`float`和`double`类型能够精确表示的最大连续整数
2. **epsilon计算器**：编写一个函数来计算给定数值范围内的合适epsilon值
3. **安全比较函数**：实现一个通用的浮点数比较函数，支持相对误差和绝对误差

## 具体要求

### 1. 精度测试
```c
// 找到float能精确表示的最大连续整数
int find_float_precision_limit();
// 找到double能精确表示的最大连续整数  
long long find_double_precision_limit();
```

### 2. Epsilon计算
```c
float calculate_float_epsilon(float value);
double calculate_double_epsilon(double value);
```

### 3. 安全比较
```c
int float_equal(float a, float b, float epsilon);
int double_equal(double a, double b, double epsilon);
// 或者实现自动选择epsilon的版本
int float_equal_auto(float a, float b);
int double_equal_auto(double a, double b);
```

## 测试用例
你的程序应该能够正确处理以下情况：
- 非常小的数值（接近零）
- 非常大的数值
- 特殊值（如NaN, infinity）
- 正常的计算结果比较

## 扩展挑战
- 实现一个"几乎相等"的比较，考虑相对误差：`|a - b| <= epsilon * max(|a|, |b|)`
- 创建一个交互式程序，让用户输入两个浮点数并显示它们的二进制表示和实际差异
- 研究并实现ULP（Units in the Last Place）比较方法