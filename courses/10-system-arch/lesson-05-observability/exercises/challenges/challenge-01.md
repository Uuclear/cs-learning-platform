# 挑战 1：实现自定义指标收集器

## 背景
在实际的微服务架构中，你可能需要收集特定业务领域的指标，比如订单处理时间、用户注册成功率等。

## 任务要求
使用 Python 标准库实现一个 `BusinessMetricsCollector` 类，满足以下要求：

1. **支持三种指标类型**：
   - `Counter`：用于计数（如订单总数）
   - `Gauge`：用于瞬时值（如当前在线用户数）
   - `Histogram`：用于分布统计（如订单处理时间）

2. **线程安全**：确保在多线程环境下指标数据的准确性

3. **Prometheus 兼容格式**：提供 `collect()` 方法返回符合 Prometheus 文本格式的字符串

4. **标签支持**：每个指标可以带有标签（labels），用于多维数据切分

## 示例用法
```python
collector = BusinessMetricsCollector()

# 订单相关指标
collector.counter("orders_total", {"status": "completed"}).inc()
collector.histogram("order_processing_seconds").observe(2.5)

# 用户相关指标  
collector.gauge("active_users").set(150)

# 输出 Prometheus 格式
print(collector.collect())
```

## 验证标准
- 代码能正确运行且无语法错误
- 支持标签功能，相同指标名不同标签被视为不同指标
- 线程安全（可使用 `threading.Lock`）
- 输出格式符合 Prometheus 规范
- 包含完整的中文注释说明

## 提示
- 参考课程中的 `solution-02.py` 实现
- Prometheus 文本格式规范：https://prometheus.io/docs/instrumenting/exposition_formats/
- 使用 `defaultdict` 和嵌套字典来管理带标签的指标