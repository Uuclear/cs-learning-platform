# 挑战 2：实现完整的可观测性上下文传播

## 背景
在现代微服务架构中，请求通常会跨越多个服务。为了有效调试和监控，需要在整个调用链中传播可观测性上下文。

## 任务要求
实现一个 `ObservabilityContext` 类，支持以下功能：

1. **上下文生成**：
   - 自动生成唯一的 Trace ID（32字符十六进制）
   - 自动生成 Span ID（16字符十六进制）
   - 支持采样标志（sampled）

2. **W3C Trace Context 兼容**：
   - 实现 `to_traceparent()` 方法，返回标准的 traceparent 头部值
   - 实现 `from_traceparent()` 类方法，从 traceparent 字符串重建上下文
   - 验证输入格式的有效性

3. **上下文传播**：
   - 实现 `create_child()` 方法，基于当前上下文创建子 span
   - 保持相同的 Trace ID，生成新的 Span ID

4. **HTTP 头部集成**：
   - 实现 `inject(headers)` 方法，将上下文注入 HTTP 头部字典
   - 实现 `extract(headers)` 方法，从 HTTP 头部字典提取上下文

5. **错误处理**：
   - 对无效输入抛出适当的异常
   - 提供清晰的错误信息

## 示例用法
```python
# 客户端生成上下文
ctx = ObservabilityContext.generate()
headers = {}
ctx.inject(headers)

# 服务端提取上下文
extracted_ctx = ObservabilityContext.extract(headers)
child_ctx = extracted_ctx.create_child()

# 验证上下文
print(f"Trace ID: {child_ctx.trace_id}")
print(f"Is sampled: {child_ctx.is_sampled()}")
```

## 验证标准
- 完全兼容 W3C Trace Context 标准
- 正确处理各种边界情况和无效输入
- 线程安全（如果涉及共享状态）
- 包含完整的中文注释和文档字符串
- 通过所有测试用例（包括正向和负向测试）

## 提示
- 参考课程中的 `solution-03.py` 实现
- W3C Trace Context 规范：https://www.w3.org/TR/trace-context/
- 使用正则表达式验证格式
- 注意十六进制字符的大小写处理
- 考虑版本兼容性（当前版本为 "00"）