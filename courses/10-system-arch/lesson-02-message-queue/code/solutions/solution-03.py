#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03: 可靠消息传递实现
实现可靠的消息传递系统，支持恰好一次语义
"""

import threading
import time
import random
import json
from typing import Optional, Dict, Set
from dataclasses import dataclass


@dataclass
class Message:
    id: str
    content: str
    timestamp: float


class ReliableMessageQueue:
    """可靠消息队列"""

    def __init__(self):
        self.messages: Dict[str, Message] = {}
        self.acknowledged: Set[str] = set()
        self.delivered: Set[str] = set()
        self.lock = threading.Lock()

    def enqueue(self, message_id: str, content: str) -> None:
        with self.lock:
            self.messages[message_id] = Message(message_id, content, time.time())

    def dequeue(self) -> Optional[Message]:
        with self.lock:
            # 找到未确认的消息
            for msg_id, msg in self.messages.items():
                if msg_id not in self.acknowledged:
                    self.delivered.add(msg_id)
                    return msg
            return None

    def acknowledge(self, message_id: str) -> bool:
        with self.lock:
            if message_id in self.messages and message_id not in self.acknowledged:
                self.acknowledged.add(message_id)
                return True
            return False

    def get_stats(self) -> Dict:
        with self.lock:
            return {
                "total": len(self.messages),
                "delivered": len(self.delivered),
                "acknowledged": len(self.acknowledged)
            }


class IdempotentProcessor:
    """幂等处理器"""

    def __init__(self):
        self.processed: Set[str] = set()
        self.results: Dict[str, str] = {}
        self.lock = threading.Lock()

    def process(self, message: Message) -> str:
        with self.lock:
            if message.id in self.processed:
                return f"重复处理 {message.id}: {self.results[message.id]}"

            # 实际处理逻辑
            result = f"处理结果-{message.content.upper()}"
            self.processed.add(message.id)
            self.results[message.id] = result
            return result


def producer_thread(queue: ReliableMessageQueue, stop_event: threading.Event):
    """生产者线程"""
    msg_count = 0
    while not stop_event.is_set():
        msg_id = f"msg-{msg_count:04d}"
        content = f"订单数据-{msg_count}"
        queue.enqueue(msg_id, content)
        print(f"📦 生产消息: {msg_id}")
        msg_count += 1
        time.sleep(0.5)


def consumer_thread(queue: ReliableMessageQueue, processor: IdempotentProcessor,
                   stop_event: threading.Event, consumer_id: str):
    """消费者线程"""
    while not stop_event.is_set():
        msg = queue.dequeue()
        if msg:
            result = processor.process(msg)
            print(f"✅ 消费者 {consumer_id} {result}")

            # 随机确认（模拟网络问题）
            if random.random() > 0.1:  # 90% 确认成功率
                if queue.acknowledge(msg.id):
                    print(f"📨 确认消息: {msg.id}")
            else:
                print(f"❌ 确认失败: {msg.id} (将重试)")
        time.sleep(0.2)


def main():
    """主函数"""
    print("=== 可靠消息传递系统 ===\n")

    queue = ReliableMessageQueue()
    processor = IdempotentProcessor()
    stop_event = threading.Event()

    # 启动生产者
    producer = threading.Thread(target=producer_thread, args=(queue, stop_event))
    producer.start()

    # 启动多个消费者（模拟重复消费）
    consumers = []
    for i in range(2):
        consumer = threading.Thread(
            target=consumer_thread,
            args=(queue, processor, stop_event, f"C{i+1}")
        )
        consumers.append(consumer)
        consumer.start()

    # 运行一段时间
    time.sleep(8)
    stop_event.set()

    # 等待线程结束
    producer.join()
    for consumer in consumers:
        consumer.join()

    # 显示统计信息
    stats = queue.get_stats()
    print(f"\n📊 最终统计: {stats}")
    print(f"🔄 处理器状态: {len(processor.processed)} 条唯一消息")


if __name__ == "__main__":
    main()