#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物联网架构模拟 - 设备到云端的数据流仿真

本示例模拟完整的 IoT 架构，包括：
1. 边缘设备 (Edge Devices) - 生成原始传感器数据
2. 网关 (Gateway) - 数据预处理和协议转换
3. 云平台 (Cloud Platform) - 数据存储、分析和应用服务
4. 应用层 (Applications) - 用户界面和业务逻辑
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque


class EdgeDevice:
    """边缘设备 - 物联网的最底层设备"""

    def __init__(self, device_id: str, device_type: str, location: str):
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
        self.is_connected = False

    def generate_sensor_data(self) -> Dict[str, Any]:
        """生成传感器数据"""
        import random

        base_data = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "location": self.location,
            "timestamp": datetime.now().isoformat(),
            "battery_level": random.randint(20, 100)
        }

        # 根据设备类型生成特定数据
        if self.device_type == "temperature_sensor":
            base_data["temperature"] = round(random.uniform(15.0, 35.0), 2)
            base_data["unit"] = "°C"
        elif self.device_type == "humidity_sensor":
            base_data["humidity"] = round(random.uniform(30.0, 90.0), 2)
            base_data["unit"] = "%"
        elif self.device_type == "motion_sensor":
            base_data["motion_detected"] = random.random() < 0.15
        elif self.device_type == "light_sensor":
            base_data["light_level"] = random.randint(0, 1000)
            base_data["unit"] = "lux"

        return base_data

    def connect(self):
        """连接到网关"""
        self.is_connected = True
        print(f"🔌 [{self.device_id}] 已连接到网关")

    def disconnect(self):
        """断开连接"""
        self.is_connected = False
        print(f"🔌 [{self.device_id}] 已断开连接")


class IoTGateway:
    """IoT 网关 - 连接边缘设备和云平台的中介"""

    def __init__(self, gateway_id: str):
        self.gateway_id = gateway_id
        self.connected_devices: List[EdgeDevice] = []
        self.data_buffer = deque(maxlen=100)  # 缓冲区
        self.cloud_platform = None

    def register_device(self, device: EdgeDevice):
        """注册设备到网关"""
        device.connect()
        self.connected_devices.append(device)
        print(f"✅ 网关 [{self.gateway_id}] 注册设备: {device.device_id}")

    def unregister_device(self, device: EdgeDevice):
        """从网关注销设备"""
        if device in self.connected_devices:
            device.disconnect()
            self.connected_devices.remove(device)
            print(f"❌ 网关 [{self.gateway_id}] 注销设备: {device.device_id}")

    def set_cloud_platform(self, cloud_platform):
        """设置云平台连接"""
        self.cloud_platform = cloud_platform
        print(f"☁️  网关 [{self.gateway_id}] 连接到云平台")

    def collect_and_forward_data(self):
        """收集设备数据并转发到云平台"""
        if not self.connected_devices:
            return

        # 收集所有设备的数据
        for device in self.connected_devices:
            if device.is_connected:
                data = device.generate_sensor_data()
                self.data_buffer.append(data)

                # 数据预处理（添加网关信息）
                processed_data = {
                    **data,
                    "gateway_id": self.gateway_id,
                    "processed_at": datetime.now().isoformat()
                }

                # 转发到云平台
                if self.cloud_platform:
                    self.cloud_platform.receive_data(processed_data)

    def get_buffer_status(self) -> Dict[str, int]:
        """获取缓冲区状态"""
        return {
            "current_size": len(self.data_buffer),
            "max_capacity": self.data_buffer.maxlen
        }


class CloudPlatform:
    """云平台 - 数据存储、处理和应用服务"""

    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.data_store: List[Dict[str, Any]] = []
        self.applications: List['IoTApplication'] = []

    def receive_data(self, data: Dict[str, Any]):
        """接收来自网关的数据"""
        self.data_store.append(data)
        print(f"📥 云平台 [{self.platform_name}] 接收数据: {data['device_id']} -> {data.get('temperature', data.get('humidity', '...'))}")

        # 通知所有应用
        for app in self.applications:
            app.process_new_data(data)

    def add_application(self, application: 'IoTApplication'):
        """添加应用到平台"""
        self.applications.append(application)
        print(f"📱 云平台 [{self.platform_name}] 添加应用: {application.app_name}")

    def get_storage_stats(self) -> Dict[str, int]:
        """获取存储统计"""
        return {
            "total_records": len(self.data_store),
            "unique_devices": len(set(d["device_id"] for d in self.data_store))
        }


class IoTApplication:
    """IoT 应用 - 用户界面和业务逻辑"""

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.alerts: List[str] = []

    def process_new_data(self, data: Dict[str, Any]):
        """处理新数据"""
        # 示例：温度过高告警
        if "temperature" in data and data["temperature"] > 30.0:
            alert = f"⚠️ 高温告警: {data['location']} 温度 {data['temperature']}°C"
            self.alerts.append(alert)
            print(f"🔔 [{self.app_name}] {alert}")

        # 示例：电池电量低告警
        if data.get("battery_level", 100) < 30:
            alert = f"🔋 低电量告警: {data['device_id']} 电量 {data['battery_level']}%"
            self.alerts.append(alert)
            print(f"🔔 [{self.app_name}] {alert}")

    def get_dashboard_data(self) -> Dict[str, Any]:
        """获取仪表板数据"""
        return {
            "app_name": self.app_name,
            "active_alerts": len(self.alerts),
            "recent_alerts": self.alerts[-3:] if self.alerts else []
        }


def simulate_iot_architecture():
    """模拟完整的 IoT 架构"""
    print("🌐 物联网架构模拟演示")
    print("=" * 50)

    # 创建云平台
    cloud = CloudPlatform("AWS IoT Core 模拟")

    # 创建应用
    monitoring_app = IoTApplication("环境监控应用")
    alert_app = IoTApplication("告警管理系统")

    cloud.add_application(monitoring_app)
    cloud.add_application(alert_app)

    # 创建网关
    gateway = IoTGateway("GATEWAY-001")
    gateway.set_cloud_platform(cloud)

    # 创建边缘设备
    devices = [
        EdgeDevice("TEMP-001", "temperature_sensor", "客厅"),
        EdgeDevice("HUMID-001", "humidity_sensor", "客厅"),
        EdgeDevice("MOTION-001", "motion_sensor", "入口"),
        EdgeDevice("LIGHT-001", "light_sensor", "阳台")
    ]

    # 注册设备到网关
    for device in devices:
        gateway.register_device(device)

    print(f"\n📊 开始模拟数据流...")

    # 模拟多轮数据传输
    for round_num in range(3):
        print(f"\n🔄 第 {round_num + 1} 轮数据传输:")
        gateway.collect_and_forward_data()

        # 显示网关状态
        buffer_status = gateway.get_buffer_status()
        print(f"   网关缓冲区: {buffer_status['current_size']}/{buffer_status['max_capacity']}")

        # 显示云平台状态
        storage_stats = cloud.get_storage_stats()
        print(f"   云平台存储: {storage_stats['total_records']} 条记录, {storage_stats['unique_devices']} 个设备")

        time.sleep(1)

    # 显示应用仪表板
    print("\n📱 应用仪表板:")
    for app in [monitoring_app, alert_app]:
        dashboard = app.get_dashboard_data()
        print(f"  {dashboard['app_name']}: {dashboard['active_alerts']} 个活跃告警")
        if dashboard['recent_alerts']:
            print(f"    最近告警: {', '.join(dashboard['recent_alerts'])}")

    print("\n✅ IoT 架构模拟演示完成！")


if __name__ == "__main__":
    simulate_iot_architecture()