#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 01: 发布-订阅模式模拟
演示消息队列中的发布-订阅模式，使用Python标准库实现
"""

import queue
import threading
import time
import random
from typing import List, Callable


class MessageBroker:
    """消息代理类，模拟发布-订阅模式"""

    def __init__(self):
        # 存储主题和对应的订阅者队列
        self.topics: dict = {}
        # 存储消费者线程
        self.consumers: List[threading.Thread] = []

    def subscribe(self, topic: str, callback: Callable[[str], None]) -> None:
        """订阅指定主题

        Args:
            topic: 主题名称
            callback: 接收到消息时的回调函数
        """
        if topic not in self.topics:
            self.topics[topic] = queue.Queue()

        # 创建消费者线程处理消息
        consumer_thread = threading.Thread(
            target=self._consume_messages,
            args=(topic, callback),
            daemon=True
        )
        self.consumers.append(consumer_thread)
        consumer_thread.start()

    def publish(self, topic: str, message: str) -> None:
        """向指定主题发布消息

        Args:
            topic: 主题名称
            message: 要发布的消息内容
        """
        if topic in self.topics:
            self.topics[topic].put(message)
            print(f"发布消息到主题 '{topic}': {message}")

    def _consume_messages(self, topic: str, callback: Callable[[str], None]) -> None:
        """消费消息的内部方法

        Args:
            topic: 主题名称
            callback: 回调函数
        """
        while True:
            try:
                # 阻塞等待消息，超时1秒避免无限阻塞
                message = self.topics[topic].get(timeout=1)
                callback(message)
                self.topics[topic].task_done()
            except queue.Empty:
                continue


def order_service_callback(message: str) -> None:
    """订单服务回调函数 - 模拟订单处理"""
    print(f"订单服务接收到消息: {message}")
    # 模拟处理时间
    time.sleep(0.5)
    print(f"订单服务处理完成: {message}")


def notification_service_callback(message: str) -> None:
    """通知服务回调函数 - 模拟发送通知"""
    print(f"通知服务接收到消息: {message}")
    # 模拟发送通知
    time.sleep(0.3)
    print(f"通知已发送: {message}")


def inventory_service_callback(message: str) -> None:
    """库存服务回调函数 - 模拟库存更新"""
    print(f"库存服务接收到消息: {message}")
    # 模拟库存更新
    time.sleep(0.4)
    print(f"库存已更新: {message}")


def main():
    """主函数 - 演示发布-订阅模式"""
    print("=== 发布-订阅模式演示 ===\n")

    # 创建消息代理
    broker = MessageBroker()

    # 订阅订单主题
    topic = "order-events"
    broker.subscribe(topic, order_service_callback)
    broker.subscribe(topic, notification_service_callback)
    broker.subscribe(topic, inventory_service_callback)

    # 发布一些订单消息
    orders = [
        "订单 #1001: 用户购买商品A",
        "订单 #1002: 用户购买商品B",
        "订单 #1003: 用户购买商品C"
    ]

    for order in orders:
        broker.publish(topic, order)
        # 随机间隔模拟真实场景
        time.sleep(random.uniform(0.1, 0.3))

    # 等待所有消息处理完成
    print("\n等待消息处理完成...")
    time.sleep(3)
    print("\n=== 演示结束 ===")


if __name__ == "__main__":
    main()