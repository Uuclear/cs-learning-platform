#!/usr/bin/env python3
"""
Solution 02: 串口通信数据帧解析模拟器（完整版）

这个完整的解决方案提供了更健壮的串口通信模拟，
包括多种协议格式、错误处理和实时数据流处理。
"""

import time
import random
import struct
import threading
from typing import Optional, Dict, Any, Callable

class UARTSimulator:
    """增强版串口通信模拟器"""
    def __init__(self, baud_rate: int = 9600):
        self.baud_rate = baud_rate
        self.buffer = bytearray()
        self.received_frames = []
        self.error_count = 0
        self.frame_handlers: Dict[str, Callable] = {}
        self._running = False
        self._rx_thread = None

    def register_frame_handler(self, protocol_name: str, handler: Callable) -> None:
        """注册特定协议的帧处理函数"""
        self.frame_handlers[protocol_name] = handler

    def send_data(self, data: bytes) -> None:
        """发送数据到串口"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, int):
            data = struct.pack('B', data)
        elif isinstance(data, list):
            data = bytearray(data)

        print(f"[TX] 发送 {len(data)} 字节: {data.hex()}")

        # 模拟传输延迟
        transmission_time = len(data) * 10 / self.baud_rate
        time.sleep(transmission_time)

        # 将数据添加到接收缓冲区
        self.buffer.extend(data)

    def receive_frame_with_timeout(self, timeout: float = 1.0,
                                 frame_length: Optional[int] = None,
                                 delimiter: bytes = b'\n') -> Optional[bytes]:
        """带超时的帧接收"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            frame = self.receive_frame(frame_length, delimiter)
            if frame is not None:
                return frame
            time.sleep(0.01)  # 短暂休眠避免忙等待
        return None

    def receive_frame(self, frame_length: Optional[int] = None,
                     delimiter: bytes = b'\n') -> Optional[bytes]:
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

    def parse_sensor_data_v1(self, frame: bytes) -> Dict[str, Any]:
        """解析传感器数据帧 v1 格式"""
        if len(frame) == 5:
            temp_raw, humidity_raw, checksum = struct.unpack('<HHB', frame)
            calculated_checksum = (temp_raw + humidity_raw) & 0xFF

            if calculated_checksum == checksum:
                return {
                    'temperature': temp_raw / 10.0,
                    'humidity': humidity_raw / 10.0,
                    'valid': True,
                    'protocol': 'sensor_v1'
                }
            else:
                self.error_count += 1
                return {'valid': False, 'error': '校验和错误', 'protocol': 'sensor_v1'}
        else:
            self.error_count += 1
            return {'valid': False, 'error': '帧长度错误', 'protocol': 'sensor_v1'}

    def parse_command_frame(self, frame: bytes) -> Dict[str, Any]:
        """解析命令帧格式: [CMD_ID][LENGTH][DATA...][CHECKSUM]"""
        if len(frame) < 3:
            self.error_count += 1
            return {'valid': False, 'error': '命令帧太短', 'protocol': 'command'}

        cmd_id, length = struct.unpack('BB', frame[:2])

        if len(frame) != length + 3:  # +3 for CMD_ID, LENGTH, and CHECKSUM
            self.error_count += 1
            return {'valid': False, 'error': '命令长度不匹配', 'protocol': 'command'}

        data = frame[2:-1]  # 排除最后的校验和
        checksum = frame[-1]
        calculated_checksum = (cmd_id + length + sum(data)) & 0xFF

        if calculated_checksum == checksum:
            return {
                'command_id': cmd_id,
                'data': data,
                'valid': True,
                'protocol': 'command'
            }
        else:
            self.error_count += 1
            return {'valid': False, 'error': '命令校验和错误', 'protocol': 'command'}

    def auto_detect_and_parse(self, frame: bytes) -> Dict[str, Any]:
        """自动检测帧类型并解析"""
        # 尝试不同的协议解析器
        protocols_to_try = [
            ('sensor_v1', lambda f: len(f) == 5),
            ('command', lambda f: len(f) >= 3 and f[1] == len(f) - 3),  # 检查长度字段
            ('text', lambda f: all(32 <= b <= 126 for b in f)),  # 可打印ASCII
        ]

        for protocol_name, condition in protocols_to_try:
            if condition(frame):
                if protocol_name == 'sensor_v1':
                    return self.parse_sensor_data_v1(frame)
                elif protocol_name == 'command':
                    return self.parse_command_frame(frame)
                elif protocol_name == 'text':
                    return {
                        'text': frame.decode('utf-8', errors='replace'),
                        'valid': True,
                        'protocol': 'text'
                    }

        self.error_count += 1
        return {'valid': False, 'error': '未知协议', 'protocol': 'unknown'}

