#!/usr/bin/env python3
"""
I2C 总线地址与寄存器读写模拟

模拟 I2C 总线的主从通信过程，包括地址识别、寄存器访问和数据传输。
"""

from typing import Dict, List, Optional


class I2CDevice:
    """I2C 从设备模拟器"""

    def __init__(self, address: int, registers: Optional[Dict[int, int]] = None):
        """
        初始化 I2C 设备

        Args:
            address: 7位设备地址 (0-127)
            registers: 寄存器映射 {地址: 值}
        """
        if not 0 <= address <= 127:
            raise ValueError("I2C 地址必须在0-127范围内")

        self.address = address
        self.registers = registers or {}
        self.current_register = 0

    def write_register(self, reg_addr: int, value: int):
        """写入寄存器"""
        self.registers[reg_addr] = value & 0xFF

    def read_register(self, reg_addr: int) -> int:
        """读取寄存器"""
        return self.registers.get(reg_addr, 0)

    def handle_i2c_transaction(self, data: List[int]) -> List[int]:
        """
        处理 I2C 事务

        Args:
            data: 接收到的数据列表 [寄存器地址, 数据...]

        Returns:
            响应数据列表
        """
        if not data:
            return []

        # 第一个字节是寄存器地址
        self.current_register = data[0]

        # 如果有更多数据，说明是写操作
        if len(data) > 1:
            for i, value in enumerate(data[1:], 1):
                self.write_register(self.current_register + i - 1, value)
            return []  # 写操作无返回

        # 读操作，返回当前寄存器的值
        return [self.read_register(self.current_register)]


class I2CBus:
    """I2C 总线模拟器"""

    def __init__(self):
        self.devices: Dict[int, I2CDevice] = {}

    def add_device(self, device: I2CDevice):
        """添加设备到总线"""
        self.devices[device.address] = device

    def scan_bus(self) -> List[int]:
        """扫描总线上的设备"""
        return sorted(self.devices.keys())

    def write_to_device(self, address: int, data: List[int]) -> bool:
        """
        向设备写入数据

        Args:
            address: 设备地址
            data: 要写入的数据

        Returns:
            是否成功
        """
        if address not in self.devices:
            return False

        self.devices[address].handle_i2c_transaction(data)
        return True

    def read_from_device(self, address: int, register: int, length: int = 1) -> List[int]:
        """
        从设备读取数据

        Args:
            address: 设备地址
            register: 起始寄存器地址
            length: 读取字节数

        Returns:
            读取的数据列表
        """
        if address not in self.devices:
            return []

        device = self.devices[address]
        result = []
        for i in range(length):
            result.append(device.read_register(register + i))
        return result


def simulate_i2c_communication():
    """模拟 I2C 通信过程"""
    print("=== I2C 总线地址与寄存器读写模拟 ===\n")

    # 创建 I2C 总线
    bus = I2CBus()

    # 创建几个模拟设备
    temp_sensor = I2CDevice(0x48, {0x00: 25, 0x01: 0x80})  # 温度传感器
    eeprom = I2CDevice(0x50, {})                           # EEPROM
    display = I2CDevice(0x3C, {0x00: 0x01, 0x01: 0x02})   # OLED 显示屏

    # 添加设备到总线
    bus.add_device(temp_sensor)
    bus.add_device(eeprom)
    bus.add_device(display)

    # 扫描总线
    devices = bus.scan_bus()
    print(f"发现 {len(devices)} 个设备: {[f'0x{addr:02X}' for addr in devices]}")

    # 模拟温度传感器读取
    print(f"\n--- 读取温度传感器 (0x48) ---")
    temp_data = bus.read_from_device(0x48, 0x00, 1)
    print(f"温度寄存器值: {temp_data[0] if temp_data else 'N/A'}°C")

    # 模拟 EEPROM 写入和读取
    print(f"\n--- EEPROM 操作 (0x50) ---")
    eeprom_data = [0x10, 0x20, 0x30, 0x40]
    success = bus.write_to_device(0x50, [0x00] + eeprom_data)  # 写入到地址0x00开始
    print(f"EEPROM 写入 {'成功' if success else '失败'}")

    read_back = bus.read_from_device(0x50, 0x00, 4)
    print(f"EEPROM 读取: {[f'0x{b:02X}' for b in read_back]}")

    # 模拟显示屏配置
    print(f"\n--- 显示屏配置 (0x3C) ---")
    config_success = bus.write_to_device(0x3C, [0x00, 0x0F])  # 设置对比度
    print(f"显示屏配置 {'成功' if config_success else '失败'}")

    display_config = bus.read_from_device(0x3C, 0x00, 2)
    print(f"显示屏配置读取: {[f'0x{b:02X}' for b in display_config]}")


if __name__ == "__main__":
    simulate_i2c_communication()