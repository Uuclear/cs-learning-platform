#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MQTT 模拟示例 - 物联网消息协议仿真

本示例模拟 MQTT (Message Queuing Telemetry Transport) 协议的基本工作原理。
MQTT 是一种轻量级的发布/订阅消息传输协议，专为低带宽、高延迟或不可靠网络设计，
广泛应用于物联网设备通信。

主要组件：
- Broker (代理服务器)：消息中介，负责接收和分发消息
- Publisher (发布者)：发送消息到特定主题
- Subscriber (订阅者)：订阅特定主题并接收消息
"""

import threading
import time
import json
from collections import defaultdict
from typing import Dict, List, Callable, Any


class MQTTSimulatedBroker:
    """模拟的 MQTT 代理服务器"""

    def __init__(self):
        self.topics: Dict[str, List[Callable]] = defaultdict(list)
        self.messages: Dict[str, List[Any]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable):
        """订阅指定主题"""
        self.topics[topic].append(callback)
        print(f"✅ 订阅成功: 主题 '{topic}'")

    def publish(self, topic: str, message: Any):
        """向指定主题发布消息"""
        # 存储消息历史
        self.messages[topic].append(message)

        # 向所有订阅者发送消息
        if topic in self.topics:
            for callback in self.topics[topic]:
                callback(topic, message)

        print(f"📤 发布消息: 主题 '{topic}' -> {message}")

    def get_message_history(self, topic: str) -> List[Any]:
        """获取指定主题的消息历史"""
        return self.messages[topic]


class MQTTSimulatedDevice:
    """模拟的 MQTT 设备（可以是发布者或订阅者）"""

    def __init__(self, device_id: str, broker: MQTTSimulatedBroker):
        self.device_id = device_id
        self.broker = broker

    def subscribe(self, topic: str):
        """订阅主题"""
        def message_handler(topic: str, message: Any):
            print(f"📡 [{self.device_id}] 收到消息 - 主题: {topic}, 内容: {message}")

        self.broker.subscribe(topic, message_handler)

    def publish(self, topic: str, message: Any):
        """发布消息"""
        self.broker.publish(topic, message)


def main():
    """主函数 - 演示 MQTT 基本功能"""
    print("🚀 开始 MQTT 模拟演示")
    print("=" * 50)

    # 创建代理服务器
    broker = MQTTSimulatedBroker()

    # 创建设备
    sensor_device = MQTTSimulatedDevice("温度传感器-001", broker)
    display_device = MQTTSimulatedDevice("控制面板-001", broker)
    cloud_service = MQTTSimulatedDevice("云服务-001", broker)

    # 订阅主题
    display_device.subscribe("sensors/temperature")
    cloud_service.subscribe("sensors/temperature")
    cloud_service.subscribe("sensors/humidity")

    print("\n📡 设备已连接并订阅主题")
    print("- 控制面板订阅: sensors/temperature")
    print("- 云服务订阅: sensors/temperature, sensors/humidity")

    # 模拟传感器数据发布
    print("\n🌡️  开始发布传感器数据...")
    time.sleep(1)

    # 发布温度数据
    temperature_data = {
        "device": "温度传感器-001",
        "timestamp": time.time(),
        "value": 23.5,
        "unit": "°C"
    }
    sensor_device.publish("sensors/temperature", temperature_data)

    time.sleep(1)

    # 发布湿度数据
    humidity_data = {
        "device": "湿度传感器-002",
        "timestamp": time.time(),
        "value": 65.2,
        "unit": "%"
    }
    sensor_device.publish("sensors/humidity", humidity_data)

    print("\n📊 消息历史:")
    print("温度消息:", broker.get_message_history("sensors/temperature"))
    print("湿度消息:", broker.get_message_history("sensors/humidity"))

    print("\n✅ MQTT 模拟演示完成！")


if __name__ == "__main__":
    main()