def generate_sensor_data_v1() -> bytes:
    """生成传感器数据 v1 格式"""
    temperature = int(random.uniform(20.0, 35.0) * 10)
    humidity = int(random.uniform(40.0, 80.0) * 10)
    checksum = (temperature + humidity) & 0xFF
    return struct.pack('<HHB', temperature, humidity, checksum)

def generate_command_frame(cmd_id: int, data: bytes) -> bytes:
    """生成命令帧"""
    length = len(data)
    checksum = (cmd_id + length + sum(data)) & 0xFF
    return struct.pack('BB', cmd_id, length) + data + struct.pack('B', checksum)

def main() -> None:
    """主函数 - 完整的串口通信演示"""
    print("=== 单片机串口通信完整解决方案 ===\n")

    # 创建串口模拟器
    uart = UARTSimulator(baud_rate=115200)  # 更高的波特率

    # 注册自定义帧处理器
    uart.register_frame_handler('auto', uart.auto_detect_and_parse)

    print("1. 多协议混合通信测试:")

    # 发送文本消息
    uart.send_data("系统启动中...\n")
    text_frame = uart.receive_frame_with_timeout(delimiter=b'\n')
    if text_frame:
        result = uart.auto_detect_and_parse(text_frame)
        if result['valid']:
            print(f"✓ 文本消息: {result['text']}")

    # 发送传感器数据
    for i in range(3):
        sensor_data = generate_sensor_data_v1()
        uart.send_data(sensor_data)

        sensor_frame = uart.receive_frame_with_timeout(frame_length=5)
        if sensor_frame:
            result = uart.auto_detect_and_parse(sensor_frame)
            if result['valid'] and result['protocol'] == 'sensor_v1':
                print(f"✓ 传感器 #{i+1}: T={result['temperature']:.1f}°C, H={result['humidity']:.1f}%")
            else:
                print(f"✗ 传感器 #{i+1}: {result.get('error', '解析失败')}")

    # 发送复杂命令
    print("\n2. 命令帧测试:")
    config_data = b'\x01\x02\x03\x04'  # 配置参数
    command_frame = generate_command_frame(0x10, config_data)  # 配置命令
    uart.send_data(command_frame)

    cmd_frame = uart.receive_frame_with_timeout(frame_length=len(command_frame))
    if cmd_frame:
        result = uart.auto_detect_and_parse(cmd_frame)
        if result['valid'] and result['protocol'] == 'command':
            print(f"✓ 命令执行: ID=0x{result['command_id']:02X}, 数据长度={len(result['data'])}")
        else:
            print(f"✗ 命令解析: {result.get('error', '失败')}")

    # 错误处理测试
    print("\n3. 错误处理测试:")
    corrupted_frame = generate_sensor_data_v1()[:-1] + b'\xFF'  # 破坏校验和
    uart.send_data(corrupted_frame)

    bad_frame = uart.receive_frame_with_timeout(frame_length=5)
    if bad_frame:
        result = uart.auto_detect_and_parse(bad_frame)
        if not result['valid']:
            print(f"✓ 正确检测到错误: {result['error']}")
            print(f"  总错误计数: {uart.error_count}")

    print("\n4. 实时数据流模拟:")
    print("   模拟持续的数据流接收...")

    # 模拟持续的数据流
    for i in range(5):
        if i % 2 == 0:
            uart.send_data(generate_sensor_data_v1())
        else:
            uart.send_data(f"心跳 #{i//2 + 1}\n".encode())

        # 尝试接收所有可用的帧
        while True:
            frame = None
            # 先尝试固定长度的传感器数据
            if len(uart.buffer) >= 5:
                frame = uart.receive_frame(frame_length=5)
                if frame:
                    result = uart.auto_detect_and_parse(frame)
                    if result['valid']:
                        if result['protocol'] == 'sensor_v1':
                            print(f"   实时传感器: T={result['temperature']:.1f}°C")
                        elif result['protocol'] == 'text':
                            print(f"   实时消息: {result['text'].strip()}")
            else:
                # 尝试文本帧
                frame = uart.receive_frame(delimiter=b'\n')
                if frame:
                    result = uart.auto_detect_and_parse(frame)
                    if result['valid'] and result['protocol'] == 'text':
                        print(f"   实时消息: {result['text'].strip()}")

            if frame is None:
                break

        time.sleep(0.5)

    print(f"\n通信统计:")
    print(f"  总错误数: {uart.error_count}")
    print(f"  缓冲区剩余: {len(uart.buffer)} 字节")

    print("\n完整串口通信解决方案演示完成!")

if __name__ == "__main__":
    main()