"""
Example 02: 模拟传感器 ADC 转换与数值映射

演示如何将ADC原始值转换为实际的物理量，
并进行数值范围映射。
"""

import time
import random
import math

class AnalogSensor:
    def __init__(self, adc_bits=10, reference_voltage=3.3):
        """
        初始化模拟传感器

        Args:
            adc_bits (int): ADC位数，默认10位（0-1023）
            reference_voltage (float): 参考电压，默认3.3V
        """
        self.adc_max = (1 << adc_bits) - 1  # 2^bits - 1
        self.ref_voltage = reference_voltage

    def read_adc_raw(self):
        """
        模拟读取ADC原始值

        Returns:
            int: ADC原始值（0到adc_max）
        """
        # 模拟温度传感器：随时间缓慢变化
        current_time = time.time()
        base_value = 512  # 中间值
        variation = 200 * math.sin(current_time * 0.5)  # 缓慢正弦变化
        noise = random.randint(-10, 10)  # 添加小量噪声

        raw_value = int(base_value + variation + noise)
        # 限制在有效范围内
        return max(0, min(self.adc_max, raw_value))

    def adc_to_voltage(self, adc_value):
        """
        将ADC值转换为电压值

        Args:
            adc_value (int): ADC原始值

        Returns:
            float: 对应的电压值（V）
        """
        return (adc_value / self.adc_max) * self.ref_voltage

    def voltage_to_temperature(self, voltage):
        """
        将电压值转换为温度（简化模型）
        假设使用LM35温度传感器：10mV/°C

        Args:
            voltage (float): 电压值（V）

        Returns:
            float: 温度（°C）
        """
        return voltage * 100  # 1V = 100°C

    def map_value(self, value, from_min, from_max, to_min, to_max):
        """
        数值范围映射函数

        Args:
            value: 输入值
            from_min: 输入范围最小值
            from_max: 输入范围最大值
            to_min: 输出范围最小值
            to_max: 输出范围最大值

        Returns:
            映射后的值
        """
        if from_max == from_min:
            return to_min
        ratio = (value - from_min) / (from_max - from_min)
        return to_min + ratio * (to_max - to_min)

def main():
    """主函数：演示ADC转换和数值映射"""
    sensor = AnalogSensor(adc_bits=10, reference_voltage=3.3)

    print("ADC转换与数值映射演示")
    print("ADC值\t电压(V)\t温度(°C)\t百分比(%)")
    print("-" * 50)

    for i in range(10):
        # 读取原始ADC值
        adc_raw = sensor.read_adc_raw()

        # 转换为电压
        voltage = sensor.adc_to_voltage(adc_raw)

        # 转换为温度
        temperature = sensor.voltage_to_temperature(voltage)

        # 映射到0-100%范围
        percentage = sensor.map_value(adc_raw, 0, 1023, 0, 100)

        print(f"{adc_raw}\t{voltage:.2f}\t{temperature:.1f}\t\t{percentage:.1f}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()