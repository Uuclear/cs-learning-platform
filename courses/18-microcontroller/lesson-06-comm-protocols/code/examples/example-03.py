#!/usr/bin/env python3
"""
SPI 高速数据传输时序模拟

模拟 SPI 总线的四线通信过程，包括时钟、数据输入输出和片选信号。
支持不同的时钟极性(CPOL)和相位(CPHA)配置。
"""

from typing import List, Tuple
import time


class SPIDevice:
    """SPI 从设备模拟器"""

    def __init__(self, name: str = "Device"):
        self.name = name
        self.received_data: List[int] = []
        self.response_data: List[int] = [0xAA, 0x55, 0xFF, 0x00]  # 模拟响应数据

    def transfer(self, data: List[int]) -> List[int]:
        """
        SPI 数据传输

        Args:
            data: 主设备发送的数据

        Returns:
            从设备返回的数据
        """
        self.received_data = data.copy()

        # 模拟从设备的响应（循环使用预定义的响应数据）
        response = []
        for i in range(len(data)):
            response.append(self.response_data[i % len(self.response_data)])

        return response


class SPIMaster:
    """SPI 主设备模拟器"""

    def __init__(self, cpol: int = 0, cpha: int = 0):
        """
        初始化 SPI 主设备

        Args:
            cpol: 时钟极性 (0=空闲时低电平, 1=空闲时高电平)
            cpha: 时钟相位 (0=第一个边沿采样, 1=第二个边沿采样)
        """
        if cpol not in [0, 1] or cpha not in [0, 1]:
            raise ValueError("CPOL 和 CPHA 必须是 0 或 1")

        self.cpol = cpol
        self.cpha = cpha
        self.devices: Dict[int, SPIDevice] = {}
        self.cs_active = False

    def add_device(self, cs_pin: int, device: SPIDevice):
        """添加从设备"""
        self.devices[cs_pin] = device

    def transfer(self, cs_pin: int, data: List[int]) -> List[int]:
        """
        SPI 数据传输

        Args:
            cs_pin: 片选引脚号
            data: 要传输的数据

        Returns:
            接收到的数据
        """
        if cs_pin not in self.devices:
            raise ValueError(f"未找到 CS 引脚 {cs_pin} 的设备")

        device = self.devices[cs_pin]

        # 激活片选 (低电平有效)
        self.cs_active = True
        print(f"CS{cs_pin} 激活 (低电平)")

        # 模拟时钟和数据传输
        received = self._simulate_transfer(data)

        # 停用片选
        self.cs_active = False
        print(f"CS{cs_pin} 停用 (高电平)")

        # 获取从设备的实际响应
        actual_response = device.transfer(data)

        return actual_response

    def _simulate_transfer(self, data: List[int]) -> List[int]:
        """模拟 SPI 时序传输"""
        print(f"\n--- SPI 传输模拟 (CPOL={self.cpol}, CPHA={self.cpha}) ---")
        print("时钟 | MOSI | MISO")
        print("-----|------|------")

        # 模拟每个字节的传输
        for byte in data:
            self._simulate_byte_transfer(byte)
            print()  # 空行分隔字节

        # 返回模拟接收数据
        return [0] * len(data)

    def _simulate_byte_transfer(self, byte: int):
        """模拟单个字节的传输时序"""
        # 根据 CPOL 设置初始时钟状态
        clock = self.cpol

        # 发送8位数据
        for bit_pos in range(8):
            # 根据 CPHA 决定何时改变数据
            if self.cpha == 0:
                # 第一个边沿设置数据，第二个边沿采样
                mosi_bit = (byte >> (7 - bit_pos)) & 1

                # 时钟跳变到采样边沿
                clock = 1 - self.cpol  # 采样边沿
                miso_bit = random.choice([0, 1])  # 模拟 MISO

                print(f" {clock}   |  {mosi_bit}   |  {miso_bit}")

                # 时钟回到空闲状态
                clock = self.cpol

            else:
                # 第二个边沿设置数据，第一个边沿采样
                # 先保持时钟在采样边沿
                clock = 1 - self.cpol
                miso_bit = random.choice([0, 1])  # 模拟 MISO

                # 然后改变数据并回到空闲状态
                mosi_bit = (byte >> (7 - bit_pos)) & 1
                clock = self.cpol

                print(f" {1-self.cpol}   |  ?   |  {miso_bit}")  # 采样时刻
                print(f" {clock}   |  {mosi_bit}   |  ?")           # 设置数据时刻


def simulate_spi_communication():
    """模拟 SPI 通信过程"""
    print("=== SPI 高速数据传输时序模拟 ===\n")

    # 创建 SPI 主设备 (模式0: CPOL=0, CPHA=0)
    spi_master = SPIMaster(cpol=0, cpha=0)

    # 创建从设备
    display = SPIDevice("OLED Display")
    adc = SPIDevice("ADC Converter")
    flash = SPIDevice("Flash Memory")

    # 连接设备到不同的 CS 引脚
    spi_master.add_device(0, display)
    spi_master.add_device(1, adc)
    spi_master.add_device(2, flash)

    # 模拟 OLED 显示屏通信
    print("=== OLED 显示屏通信 ===")
    display_cmd = [0xAE, 0x20, 0x00, 0x10]  # 关闭显示 + 设置内存地址
    response = spi_master.transfer(0, display_cmd)
    print(f"发送命令: {[f'0x{b:02X}' for b in display_cmd]}")
    print(f"接收响应: {[f'0x{b:02X}' for b in response]}")

    print("\n" + "="*50 + "\n")

    # 模拟 ADC 数据读取
    print("=== ADC 数据读取 ===")
    adc_cmd = [0x01, 0x80]  # 读取通道0
    adc_response = spi_master.transfer(1, adc_cmd)
    print(f"ADC 命令: {[f'0x{b:02X}' for b in adc_cmd]}")
    print(f"ADC 数据: {[f'0x{b:02X}' for b in adc_response[:2]]}")

    print("\n" + "="*50 + "\n")

    # 模拟不同 SPI 模式
    print("=== 不同 SPI 模式对比 ===")
    modes = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for cpol, cpha in modes:
        print(f"\nSPI 模式 {cpol*2 + cpha} (CPOL={cpol}, CPHA={cpha}):")
        test_master = SPIMaster(cpol, cpha)
        test_device = SPIDevice("Test")
        test_master.add_device(0, test_device)

        # 只显示时序，不实际传输
        test_master._simulate_transfer([0x55])


if __name__ == "__main__":
    import random
    simulate_spi_communication()