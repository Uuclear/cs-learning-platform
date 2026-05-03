#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03 - 简化的 IoT 架构

演示基本的 IoT 设备到云的数据流。
"""

class Device:
    def __init__(self, device_id):
        self.device_id = device_id

    def generate_data(self):
        return {"device_id": self.device_id, "data": "sensor_value"}


class Gateway:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def collect_data(self):
        data_list = []
        for device in self.devices:
            data_list.append(device.generate_data())
        return data_list


class Cloud:
    def __init__(self):
        self.data_store = []

    def store_data(self, data):
        self.data_store.append(data)


def main():
    # 创建组件
    cloud = Cloud()
    gateway = Gateway()

    # 添加设备
    device1 = Device("device_001")
    device2 = Device("device_002")
    gateway.add_device(device1)
    gateway.add_device(device2)

    # 数据流
    data = gateway.collect_data()
    for item in data:
        cloud.store_data(item)

    print(f"云平台存储了 {len(cloud.data_store)} 条数据记录")

    return True


if __name__ == "__main__":
    main()