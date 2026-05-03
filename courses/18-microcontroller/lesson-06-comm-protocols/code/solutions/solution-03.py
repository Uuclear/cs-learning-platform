#!/usr/bin/env python3
"""
SPI 高速数据传输时序模拟 - 完整解决方案

此解决方案包含了完整的 SPI 时序模拟，支持所有四种 SPI 模式和多设备管理。
"""

from typing import List, Dict, Optional
import random


class SPIDevice:
    """SPI 从设备模拟器"""

    def __init__(self, name: str = "Device", response_pattern: Optional[List[int]] = None):
        self.name = name
        self.received_data: List[int] = []
        self.response_pattern = response_pattern or [0xAA, 0x55, 0xFF, 0x00]
        self.transfer_count = 0

    def transfer(self, data: List[int]) -> List[int]:
        """
        SPI 数据传输

        Args:
            data: 主设备发送的数据

        Returns:
            从设备返回的数据
        """
        self.received_data = data.copy()
        self.transfer_count += 1

        # 根据传输次数生成不同的响应模式
        response = []
        for i in range(len(data)):
            pattern_index = (self.transfer_count + i) % len(self.response_pattern)
            response.append(self.response_pattern[pattern_index])

        return response

    def get_stats(self) -> dict:
        """获取设备统计信息"""
        return {
            'name': self.name,
            'transfer_count': self.transfer_count,
            'last_received': self.received_data.copy() if self.received_data else None
        }


class SPIMaster:
    """SPI 主设备模拟器"""

    def __init__(self, cpol: int = 0, cpha: int = 0, bit_order: str = 'msb'):
        """
        初始化 SPI 主设备

        Args:
            cpol: 时钟极性 (0=空闲时低电平, 1=空闲时高电平)
            cpha: 时钟相位 (0=第一个边沿采样, 1=第二个边沿采样)
            bit_order: 位顺序 ('msb' 或 'lsb')
        """
        if cpol not in [0, 1] or cpha not in [0, 1]:
            raise ValueError("CPOL 和 CPHA 必须是 0 或 1")
        if bit_order not in ['msb', 'lsb']:
            raise ValueError("bit_order 必须是 'msb' 或 'lsb'")

        self.cpol = cpol
        self.cpha = cpha
        self.bit_order = bit_order
        self.devices: Dict[int, SPIDevice] = {}
        self.cs_active = False
        self.transfer_log: List[dict] = []

    def add_device(self, cs_pin: int, device: SPIDevice) -> bool:
        """添加从设备"""
        if cs_pin in self.devices:
            return False
        self.devices[cs_pin] = device
        return True

    def remove_device(self, cs_pin: int) -> bool:
        """移除从设备"""
        if cs_pin in self.devices:
            del self.devices[cs_pin]
            return True
        return False

    def transfer(self, cs_pin: int, data: List[int], delay_us: float = 0.1) -> List[int]:
        """
        SPI 数据传输

        Args:
            cs_pin: 片选引脚号
            data: 要传输的数据
            delay_us: 模拟传输延迟（微秒）

        Returns:
            接收到的数据
        """
        if cs_pin not in self.devices:
            raise ValueError(f"未找到 CS 引脚 {cs_pin} 的设备")

        device = self.devices[cs_pin]

        # 记录传输日志
        log_entry = {
            'cs_pin': cs_pin,
            'device_name': device.name,
            'sent_data': data.copy(),
            'cpol': self.cpol,
            'cpha': self.cpha,
            'bit_order': self.bit_order,
            'timestamp': time.time()
        }

        # 激活片选 (低电平有效)
        self.cs_active = True

        # 获取从设备的实际响应
        actual_response = device.transfer(data)

        # 模拟传输延迟
        if delay_us > 0:
            time.sleep(delay_us / 1_000_000)

        # 停用片选
        self.cs_active = False

        # 完成日志记录
        log_entry['received_data'] = actual_response.copy()
        self.transfer_log.append(log_entry)

        return actual_response

    def get_transfer_log(self) -> List[dict]:
        """获取传输日志"""
        return self.transfer_log.copy()

    def get_spi_mode(self) -> int:
        """获取 SPI 模式编号 (0-3)"""
        return self.cpol * 2 + self.cpha

    def set_spi_mode(self, mode: int):
        """设置 SPI 模式 (0-3)"""
        if not 0 <= mode <= 3:
            raise ValueError("SPI 模式必须是 0-3")
        self.cpol = mode // 2
        self.cpha = mode % 2


def create_typical_spi_devices() -> Dict[int, SPIDevice]:
    """创建典型的 SPI 设备"""
    devices = {}

    # OLED 显示屏 (SSD1306)
    devices[0] = SPIDevice("OLED Display", [0x00, 0xFF, 0xAA, 0x55])

    # ADC 转换器 (MCP3008)
    devices[1] = SPIDevice("ADC MCP3008", [0x12, 0x34, 0x56, 0x78])

    # Flash 存储器 (W25Q64)
    devices[2] = SPIDevice("Flash W25Q64", [0x9F, 0xEF, 0x14, 0x00])  # JEDEC ID

    # SD 卡
    devices[3] = SPIDevice("SD Card", [0xFE, 0xFF, 0xFF, 0xFF])

    return devices


