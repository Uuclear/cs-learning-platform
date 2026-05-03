# 挑战 01: 实现 Jest 测试模拟器

## 任务描述

在这个挑战中，你需要实现一个简化的 Jest 测试框架，支持基本的测试组织和断言功能。

## 要求

1. **实现 `describe` 函数**：用于组织测试套件
   - 接收描述字符串和测试函数
   - 打印测试套件标题并执行测试函数

2. **实现 `it` 函数**：用于定义单个测试用例
   - 接收描述字符串和测试函数
   - 执行测试函数并捕获异常
   - 打印通过/失败状态

3. **实现 `expect` 函数和 `Expect` 类**：
   - `expect(actual)` 返回 `Expect` 对象
   - 支持 `to_be(expected)` 断言（严格相等）
   - 支持 `to_equal(expected)` 断言（深度相等）
   - 支持 `to_be_truthy()` 和 `to_be_falsy()` 断言

4. **实现 `mock_fn` 函数**：
   - 返回一个 mock 函数对象
   - 支持记录调用次数 (`mock_calls_length()`)
   - 支持设置返回值 (`mock_return_value(value)`)

## 示例使用

```python
def test_addition():
    def add(a, b):
        return a + b
    
    def test_positive_numbers():
        result = add(1, 2)
        expect(result).to_equal(3)
    
    it("应该正确计算正数相加", test_positive_numbers)

describe("数学函数测试", test_addition)
```

## 提示

- 使用 Python 的 `assert` 语句进行断言
- 在 `it` 函数中使用 try-catch 捕获断言失败
- Mock 函数可以是一个带有特殊方法的类实例
- 参考 `code/solutions/solution-01.py` 获取完整实现思路

## 验证

运行你的实现，确保以下测试能够正确执行并显示结果：

1. 基本算术运算测试
2. 字符串操作测试  
3. Mock 函数调用跟踪测试

完成后，你的测试框架应该能够清晰地显示哪些测试通过，哪些失败，并提供有用的错误信息。