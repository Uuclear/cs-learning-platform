#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物联网传感器数据收集与聚合示例

本示例模拟多个 IoT 传感器设备的数据收集过程，并展示如何将分散的传感器数据
进行聚合处理，为上层应用提供统一的数据视图。
"""

import random
import time
import json
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict


class SensorSimulator:
    """传感器模拟器基类"""

    def __init__(self, sensor_id: str, sensor_type: str):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.last_reading = None

    def read(self) -> Dict[str, Any]:
        """读取传感器数据"""
        raise NotImplementedError("子类必须实现 read 方法")


class TemperatureSensor(SensorSimulator):
    """温度传感器"""

    def __init__(self, sensor_id: str, location: str = "未知"):
        super().__init__(sensor_id, "temperature")
        self.location = location
        self.base_temp = random.uniform(15.0, 30.0)  # 基础温度

    def read(self) -> Dict[str, Any]:
        # 模拟温度波动（±2°C）
        temp = self.base_temp + random.uniform(-2.0, 2.0)
        self.last_reading = {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type,
            "location": self.location,
            "value": round(temp, 2),
            "unit": "°C",
            "timestamp": datetime.now().isoformat()
        }
        return self.last_reading


class HumiditySensor(SensorSimulator):
    """湿度传感器"""

    def __init__(self, sensor_id: str, location: str = "未知"):
        super().__init__(sensor_id, "humidity")
        self.location = location
        self.base_humidity = random.uniform(40.0, 80.0)  # 基础湿度

    def read(self) -> Dict[str, Any]:
        # 模拟湿度波动（±5%）
        humidity = self.base_humidity + random.uniform(-5.0, 5.0)
        humidity = max(0.0, min(100.0, humidity))  # 限制在 0-100%
        self.last_reading = {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type,
            "location": self.location,
            "value": round(humidity, 2),
            "unit": "%",
            "timestamp": datetime.now().isoformat()
        }
        return self.last_reading


class MotionSensor(SensorSimulator):
    """运动传感器"""

    def __init__(self, sensor_id: str, location: str = "未知"):
        super().__init__(sensor_id, "motion")
        self.location = location

    def read(self) -> Dict[str, Any]:
        # 10% 概率检测到运动
        motion_detected = random.random() < 0.1
        self.last_reading = {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type,
            "location": self.location,
            "value": motion_detected,
            "unit": "boolean",
            "timestamp": datetime.now().isoformat()
        }
        return self.last_reading


class SensorDataManager:
    """传感器数据管理器 - 负责收集和聚合数据"""

    def __init__(self):
        self.sensors: List[SensorSimulator] = []
        self.data_history: Dict[str, List[Dict]] = defaultdict(list)

    def add_sensor(self, sensor: SensorSimulator):
        """添加传感器"""
        self.sensors.append(sensor)
        print(f"✅ 添加传感器: {sensor.sensor_id} ({sensor.sensor_type})")

    def collect_data(self) -> List[Dict[str, Any]]:
        """收集所有传感器的当前数据"""
        current_data = []
        for sensor in self.sensors:
            data = sensor.read()
            current_data.append(data)
            self.data_history[sensor.sensor_type].append(data)
        return current_data

    def get_aggregated_data(self) -> Dict[str, Any]:
        """获取聚合后的数据视图"""
        if not self.data_history:
            return {}

        aggregated = {}

        # 温度聚合统计
        if "temperature" in self.data_history:
            temps = [d["value"] for d in self.data_history["temperature"]]
            aggregated["temperature"] = {
                "count": len(temps),
                "average": round(sum(temps) / len(temps), 2),
                "min": min(temps),
                "max": max(temps)
            }

        # 湿度聚合统计
        if "humidity" in self.data_history:
            humids = [d["value"] for d in self.data_history["humidity"]]
            aggregated["humidity"] = {
                "count": len(humids),
                "average": round(sum(humids) / len(humids), 2),
                "min": min(humids),
                "max": max(humids)
            }

        # 运动检测统计
        if "motion" in self.data_history:
            motions = [d["value"] for d in self.data_history["motion"]]
            detected_count = sum(motions)
            aggregated["motion"] = {
                "total_readings": len(motions),
                "detections": detected_count,
                "detection_rate": round(detected_count / len(motions) * 100, 2) if motions else 0
            }

        return aggregated

    def get_recent_data(self, limit: int = 5) -> List[Dict[str, Any]]:
        """获取最近的传感器数据"""
        all_data = []
        for sensor_type in self.data_history:
            all_data.extend(self.data_history[sensor_type][-limit:])
        # 按时间戳排序
        all_data.sort(key=lambda x: x["timestamp"], reverse=True)
        return all_data[:limit]


def main():
    """主函数 - 演示传感器数据收集与聚合"""
    print("🌡️  物联网传感器数据收集与聚合演示")
    print("=" * 50)

    # 创建数据管理器
    manager = SensorDataManager()

    # 创建各种传感器
    manager.add_sensor(TemperatureSensor("TEMP-001", "客厅"))
    manager.add_sensor(TemperatureSensor("TEMP-002", "卧室"))
    manager.add_sensor(HumiditySensor("HUMID-001", "客厅"))
    manager.add_sensor(HumiditySensor("HUMID-002", "厨房"))
    manager.add_sensor(MotionSensor("MOTION-001", "入口"))
    manager.add_sensor(MotionSensor("MOTION-002", "走廊"))

    print(f"\n📊 开始收集传感器数据...")

    # 收集多轮数据
    for i in range(3):
        print(f"\n🔄 第 {i+1} 轮数据收集:")
        data = manager.collect_data()
        for reading in data:
            print(f"  📡 {reading['sensor_id']}: {reading['value']} {reading['unit']}")
        time.sleep(0.5)

    # 显示聚合数据
    print("\n📈 聚合数据分析:")
    aggregated = manager.get_aggregated_data()
    for sensor_type, stats in aggregated.items():
        print(f"  {sensor_type.upper()}: {stats}")

    # 显示最近数据
    print("\n🆕 最近 5 条传感器数据:")
    recent = manager.get_recent_data(5)
    for data in recent:
        print(f"  📡 {data['sensor_id']} ({data['location']}): {data['value']} {data['unit']} @ {data['timestamp'][:19]}")

    print("\n✅ 传感器数据收集与聚合演示完成！")


if __name__ == "__main__":
    main()