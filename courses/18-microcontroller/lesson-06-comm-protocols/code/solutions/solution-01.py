#!/usr/bin/env python3
"""
UART 串口数据帧解析模拟器 - 完整解决方案

此解决方案包含了错误处理、多种配置支持和完整的帧验证功能。
"""

import random
from typing import List, Optional, Tuple


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

        # 检查帧长度是否足够
        min_length = 1 + self.data_bits + (1 if self.parity else 0) + self.stop_bits
        if len(frame) < min_length:
            result['valid'] = False
            result['error'] = f'帧长度不足，期望至少{min_length}位，实际{len(frame)}位'
            return result

        # 提取数据位
        data_bits = frame[1:1+self.data_bits]
        for i, bit in enumerate(data_bits):
            result['data'] |= (bit << i)

        # 检查校验位
        current_index = 1 + self.data_bits
        if self.parity:
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

    def frame_to_string(self, frame: List[int]) -> str:
        """将帧转换为可读字符串"""
        parts = []
        parts.append(f"S({frame[0]})")  # 起始位

        data_str = ''.join(str(b) for b in frame[1:1+self.data_bits])
        parts.append(f"D({data_str})")  # 数据位

        if self.parity:
            parity_index = 1 + self.data_bits
            parts.append(f"P({frame[parity_index]})")  # 校验位

        stop_start = 1 + self.data_bits + (1 if self.parity else 0)
        stop_str = ''.join(str(b) for b in frame[stop_start:stop_start+self.stop_bits])
        parts.append(f"T({stop_str})")  # 停止位

        return ' '.join(parts)


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
        print(f"数据帧:   {uart.frame_to_string(frame)}")

        # 解析帧
        result = uart.parse_frame(frame)
        print(f"解析结果: {'有效' if result['valid'] else '无效'}")
        if not result['valid']:
            print(f"错误信息: {result['error']}")
        print(f"恢复数据: {result['data']:03d} (0x{result['data']:02X})")
        print("-" * 50)


def test_error_conditions():
    """测试各种错误条件"""
    print("\n=== 错误条件测试 ===\n")

    uart = UARTFrame(8, None, 1)

    # 测试起始位错误
    bad_frame1 = [1, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 起始位为1
    result1 = uart.parse_frame(bad_frame1)
    print(f"起始位错误测试: {result1['error']}")

    # 测试停止位错误
    bad_frame2 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]  # 停止位为0
    result2 = uart.parse_frame(bad_frame2)
    print(f"停止位错误测试: {result2['error']}")

    # 测试帧长度不足
    bad_frame3 = [0, 1, 0, 1, 0, 1]  # 只有6位
    result3 = uart.parse_frame(bad_frame3)
    print(f"帧长度不足测试: {result3['error']}")


if __name__ == "__main__":
    simulate_uart_communication()
    test_error_conditions()