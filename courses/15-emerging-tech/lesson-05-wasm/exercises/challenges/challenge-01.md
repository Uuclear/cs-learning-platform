# 挑战 1：实现 WebAssembly 栈机的扩展功能

## 背景
在 `example-01-wasm-concept.py` 中，我们实现了一个基本的 WebAssembly 栈机，支持加、减、乘、除操作。

## 任务
扩展这个栈机，添加以下功能：

1. **比较操作**：实现 `eq`（相等）、`lt`（小于）、`gt`（大于）操作
2. **逻辑操作**：实现 `and`、`or`、`not` 操作  
3. **控制流**：实现简单的条件跳转（使用标签和跳转指令）

## 要求

### 功能要求
- `eq`: 弹出两个值，如果相等则压入 1，否则压入 0
- `lt`: 弹出两个值 a, b，如果 a < b 则压入 1，否则压入 0
- `gt`: 弹出两个值 a, b，如果 a > b 则压入 1，否则压入 0
- `and`: 弹出两个值，执行逻辑与操作（非零为真）
- `or`: 弹出两个值，执行逻辑或操作
- `not`: 弹出一个值，执行逻辑非操作
- 实现简单的 `if_else` 控制结构

### 测试用例
你的实现应该能够正确执行以下程序：

```python
# 测试比较操作
machine.push(5)
machine.push(5)
machine.eq()  # 应该得到 1 (true)

machine.push(3)
machine.push(7)
machine.lt()  # 应该得到 1 (true)

# 测试逻辑操作
machine.push(1)
machine.push(0)
machine.and_()  # 应该得到 0 (false)

machine.push(1)
machine.push(0)  
machine.or_()   # 应该得到 1 (true)
```

## 提示
- 在 WebAssembly 中，布尔值用整数表示：0 表示 false，非零表示 true
- 控制流可以使用 Python 的条件语句来模拟，但要保持栈机的接口一致性
- 考虑错误处理，比如栈中元素不足时的情况

## 评估标准
- [ ] 所有新操作都能正确执行
- [ ] 保持原有的错误处理机制
- [ ] 代码风格一致，包含适当的中文注释
- [ ] 提供完整的测试用例验证功能