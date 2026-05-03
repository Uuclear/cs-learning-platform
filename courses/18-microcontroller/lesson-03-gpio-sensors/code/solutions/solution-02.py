"""
Solution 02: 完整的模拟传感器数据处理系统

这是一个完整的模拟传感器处理系统，
支持多种传感器类型和自动校准功能。
"""

import time
import math
from typing import Optional, Tuple, Callable

class SensorProcessor:
    def __init__(self, adc_bits: int = 10, reference_voltage: float = 3.3):
        """
        初始化传感器处理器

        Args:
            adc_bits: ADC位数
            reference_voltage: 参考电压
        """
        self.adc_max = (1 << adc_bits) - 1
        self.ref_voltage = reference_voltage
        self.calibration_offset = 0.0
        self.calibration_scale = 1.0

    def set_calibration(self, offset: float, scale: float):
        """设置校准参数"""
        self.calibration_offset = offset
        self.calibration_scale = scale

    def read_adc(self, pin: int) -> int:
        """
        读取ADC值（实际应用中替换为硬件读取）

        Args:
            pin: ADC引脚号

        Returns:
            ADC原始值
        """
        # 模拟不同传感器的读数模式
        current_time = time.time()

        if pin == 0:  # 温度传感器
            base = 512
            variation = 200 * math.sin(current_time * 0.3)
        elif pin == 1:  # 光照传感器
            base = 768
            variation = 256 * math.sin(current_time * 0.2)
        else:  # 默认
            base = 512
            variation = 100 * math.sin(current_time * 0.1)

        noise = (random.random() - 0.5) * 20  # ±10的噪声
        value = int(base + variation + noise)
        return max(0, min(self.adc_max, value))

    def adc_to_voltage(self, adc_value: int) -> float:
        """ADC值转电压"""
        return (adc_value / self.adc_max) * self.ref_voltage

    def voltage_to_physical(self, voltage: float, sensor_type: str) -> float:
        """
        电压值转物理量

        Args:
            voltage: 电压值
            sensor_type: 传感器类型

        Returns:
            物理量值
        """
        if sensor_type == "temperature":
            # LM35: 10mV/°C
            return voltage * 100
        elif sensor_type == "light":
            # 光敏电阻：简化模型
            # 0V = 0% 光照, 3.3V = 100% 光照
            return (voltage / self.ref_voltage) * 100
        elif sensor_type == "potentiometer":
            # 电位器：0-100%
            return (voltage / self.ref_voltage) * 100
        else:
            return voltage

    def process_sensor(self, pin: int, sensor_type: str) -> float:
        """
        处理传感器数据

        Args:
            pin: ADC引脚
            sensor_type: 传感器类型

        Returns:
            校准后的物理量值
        """
        adc_value = self.read_adc(pin)
        voltage = self.adc_to_voltage(adc_value)
        physical_value = self.voltage_to_physical(voltage, sensor_type)

        # 应用校准
        calibrated_value = (physical_value - self.calibration_offset) * self.calibration_scale

        return calibrated_value

    def auto_calibrate(self, pin: int, sensor_type: str, known_value: float):
        """
        自动校准传感器

        Args:
            pin: ADC引脚
            sensor_type: 传感器类型
            known_value: 已知的标准值
        """
        measured_value = self.process_sensor(pin, sensor_type)
        if measured_value != 0:
            self.calibration_scale = known_value / measured_value
        else:
            self.calibration_offset = known_value - measured_value

class MultiSensorSystem:
    def __init__(self):
        """初始化多传感器系统"""
        self.processor = SensorProcessor()
        self.sensors = {
            "temperature": {"pin": 0, "type": "temperature", "unit": "°C"},
            "light": {"pin": 1, "type": "light", "unit": "%"},
            "potentiometer": {"pin": 2, "type": "potentiometer", "unit": "%"}
        }

    def read_all_sensors(self) -> dict:
        """读取所有传感器数据"""
        results = {}
        for name, config in self.sensors.items():
            value = self.processor.process_sensor(config["pin"], config["type"])
            results[name] = {
                "value": round(value, 1),
                "unit": config["unit"]
            }
        return results

    def display_sensors(self):
        """显示所有传感器数据"""
        data = self.read_all_sensors()
        print(f"{'='*40}")
        print(f"传感器数据 - {time.strftime('%H:%M:%S')}")
        print(f"{'='*40}")
        for name, info in data.items():
            print(f"{name.capitalize():12}: {info['value']:6.1f} {info['unit']}")
        print()

def main():
    """主函数：演示完整的多传感器系统"""
    system = MultiSensorSystem()

    # 演示校准功能
    print("校准温度传感器...")
    system.processor.auto_calibrate(0, "temperature", 25.0)  # 假设标准温度25°C

    print("多传感器系统演示")
    print("按 Ctrl+C 退出")

    try:
        while True:
            system.display_sensors()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序结束")

if __name__ == "__main__":
    main()