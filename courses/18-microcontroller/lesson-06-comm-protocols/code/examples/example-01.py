#!/usr/bin/env python3
"""
UART 串口数据帧解析模拟器

模拟 UART 通信的数据帧结构，包括起始位、数据位、校验位和停止位。
支持不同的数据位长度（5-9位）和校验方式。
"""

import random
from typing import List, Optional


class UARTFrame:
    """UART 数据帧模拟器"""

    def __init__(self, data_bits: int = 8, parity: Optional[str] = None, stop_bits: int = 1):
        """
        初始化 UART 帧参数

        Args:
            data_bits: 数据位数 (5-9)
            parity: 校验方式 ("even", "odd", None)
            stop_bits: 停止位数 (1 or 2)
        """
        if not 5 <= data_bits <= 9:
            raise ValueError("数据位必须在5-9之间")
        if stop_bits not in [1, 2]:
            raise ValueError("停止位必须是1或2")
        if parity not in [None, "even", "odd"]:
            raise ValueError("校验方式必须是 None, 'even', 或 'odd'")

        self.data_bits = data_bits
        self.parity = parity
        self.stop_bits = stop_bits

    def create_frame(self, data: int) -> List[int]:
        """
        创建 UART 数据帧

        Args:
            data: 要传输的数据 (0-255)

        Returns:
            完整的帧位列表 [起始位, 数据位..., 校验位, 停止位...]
        """
        # 起始位 (0)
        frame = [0]

        # 数据位 (LSB first)
        for i in range(self.data_bits):
            frame.append((data >> i) & 1)

        # 校验位
        if self.parity:
            parity_bit = self._calculate_parity(frame[1:1+self.data_bits])
            frame.append(parity_bit)

        # 停止位 (1)
        frame.extend([1] * self.stop_bits)

        return frame

    def _calculate_parity(self, data_bits: List[int]) -> int:
        """计算校验位"""
        ones_count = sum(data_bits)
        if self.parity == "even":
            return ones_count % 2
        else:  # odd
            return 1 - (ones_count % 2)

    def parse_frame(self, frame: List[int]) -> dict:
        """
        解析 UART 帧

        Args:
            frame: 接收到的帧位列表

        Returns:
            解析结果字典
        """
        result = {
            'valid': True,
            'start_bit': frame[0],
            'data': 0,
            'parity_check': True,
            'stop_bits_valid': True,
            'error': ''
        }

        # 检查起始位
        if frame[0] != 0:
            result['valid'] = False
            result['error'] = '起始位错误'
            return result

        # 提取数据位
        data_bits = frame[1:1+self.data_bits]
        for i, bit in enumerate(data_bits):
            result['data'] |= (bit << i)

        # 检查校验位
        current_index = 1 + self.data_bits
        if self.parity:
            if current_index >= len(frame):
                result['valid'] = False
                result['error'] = '帧长度不足'
                return result

            received_parity = frame[current_index]
            calculated_parity = self._calculate_parity(data_bits)
            if received_parity != calculated_parity:
                result['parity_check'] = False
                result['valid'] = False
                result['error'] = '校验错误'
            current_index += 1

        # 检查停止位
        expected_stop_bits = frame[current_index:current_index + self.stop_bits]
        if len(expected_stop_bits) != self.stop_bits or any(bit != 1 for bit in expected_stop_bits):
            result['stop_bits_valid'] = False
            result['valid'] = False
            if result['error'] == '':
                result['error'] = '停止位错误'

        return result


def simulate_uart_communication():
    """模拟 UART 通信过程"""
    print("=== UART 串口数据帧解析模拟器 ===\n")

    # 创建不同配置的 UART 帧
    configs = [
        (8, None, 1),    # 8N1 (最常用)
        (8, "even", 1),  # 8E1
        (7, "odd", 2),   # 7O2
    ]

    for data_bits, parity, stop_bits in configs:
        print(f"测试配置: {data_bits}数据位, {parity or '无'}校验, {stop_bits}停止位")

        uart = UARTFrame(data_bits, parity, stop_bits)
        test_data = random.randint(0, 255)

        # 创建帧
        frame = uart.create_frame(test_data)
        print(f"原始数据: {test_data:03d} (0x{test_data:02X})")
        print(f"数据帧:   {''.join(map(str, frame))}")

        # 解析帧
        result = uart.parse_frame(frame)
        print(f"解析结果: {'有效' if result['valid'] else '无效'}")
        if not result['valid']:
            print(f"错误信息: {result['error']}")
        print(f"恢复数据: {result['data']:03d} (0x{result['data']:02X})")
        print("-" * 50)


if __name__ == "__main__":
    simulate_uart_communication()