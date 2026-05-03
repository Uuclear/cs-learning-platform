#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 02: Kafka消费者组行为模拟
演示Kafka消费者组的分区分配和负载均衡行为
"""

import threading
import time
import random
from typing import List, Dict, Set


class KafkaPartition:
    """Kafka分区类"""

    def __init__(self, topic: str, partition_id: int):
        self.topic = topic
        self.partition_id = partition_id
        self.messages: List[str] = []
        self.offset = 0

    def add_message(self, message: str) -> None:
        """向分区添加消息"""
        self.messages.append(message)

    def get_next_message(self) -> str:
        """获取下一条消息（按偏移量）"""
        if self.offset < len(self.messages):
            message = self.messages[self.offset]
            self.offset += 1
            return message
        return None


class KafkaConsumer:
    """Kafka消费者类"""

    def __init__(self, consumer_id: str, group_id: str):
        self.consumer_id = consumer_id
        self.group_id = group_id
        self.assigned_partitions: List[KafkaPartition] = []
        self.running = False

    def assign_partitions(self, partitions: List[KafkaPartition]) -> None:
        """分配分区给消费者"""
        self.assigned_partitions = partitions
        print(f"消费者 {self.consumer_id} 被分配分区: {[f'{p.topic}-{p.partition_id}' for p in partitions]}")

    def start_consuming(self) -> None:
        """开始消费消息"""
        self.running = True
        thread = threading.Thread(target=self._consume_loop, daemon=True)
        thread.start()

    def _consume_loop(self) -> None:
        """消费循环"""
        while self.running:
            for partition in self.assigned_partitions:
                message = partition.get_next_message()
                if message:
                    print(f"消费者 {self.consumer_id} 从分区 {partition.topic}-{partition.partition_id} 消费: {message}")
                    # 模拟处理时间
                    time.sleep(random.uniform(0.1, 0.3))
            time.sleep(0.1)

    def stop_consuming(self) -> None:
        """停止消费"""
        self.running = False


class KafkaConsumerGroup:
    """Kafka消费者组类"""

    def __init__(self, group_id: str):
        self.group_id = group_id
        self.consumers: Dict[str, KafkaConsumer] = {}
        self.partitions: List[KafkaPartition] = []
        self.assignment_strategy = "round_robin"

    def add_consumer(self, consumer_id: str) -> KafkaConsumer:
        """添加消费者到组"""
        consumer = KafkaConsumer(consumer_id, self.group_id)
        self.consumers[consumer_id] = consumer
        self._rebalance()
        return consumer

    def remove_consumer(self, consumer_id: str) -> None:
        """从组中移除消费者"""
        if consumer_id in self.consumers:
            del self.consumers[consumer_id]
            self._rebalance()

    def add_partition(self, topic: str, partition_id: int) -> KafkaPartition:
        """添加分区"""
        partition = KafkaPartition(topic, partition_id)
        self.partitions.append(partition)
        self._rebalance()
        return partition

    def _rebalance(self) -> None:
        """重新平衡分区分配（模拟消费者组重平衡）"""
        if not self.consumers or not self.partitions:
            return

        print(f"\n=== 消费者组 '{self.group_id}' 正在重平衡 ===")

        # 简单的轮询分配策略
        consumers_list = list(self.consumers.values())
        num_consumers = len(consumers_list)

        # 清空所有消费者的分区分配
        for consumer in consumers_list:
            consumer.assigned_partitions = []

        # 分配分区给消费者
        for i, partition in enumerate(self.partitions):
            consumer_index = i % num_consumers
            consumers_list[consumer_index].assign_partitions(
                consumers_list[consumer_index].assigned_partitions + [partition]
            )

        print("=== 重平衡完成 ===\n")


def main():
    """主函数 - 演示消费者组行为"""
    print("=== Kafka消费者组行为模拟 ===\n")

    # 创建消费者组
    group = KafkaConsumerGroup("order-processing-group")

    # 创建主题分区
    topic = "orders"
    for i in range(3):  # 3个分区
        partition = group.add_partition(topic, i)
        # 向每个分区添加一些消息
        for j in range(5):
            partition.add_message(f"订单消息-{i}-{j}")

    # 添加消费者
    consumer1 = group.add_consumer("consumer-1")
    consumer2 = group.add_consumer("consumer-2")

    # 开始消费
    consumer1.start_consuming()
    consumer2.start_consuming()

    time.sleep(2)

    # 模拟添加新消费者（触发重平衡）
    print("\n--- 添加新消费者 ---")
    consumer3 = group.add_consumer("consumer-3")
    consumer3.start_consuming()

    time.sleep(3)

    # 模拟消费者离开（触发重平衡）
    print("\n--- 消费者1离开 ---")
    consumer1.stop_consuming()
    group.remove_consumer("consumer-1")

    time.sleep(3)

    print("\n=== 演示结束 ===")


if __name__ == "__main__":
    main()