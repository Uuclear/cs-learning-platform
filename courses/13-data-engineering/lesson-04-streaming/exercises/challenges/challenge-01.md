# 挑战 01：实现自定义窗口函数

## 背景
在实际的流式处理应用中，标准的窗口类型（滚动、滑动、会话）可能无法满足所有需求。有时需要实现自定义的窗口逻辑。

## 任务
实现一个**计数窗口（Count Window）**，该窗口基于事件数量而不是时间来触发计算。

### 要求
1. 创建一个 `CountWindowProcessor` 类
2. 窗口大小由事件数量决定（例如：每10个事件触发一次计算）
3. 支持按键分组（例如：按用户ID分组）
4. 实现 `add_event(key, event)` 方法添加事件
5. 实现 `get_results()` 方法获取所有窗口结果

### 示例使用
```python
processor = CountWindowProcessor(window_size=3)
processor.add_event("user_A", {"value": 10})
processor.add_event("user_A", {"value": 20})
processor.add_event("user_A", {"value": 30})  # 触发窗口计算
processor.add_event("user_B", {"value": 5})
# ...
results = processor.get_results()
```

### 提示
- 使用字典来存储每个键的状态
- 跟踪每个键的事件计数
- 当计数达到窗口大小时，触发计算并重置计数

## 验证
编写测试代码验证你的实现：
1. 测试单个键的计数窗口
2. 测试多个键的并行计数窗口
3. 验证窗口触发后的状态重置