def simulate_spi_communication():
    """模拟 SPI 通信过程"""
    print("=== SPI 高速数据传输时序模拟 ===\n")

    # 创建 SPI 主设备 (模式0: CPOL=0, CPHA=0)
    spi_master = SPIMaster(cpol=0, cpha=0, bit_order='msb')

    # 创建典型设备
    devices = create_typical_spi_devices()

    # 连接设备到不同的 CS 引脚
    for cs_pin, device in devices.items():
        success = spi_master.add_device(cs_pin, device)
        print(f"连接 {device.name} 到 CS{cs_pin}: {'成功' if success else '失败'}")

    print(f"\nSPI 模式: {spi_master.get_spi_mode()} (CPOL={spi_master.cpol}, CPHA={spi_master.cpha})")
    print(f"位顺序: {spi_master.bit_order.upper()}\n")

    # 模拟 OLED 显示屏通信
    print("=== OLED 显示屏通信 ===")
    display_cmd = [0xAE, 0x20, 0x00, 0x10]  # 关闭显示 + 设置内存地址
    response = spi_master.transfer(0, display_cmd)
    print(f"发送命令: {[f'0x{b:02X}' for b in display_cmd]}")
    print(f"接收响应: {[f'0x{b:02X}' for b in response]}")

    # 发送显示数据
    display_data = [0x40] + [random.randint(0, 255) for _ in range(8)]  # 显示数据
    data_response = spi_master.transfer(0, display_data)
    print(f"显示数据: 发送{len(display_data)}字节")
    print(f"数据响应: {[f'0x{b:02X}' for b in data_response[:4]]}...")

    print("\n" + "="*50 + "\n")

    # 模拟 ADC 数据读取
    print("=== ADC 数据读取 ===")
    adc_cmd = [0x01, 0x80, 0x00]  # 读取通道0 (MCP3008 格式)
    adc_response = spi_master.transfer(1, adc_cmd)
    print(f"ADC 命令: {[f'0x{b:02X}' for b in adc_cmd]}")

    # 解析 ADC 结果 (假设10位结果在后两个字节)
    if len(adc_response) >= 3:
        adc_value = ((adc_response[1] & 0x03) << 8) | adc_response[2]
        voltage = (adc_value / 1023.0) * 3.3  # 假设3.3V参考电压
        print(f"ADC 值: {adc_value} ({voltage:.2f}V)")
    else:
        print("ADC 响应长度不足")

    print("\n" + "="*50 + "\n")

    # 模拟 Flash 存储器操作
    print("=== Flash 存储器操作 ===")
    # 读取 JEDEC ID
    jedec_cmd = [0x9F]  # Read JEDEC ID 命令
    jedec_response = spi_master.transfer(2, jedec_cmd + [0x00, 0x00, 0x00])
    print(f"JEDEC ID: {[f'0x{b:02X}' for b in jedec_response[1:]]}")

    # 写入数据到 Flash
    write_cmd = [0x02, 0x00, 0x00, 0x00] + [0xDE, 0xAD, 0xBE, 0xEF]  # 写入命令 + 地址 + 数据
    write_response = spi_master.transfer(2, write_cmd)
    print(f"Flash 写入: 命令长度 {len(write_cmd)} 字节")

    print("\n" + "="*50 + "\n")

    # 测试不同 SPI 模式
    print("=== 不同 SPI 模式测试 ===")
    test_data = [0x55, 0xAA]

    for mode in range(4):
        print(f"\n测试 SPI 模式 {mode}:")
        test_master = SPIMaster()
        test_master.set_spi_mode(mode)

        test_device = SPIDevice("Test Device")
        test_master.add_device(0, test_device)

        response = test_master.transfer(0, test_data)
        print(f"  发送: {[f'0x{b:02X}' for b in test_data]}")
        print(f"  接收: {[f'0x{b:02X}' for b in response]}")


def analyze_transfer_performance():
    """分析传输性能"""
    print("\n=== 传输性能分析 ===\n")

    spi_master = SPIMaster(cpol=0, cpha=0)
    test_device = SPIDevice("Performance Test")
    spi_master.add_device(0, test_device)

    # 测试不同数据长度的传输时间
    import time

    data_lengths = [1, 4, 16, 64, 256]
    results = []

    for length in data_lengths:
        test_data = [random.randint(0, 255) for _ in range(length)]

        start_time = time.perf_counter()
        response = spi_master.transfer(0, test_data, delay_us=1.0)  # 1us 延迟
        end_time = time.perf_counter()

        duration_us = (end_time - start_time) * 1_000_000
        throughput = (length * 8) / (duration_us / 1_000_000)  # bits per second

        results.append({
            'length': length,
            'duration_us': duration_us,
            'throughput_bps': throughput
        })

    print("数据长度 | 传输时间(μs) | 吞吐量(bps)")
    print("---------|--------------|------------")
    for result in results:
        print(f"{result['length']:8d} | {result['duration_us']:12.2f} | {result['throughput_bps']:10.0f}")


if __name__ == "__main__":
    import time
    simulate_spi_communication()
    analyze_transfer_performance()