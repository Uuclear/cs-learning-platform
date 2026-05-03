#!/usr/bin/env python3
"""
Example 02: 串口通信数据帧解析模拟器

这个程序模拟了单片机如何通过串口 (UART) 接收和解析数据帧。
在嵌入式系统中，串口通信是调试和设备间通信的重要方式。
"""

import time
import random
import struct

class UARTSimulator:
    """串口通信模拟器"""
    def __init__(self, baud_rate=9600):
        self.baud_rate = baud_rate
        self.buffer = bytearray()
        self.received_frames = []

    def send_data(self, data):
        """发送数据到串口 (模拟其他设备发送数据)"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, int):
            data = struct.pack('B', data)
        elif isinstance(data, list):
            data = bytearray(data)

        print(f"发送数据: {data.hex() if isinstance(data, (bytes, bytearray)) else data}")
        # 模拟数据传输延迟
        transmission_time = len(data) * 10 / self.baud_rate
        time.sleep(transmission_time)
        self.buffer.extend(data)

    def receive_frame(self, frame_length=None, delimiter=b'\n'):
        """接收并解析一个数据帧"""
        if frame_length:
            # 固定长度帧
            if len(self.buffer) >= frame_length:
                frame = self.buffer[:frame_length]
                self.buffer = self.buffer[frame_length:]
                return bytes(frame)
        else:
            # 以分隔符结尾的帧
            delimiter_pos = self.buffer.find(delimiter)
            if delimiter_pos != -1:
                frame = self.buffer[:delimiter_pos]
                self.buffer = self.buffer[delimiter_pos + len(delimiter):]
                return bytes(frame)

        return None

    def parse_sensor_data(self, frame):
        """解析传感器数据帧 (假设格式: [温度(2字节)][湿度(2字节)][校验和(1字节)])"""
        if len(frame) == 5:
            temp_raw, humidity_raw, checksum = struct.unpack('<HHB', frame)

            # 简单的校验和验证
            calculated_checksum = (temp_raw + humidity_raw) & 0xFF
            if calculated_checksum == checksum:
                temperature = temp_raw / 10.0  # 假设温度值需要除以10
                humidity = humidity_raw / 10.0  # 假设湿度值需要除以10
                return {
                    'temperature': temperature,
                    'humidity': humidity,
                    'valid': True
                }
            else:
                return {'valid': False, 'error': '校验和错误'}
        else:
            return {'valid': False, 'error': '帧长度错误'}

def simulate_sensor_data():
    """生成模拟的传感器数据"""
    temperature = int(random.uniform(20.0, 35.0) * 10)  # 20.0-35.0°C
    humidity = int(random.uniform(40.0, 80.0) * 10)     # 40.0-80.0%
    checksum = (temperature + humidity) & 0xFF
    return struct.pack('<HHB', temperature, humidity, checksum)

def main():
    """主函数 - 演示串口通信和数据解析"""
    print("=== 单片机串口通信模拟演示 ===\n")

    # 创建串口模拟器
    uart = UARTSimulator(baud_rate=9600)

    print("1. 发送简单的文本消息:")
    uart.send_data("Hello, Microcontroller!\n")

    # 接收文本帧
    text_frame = uart.receive_frame(delimiter=b'\n')
    if text_frame:
        print(f"接收到文本: {text_frame.decode('utf-8', errors='replace')}")

    print("\n2. 发送和解析传感器数据:")
    for i in range(3):
        # 生成并发送传感器数据
        sensor_data = simulate_sensor_data()
        uart.send_data(sensor_data)

        # 接收并解析传感器数据
        sensor_frame = uart.receive_frame(frame_length=5)
        if sensor_frame:
            parsed_data = uart.parse_sensor_data(sensor_frame)
            if parsed_data['valid']:
                print(f"传感器数据 #{i+1}: 温度={parsed_data['temperature']:.1f}°C, 湿度={parsed_data['humidity']:.1f}%")
            else:
                print(f"传感器数据 #{i+1}: {parsed_data['error']}")

    print("\n3. 发送命令帧:")
    # 模拟发送控制命令 (例如: [命令ID][参数][校验和])
    command_id = 0x01  # 开灯命令
    parameter = 0xFF   # 参数 (全亮)
    cmd_checksum = (command_id + parameter) & 0xFF
    command_frame = bytes([command_id, parameter, cmd_checksum])

    uart.send_data(command_frame)
    received_cmd = uart.receive_frame(frame_length=3)
    if received_cmd and len(received_cmd) == 3:
        cmd_id, param, chk = received_cmd
        if (cmd_id + param) & 0xFF == chk:
            print(f"接收到有效命令: ID=0x{cmd_id:02X}, 参数=0x{param:02X}")
        else:
            print("命令帧校验失败!")

    print("\n串口通信模拟完成!")

if __name__ == "__main__":
    main()