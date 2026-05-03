#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02 - 传感器数据聚合

简单的传感器数据收集和聚合示例。
"""

class SimpleSensor:
    def __init__(self, sensor_id, sensor_type):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.readings = []

    def read(self, value):
        reading = {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type,
            "value": value
        }
        self.readings.append(reading)
        return reading


class DataAggregator:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def get_average(self, sensor_type):
        values = []
        for sensor in self.sensors:
            if sensor.sensor_type == sensor_type:
                values.extend([r["value"] for r in sensor.readings])
        return sum(values) / len(values) if values else 0


def main():
    aggregator = DataAggregator()

    temp_sensor = SimpleSensor("temp1", "temperature")
    temp_sensor.read(25.5)
    temp_sensor.read(26.0)

    aggregator.add_sensor(temp_sensor)
    avg_temp = aggregator.get_average("temperature")
    print(f"平均温度: {avg_temp}°C")

    return True


if __name__ == "__main__":
    main()