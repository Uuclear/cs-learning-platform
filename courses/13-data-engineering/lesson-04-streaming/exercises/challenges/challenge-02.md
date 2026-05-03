# 挑战 02：实现延迟数据处理策略

## 背景
在真实的流式处理系统中，数据延迟是常见问题。不同的应用场景可能需要不同的延迟数据处理策略。

## 任务
实现一个灵活的延迟数据处理框架，支持多种处理策略：

### 策略要求
1. **丢弃策略（Discard）**：直接丢弃延迟事件
2. **侧输出策略（Side Output）**：将延迟事件发送到单独的输出流
3. **更新策略（Update）**：允许延迟事件更新之前窗口的结果

### 实现要求
创建一个 `LateDataHandler` 类，包含以下方法：

```python
class LateDataHandler:
    def __init__(self, strategy: str, max_lateness_minutes: int):
        # 初始化处理器，指定策略和最大延迟时间
        
    def process_event(self, event_time: datetime, processing_time: datetime, data: Any) -> dict:
        # 处理事件，返回包含处理结果和策略信息的字典
```

### 返回结果格式
```python
{
    "action": "process" | "discard" | "side_output" | "update",
    "data": processed_data,
    "is_late": bool,
    "watermark": datetime,
    "strategy_used": str
}
```

## 扩展思考
1. 如何在实际的Flink或Spark Streaming应用中实现这些策略？
2. 更新策略如何保证Exactly-once语义？
3. 侧输出的数据如何被下游系统消费？

## 验证
编写测试用例验证三种策略：
1. 创建包含按时和延迟事件的测试数据
2. 分别使用三种策略处理相同的事件流
3. 验证每种策略的行为是否符合预期