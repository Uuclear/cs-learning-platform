#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 03: 消息传递保证模式演示
演示不同消息传递保证模式：至少一次、至多一次、恰好一次
"""

import threading
import time
import random
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Message:
    """消息类"""
    id: str
    content: str
    delivered: bool = False
    processed: bool = False


class AtMostOnceQueue:
    """至多一次传递队列（可能丢失消息）"""

    def __init__(self):
        self.messages: List[Message] = []
        self.delivered_count = 0

    def enqueue(self, message: Message) -> None:
        """入队消息"""
        self.messages.append(message)

    def dequeue(self) -> Optional[Message]:
        """出队消息 - 至多一次语义"""
        if not self.messages:
            return None

        message = self.messages.pop(0)
        # 模拟网络问题导致消息丢失
        if random.random() < 0.2:  # 20% 概率丢失
            print(f"消息 {message.id} 在传输中丢失!")
            return None

        message.delivered = True
        self.delivered_count += 1
        return message


class AtLeastOnceQueue:
    """至少一次传递队列（可能重复）"""

    def __init__(self):
        self.messages: List[Message] = []
        self.acknowledged: set = set()
        self.delivered_count = 0

    def enqueue(self, message: Message) -> None:
        """入队消息"""
        self.messages.append(message)

    def dequeue(self) -> Optional[Message]:
        """出队消息 - 至少一次语义"""
        if not self.messages:
            return None

        message = self.messages[0]  # 不立即移除

        # 模拟ACK丢失导致重复发送
        if random.random() < 0.3:  # 30% 概率ACK丢失
            print(f"消息 {message.id} 的ACK丢失，将重试...")
            # 不移除消息，下次还会发送
        else:
            # 成功ACK，移除消息
            self.messages.pop(0)
            self.acknowledged.add(message.id)

        message.delivered = True
        self.delivered_count += 1
        return message

    def acknowledge(self, message_id: str) -> None:
        """确认消息处理完成"""
        if message_id in [m.id for m in self.messages]:
            # 找到并移除已确认的消息
            self.messages = [m for m in self.messages if m.id != message_id]
            self.acknowledged.add(message_id)


class ExactlyOnceProcessor:
    """恰好一次处理器（使用幂等性）"""

    def __init__(self):
        self.processed_messages: set = set()
        self.processed_count = 0

    def process_message(self, message: Message) -> bool:
        """处理消息 - 确保恰好一次语义"""
        if message.id in self.processed_messages:
            print(f"消息 {message.id} 已处理过，跳过重复处理")
            return False

        # 处理消息
        print(f"处理消息 {message.id}: {message.content}")
        time.sleep(0.1)  # 模拟处理时间

        # 标记为已处理
        self.processed_messages.add(message.id)
        message.processed = True
        self.processed_count += 1
        return True


def simulate_at_most_once():
    """模拟至多一次传递"""
    print("=== 至多一次传递模拟 ===")
    queue = AtMostOnceQueue()
    processor = ExactlyOnceProcessor()

    # 添加消息
    messages = [Message(f"msg-{i}", f"内容-{i}") for i in range(5)]
    for msg in messages:
        queue.enqueue(msg)

    # 消费消息
    delivered = 0
    while delivered < len(messages) and queue.delivered_count < 10:  # 防止无限循环
        msg = queue.dequeue()
        if msg:
            processor.process_message(msg)
            delivered += 1
        time.sleep(0.1)

    print(f"至多一次: 发送{len(messages)}条, 交付{queue.delivered_count}条, 处理{processor.processed_count}条")
    print()


def simulate_at_least_once():
    """模拟至少一次传递"""
    print("=== 至少一次传递模拟 ===")
    queue = AtLeastOnceQueue()
    processor = ExactlyOnceProcessor()

    # 添加消息
    messages = [Message(f"msg-{i}", f"内容-{i}") for i in range(3)]
    for msg in messages:
        queue.enqueue(msg)

    # 消费消息（可能重复）
    attempts = 0
    while attempts < 15:  # 最多尝试15次
        msg = queue.dequeue()
        if msg:
            processor.process_message(msg)
        attempts += 1
        time.sleep(0.1)

    print(f"至少一次: 发送{len(messages)}条, 交付{queue.delivered_count}条, 处理{processor.processed_count}条")
    print()


def simulate_exactly_once():
    """模拟恰好一次传递（结合幂等处理器）"""
    print("=== 恰好一次传递模拟 ===")
    queue = AtLeastOnceQueue()  # 使用至少一次队列 + 幂等处理器
    processor = ExactlyOnceProcessor()

    # 添加消息
    messages = [Message(f"msg-{i}", f"内容-{i}") for i in range(4)]
    for msg in messages:
        queue.enqueue(msg)

    # 消费消息
    attempts = 0
    while attempts < 20:  # 最多尝试20次
        msg = queue.dequeue()
        if msg:
            processor.process_message(msg)
        attempts += 1
        time.sleep(0.1)

    print(f"恰好一次: 发送{len(messages)}条, 交付{queue.delivered_count}条, 处理{processor.processed_count}条")
    print()


def main():
    """主函数 - 演示不同传递保证"""
    print("=== 消息传递保证模式演示 ===\n")

    simulate_at_most_once()
    simulate_at_least_once()
    simulate_exactly_once()

    print("=== 演示结束 ===")


if __name__ == "__main__":
    main()