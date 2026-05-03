#!/usr/bin/env python3
"""
I2C 总线地址与寄存器读写模拟 - 完整解决方案

此解决方案包含了完整的 I2C 总线模拟，支持多设备、地址冲突检测和高级寄存器操作。
"""

from typing import Dict, List, Optional, Tuple


class I2CDevice:
    """I2C 从设备模拟器"""

    def __init__(self, address: int, registers: Optional[Dict[int, int]] = None, name: str = "I2C Device"):
        """
        初始化 I2C 设备

        Args:
            address: 7位设备地址 (0-127)
            registers: 寄存器映射 {地址: 值}
            name: 设备名称
        """
        if not 0 <= address <= 127:
            raise ValueError("I2C 地址必须在0-127范围内")

        self.address = address
        self.registers = registers or {}
        self.current_register = 0
        self.name = name

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

    def get_register_dump(self) -> Dict[int, int]:
        """获取所有寄存器的转储"""
        return self.registers.copy()


class I2CBus:
    """I2C 总线模拟器"""

    def __init__(self):
        self.devices: Dict[int, I2CDevice] = {}

    def add_device(self, device: I2CDevice) -> bool:
        """添加设备到总线，返回是否成功（避免地址冲突）"""
        if device.address in self.devices:
            print(f"警告: 地址 0x{device.address:02X} 已被 {self.devices[device.address].name} 占用")
            return False

        self.devices[device.address] = device
        return True

    def remove_device(self, address: int) -> bool:
        """从总线移除设备"""
        if address in self.devices:
            del self.devices[address]
            return True
        return False

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

    def get_device_info(self, address: int) -> Optional[str]:
        """获取设备信息"""
        if address in self.devices:
            device = self.devices[address]
            return f"{device.name} @ 0x{address:02X}"
        return None


def create_typical_devices() -> List[I2CDevice]:
    """创建典型的 I2C 设备"""
    devices = []

    # 温湿度传感器 (SHT30/SHT31)
    temp_sensor = I2CDevice(0x44, {
        0x00: 0x80,  # 状态寄存器
        0x01: 25,    # 温度值 (简化)
        0x02: 60,    # 湿度值 (简化)
    }, "Temperature/Humidity Sensor")

    # EEPROM (24LC256)
    eeprom = I2CDevice(0x50, {}, "EEPROM 24LC256")

    # OLED 显示屏 (SSD1306)
    display = I2CDevice(0x3C, {
        0x00: 0x01,  # 控制寄存器
        0x01: 0x02,  # 显示设置
        0x02: 0x03,  # 对比度
    }, "OLED Display SSD1306")

    # 实时时钟 (DS3231)
    rtc = I2CDevice(0x68, {
        0x00: 0x30,  # 秒
        0x01: 0x45,  # 分
        0x02: 0x12,  # 时
        0x03: 0x03,  # 日
        0x04: 0x05,  # 月
        0x05: 0x26,  # 年
    }, "Real-Time Clock DS3231")

    devices.extend([temp_sensor, eeprom, display, rtc])
    return devices


def simulate_i2c_communication():
    """模拟 I2C 通信过程"""
    print("=== I2C 总线地址与寄存器读写模拟 ===\n")

    # 创建 I2C 总线
    bus = I2CBus()

    # 创建典型设备
    devices = create_typical_devices()

    # 添加设备到总线
    print("添加设备到总线:")
    for device in devices:
        success = bus.add_device(device)
        status = "✓ 成功" if success else "✗ 失败"
        print(f"  {device.name}: {status}")

    print(f"\n总线上有 {len(bus.scan_bus())} 个设备")

    # 扫描总线
    devices_found = bus.scan_bus()
    print(f"\n发现设备: {[f'0x{addr:02X}' for addr in devices_found]}")
    print("设备详情:")
    for addr in devices_found:
        info = bus.get_device_info(addr)
        print(f"  {info}")

    # 模拟温度传感器读取
    print(f"\n--- 读取温度传感器 (0x44) ---")
    temp_data = bus.read_from_device(0x44, 0x01, 2)  # 读取温度和湿度
    if temp_data:
        print(f"温度: {temp_data[0]}°C, 湿度: {temp_data[1]}%")
    else:
        print("读取失败")

    # 模拟 EEPROM 写入和读取
    print(f"\n--- EEPROM 操作 (0x50) ---")
    eeprom_data = [0x10, 0x20, 0x30, 0x40, 0x50, 0x60]
    success = bus.write_to_device(0x50, [0x00] + eeprom_data)  # 写入到地址0x00开始
    print(f"EEPROM 写入 {'成功' if success else '失败'}")

    read_back = bus.read_from_device(0x50, 0x00, len(eeprom_data))
    print(f"EEPROM 读取: {[f'0x{b:02X}' for b in read_back]}")

    # 验证写入正确性
    if read_back == eeprom_data:
        print("✓ EEPROM 数据验证通过")
    else:
        print("✗ EEPROM 数据验证失败")

    # 模拟显示屏配置
    print(f"\n--- 显示屏配置 (0x3C) ---")
    config_success = bus.write_to_device(0x3C, [0x00, 0x0F])  # 设置对比度
    print(f"显示屏配置 {'成功' if config_success else '失败'}")

    display_config = bus.read_from_device(0x3C, 0x00, 3)
    print(f"显示屏配置读取: {[f'0x{b:02X}' for b in display_config]}")

    # 模拟 RTC 时间读取
    print(f"\n--- RTC 时间读取 (0x68) ---")
    rtc_time = bus.read_from_device(0x68, 0x00, 6)
    if rtc_time:
        print(f"RTC 时间: 20{rtc_time[5]:02d}-{rtc_time[4]:02d}-{rtc_time[3]:02d} "
              f"{rtc_time[2]:02d}:{rtc_time[1]:02d}:{rtc_time[0]:02d}")
    else:
        print("RTC 读取失败")


def test_address_conflict():
    """测试地址冲突情况"""
    print("\n=== 地址冲突测试 ===\n")

    bus = I2CBus()

    # 创建两个相同地址的设备
    device1 = I2CDevice(0x48, {}, "Device A")
    device2 = I2CDevice(0x48, {}, "Device B")

    success1 = bus.add_device(device1)
    success2 = bus.add_device(device2)

    print(f"添加 Device A: {'成功' if success1 else '失败'}")
    print(f"添加 Device B: {'成功' if success2 else '失败'}")
    print(f"总线上设备数量: {len(bus.scan_bus())}")


if __name__ == "__main__":
    simulate_i2c_communication()
    test_address_conflict()