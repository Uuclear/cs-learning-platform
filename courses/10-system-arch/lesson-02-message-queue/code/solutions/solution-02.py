#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02: Kafka消费者组实现
完整的消费者组实现，支持动态重平衡和分区分配
"""

import threading
import time
import random
from typing import List, Dict, Optional
from collections import defaultdict


class Partition:
    """分区类"""

    def __init__(self, topic: str, partition_id: int):
        self.topic = topic
        self.partition_id = partition_id
        self.messages = []
        self.offset = 0
        self.lock = threading.Lock()

    def add_message(self, message: str) -> None:
        with self.lock:
            self.messages.append(message)

    def get_message(self) -> Optional[str]:
        with self.lock:
            if self.offset < len(self.messages):
                msg = self.messages[self.offset]
                self.offset += 1
                return msg
            return None

    def __str__(self):
        return f"{self.topic}-{self.partition_id}"


class Consumer:
    """消费者类"""

    def __init__(self, consumer_id: str, group_id: str):
        self.consumer_id = consumer_id
        self.group_id = group_id
        self.partitions: List[Partition] = []
        self.running = False
        self.processed_count = 0

    def assign_partitions(self, partitions: List[Partition]) -> None:
        self.partitions = partitions.copy()

    def start_consuming(self) -> None:
        self.running = True
        thread = threading.Thread(target=self._consume_loop, daemon=True)
        thread.start()

    def _consume_loop(self) -> None:
        while self.running:
            for partition in self.partitions:
                msg = partition.get_message()
                if msg:
                    print(f"消费者 {self.consumer_id} 处理 {partition}: {msg}")
                    self.processed_count += 1
                    time.sleep(0.05)
            time.sleep(0.1)

    def stop(self) -> None:
        self.running = False


class ConsumerGroup:
    """消费者组类"""

    def __init__(self, group_id: str):
        self.group_id = group_id
        self.consumers: Dict[str, Consumer] = {}
        self.partitions: List[Partition] = []
        self.rebalance_lock = threading.Lock()

    def add_consumer(self, consumer_id: str) -> Consumer:
        with self.rebalance_lock:
            consumer = Consumer(consumer_id, self.group_id)
            self.consumers[consumer_id] = consumer
            self._rebalance()
            return consumer

    def remove_consumer(self, consumer_id: str) -> None:
        with self.rebalance_lock:
            if consumer_id in self.consumers:
                del self.consumers[consumer_id]
                self._rebalance()

    def add_partition(self, topic: str, partition_id: int) -> Partition:
        with self.rebalance_lock:
            partition = Partition(topic, partition_id)
            self.partitions.append(partition)
            self._rebalance()
            return partition

    def _rebalance(self) -> None:
        """重新分配分区"""
        if not self.consumers or not self.partitions:
            return

        print(f"\n🔄 消费者组 '{self.group_id}' 重平衡中...")

        # 清空所有分配
        for consumer in self.consumers.values():
            consumer.assign_partitions([])

        # 轮询分配
        consumers_list = list(self.consumers.values())
        for i, partition in enumerate(self.partitions):
            consumer_idx = i % len(consumers_list)
            consumers_list[consumer_idx].assign_partitions(
                consumers_list[consumer_idx].partitions + [partition]
            )

        print("✅ 重平衡完成")
        for consumer in consumers_list:
            partition_names = [str(p) for p in consumer.partitions]
            print(f"  消费者 {consumer.consumer_id}: {partition_names}")


def main():
    """主函数"""
    group = ConsumerGroup("payment-processing")

    # 创建分区
    for i in range(4):
        partition = group.add_partition("payments", i)
        for j in range(3):
            partition.add_message(f"支付消息-{i}-{j}")

    # 添加消费者
    c1 = group.add_consumer("consumer-A")
    c2 = group.add_consumer("consumer-B")

    c1.start_consuming()
    c2.start_consuming()

    time.sleep(2)

    # 动态添加消费者
    print("\n➕ 添加新消费者 C")
    c3 = group.add_consumer("consumer-C")
    c3.start_consuming()

    time.sleep(3)

    # 移除消费者
    print("\n➖ 移除消费者 A")
    c1.stop()
    group.remove_consumer("consumer-A")

    time.sleep(2)

    print("\n📊 最终处理统计:")
    for cid, consumer in group.consumers.items():
        print(f"  {cid}: {consumer.processed_count} 条消息")


if __name__ == "__main__":
    main()