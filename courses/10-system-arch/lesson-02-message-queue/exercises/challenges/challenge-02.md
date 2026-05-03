# 挑战 02：实现可靠的消费者组

## 难度
⭐⭐⭐⭐

## 背景
在分布式系统中，消费者组需要处理动态的成员变化（消费者加入/离开）并重新平衡分区分配。同时，系统必须保证消息处理的可靠性。

## 要求
实现一个 `ReliableConsumerGroup` 类，支持以下高级功能：

1. **动态重平衡**：当消费者加入或离开时，自动重新分配分区
2. **恰好一次语义**：结合幂等处理器确保消息不重复处理
3. **故障恢复**：消费者崩溃后能够从上次处理的位置继续
4. **监控指标**：提供处理统计信息（总消息数、已处理、失败率等）

## 接口定义
```python
class ReliableConsumerGroup:
    def add_consumer(self, consumer_id: str) -> None:
        """添加消费者到组"""
        pass
    
    def remove_consumer(self, consumer_id: str) -> None:
        """从组中移除消费者"""
        pass
    
    def add_partition(self, topic: str, partition_id: int) -> None:
        """添加分区"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        pass
    
    def start_processing(self) -> None:
        """开始处理消息"""
        pass
```

## 复杂场景
- 模拟网络分区导致的消费者临时断开
- 处理消费者处理消息时的异常情况
- 实现检查点机制（checkpointing）来记录处理进度
- 支持优雅关闭，确保所有消息都被正确处理

## 技术要求
- 使用文件或内存存储来模拟持久化状态
- 实现基于偏移量（offset）的消息跟踪
- 包含完整的错误处理和恢复逻辑
- 提供详细的日志记录

## 评估标准
- 动态重平衡正确性（30%）
- 恰好一次语义保证（25%）
- 故障恢复能力（25%）
- 代码架构与可维护性（20%）

## 扩展思考
- 如何优化重平衡过程以减少对正常处理的影响？
- 在大规模部署中，如何避免"惊群效应"（thundering herd）？
- 如何实现跨数据中心的消费者组协调？