#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01 - MQTT 模拟的简化版本

这是一个简化的 MQTT 模拟实现，用于教学目的。
"""

class SimpleMQTTBroker:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, callback):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def publish(self, topic, message):
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)


def main():
    broker = SimpleMQTTBroker()

    def print_message(msg):
        print(f"收到消息: {msg}")

    broker.subscribe("test/topic", print_message)
    broker.publish("test/topic", "Hello IoT!")

    return True


if __name__ == "__main__":
    main()