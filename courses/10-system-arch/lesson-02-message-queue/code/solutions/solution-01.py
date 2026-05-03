#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: 发布-订阅模式实现
完整的发布-订阅模式实现，包含错误处理和优雅关闭
"""

import queue
import threading
import time
import random
from typing import List, Callable, Dict


class MessageBroker:
    """增强版消息代理类"""

    def __init__(self):
        self.topics: Dict[str, queue.Queue] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
        self.consumers: List[threading.Thread] = []
        self.running = True

    def subscribe(self, topic: str, callback: Callable[[str], None]) -> None:
        """订阅主题"""
        if topic not in self.topics:
            self.topics[topic] = queue.Queue()
            self.subscribers[topic] = []

        self.subscribers[topic].append(callback)

        # 启动消费者线程（每个主题一个线程）
        if not any(t.name == f"consumer-{topic}" for t in self.consumers):
            consumer_thread = threading.Thread(
                target=self._consume_messages,
                args=(topic,),
                name=f"consumer-{topic}",
                daemon=True
            )
            self.consumers.append(consumer_thread)
            consumer_thread.start()

    def publish(self, topic: str, message: str) -> bool:
        """发布消息到主题"""
        if topic not in self.topics:
            return False

        try:
            self.topics[topic].put(message, timeout=1)
            return True
        except queue.Full:
            print(f"主题 '{topic}' 队列已满，消息丢失: {message}")
            return False

    def _consume_messages(self, topic: str) -> None:
        """消费消息"""
        while self.running:
            try:
                message = self.topics[topic].get(timeout=0.5)
                for callback in self.subscribers[topic]:
                    try:
                        callback(message)
                    except Exception as e:
                        print(f"回调函数执行错误: {e}")
                self.topics[topic].task_done()
            except queue.Empty:
                continue

    def shutdown(self) -> None:
        """优雅关闭"""
        self.running = False
        for topic in self.topics:
            self.topics[topic].join()  # 等待所有消息处理完成


def main():
    """主函数"""
    broker = MessageBroker()

    def service_callback(service_name: str, message: str):
        print(f"{service_name} 处理: {message}")
        time.sleep(0.1)

    # 创建多个服务的回调
    services = ["订单服务", "通知服务", "库存服务", "日志服务"]
    for service in services:
        broker.subscribe("order-events", lambda msg, s=service: service_callback(s, msg))

    # 发布消息
    for i in range(5):
        broker.publish("order-events", f"订单 #{i+1000}")
        time.sleep(0.2)

    time.sleep(2)
    broker.shutdown()
    print("系统关闭")


if __name__ == "__main__":
    main()