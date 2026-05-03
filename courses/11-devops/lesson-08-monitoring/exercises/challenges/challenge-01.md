# 挑战1：实现自定义指标导出器

## 背景
在实际的可观测性系统中，你可能需要将指标导出到不同的后端系统，比如Prometheus、Graphite、StatsD等。当前的`MetricCollector`只支持Prometheus格式。

## 任务
扩展`MetricCollector`类，添加一个通用的导出接口，支持多种导出格式：

1. **实现`export_format`方法**：接受一个格式参数（如'prometheus'、'json'、'influxdb'）
2. **添加JSON导出格式**：将所有指标数据导出为结构化的JSON格式
3. **添加InfluxDB行协议格式**：实现InfluxDB的行协议格式导出

## 要求
- 保持向后兼容性，原有的`export_prometheus()`方法继续工作
- JSON格式应该包含完整的指标元数据（名称、类型、描述、值、标签等）
- InfluxDB格式应该遵循官方行协议规范
- 所有代码必须包含中文注释

## 提示
- InfluxDB行协议格式：`measurement,tag_key=tag_value field_key=field_value timestamp`
- 可以为每种格式创建单独的导出方法，然后在`export_format`中调用

## 验证
运行你的代码，确保能够正确导出三种不同格式的指标数据，并且输出格式符合各自的标准。