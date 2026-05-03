"""
Example 03: DHT11 温湿度传感器数据解析模拟

DHT11传感器通过单总线协议传输40位数据：
- 8位湿度整数
- 8位湿度小数（DHT11总是0）
- 8位温度整数
- 8位温度小数（DHT11总是0）
- 8位校验和

本示例模拟DHT11的数据传输和解析过程。
"""

import time
import random

class DHT11Simulator:
    def __init__(self):
        """初始化DHT11模拟器"""
        pass

    def simulate_dht11_data(self):
        """
        模拟生成DHT11的40位数据流

        Returns:
            list: 40个布尔值，表示数据位（True=1, False=0）
        """
        # 模拟真实的温湿度值
        humidity = random.randint(30, 70)  # 30-70% 湿度
        temperature = random.randint(20, 30)  # 20-30°C 温度

        # DHT11的小数部分总是0
        humidity_frac = 0
        temperature_frac = 0

        # 计算校验和
        checksum = (humidity + humidity_frac + temperature + temperature_frac) & 0xFF

        # 构建40位数据：湿度(8) + 湿度小数(8) + 温度(8) + 温度小数(8) + 校验和(8)
        data_bytes = [humidity, humidity_frac, temperature, temperature_frac, checksum]

        # 转换为位流
        bit_stream = []
        for byte in data_bytes:
            for i in range(7, -1, -1):  # 从最高位到最低位
                bit_stream.append(bool((byte >> i) & 1))

        return bit_stream

    def parse_dht11_data(self, bit_stream):
        """
        解析DHT11的40位数据流

        Args:
            bit_stream (list): 40个布尔值的数据流

        Returns:
            tuple: (humidity, temperature, is_valid) 或 (None, None, False)
        """
        if len(bit_stream) != 40:
            print(f"错误：数据长度应为40位，实际为{len(bit_stream)}位")
            return None, None, False

        # 将位流转换为字节
        data_bytes = []
        for i in range(0, 40, 8):
            byte = 0
            for j in range(8):
                if bit_stream[i + j]:
                    byte |= (1 << (7 - j))
            data_bytes.append(byte)

        humidity, humidity_frac, temperature, temperature_frac, checksum = data_bytes

        # 验证校验和
        calculated_checksum = (humidity + humidity_frac + temperature + temperature_frac) & 0xFF
        is_valid = (checksum == calculated_checksum)

        if not is_valid:
            print(f"校验和错误：期望{calculated_checksum}，实际{checksum}")
            return None, None, False

        # DHT11的小数部分忽略
        return humidity, temperature, True

    def read_sensor(self):
        """
        模拟完整的传感器读取过程

        Returns:
            tuple: (humidity, temperature) 或 (None, None) 如果读取失败
        """
        print("正在读取DHT11传感器...")

        # 模拟传感器响应时间
        time.sleep(0.1)

        # 生成模拟数据
        bit_stream = self.simulate_dht11_data()

        # 解析数据
        humidity, temperature, is_valid = self.parse_dht11_data(bit_stream)

        if is_valid:
            print(f"读取成功！湿度: {humidity}%, 温度: {temperature}°C")
            return humidity, temperature
        else:
            print("读取失败！")
            return None, None

def main():
    """主函数：演示DHT11数据读取和解析"""
    dht11 = DHT11Simulator()

    print("DHT11温湿度传感器数据解析演示")
    print("=" * 40)

    # 连续读取5次
    for i in range(5):
        print(f"\n第{i+1}次读取:")
        humidity, temperature = dht11.read_sensor()

        if humidity is not None and temperature is not None:
            # 判断环境舒适度
            if 40 <= humidity <= 60 and 22 <= temperature <= 26:
                comfort = "舒适"
            elif humidity < 30 or humidity > 70:
                comfort = "干燥/潮湿"
            elif temperature < 20 or temperature > 30:
                comfort = "过冷/过热"
            else:
                comfort = "一般"

            print(f"环境状态: {comfort}")
        else:
            print("无法获取环境状态")

        time.sleep(1)

if __name__ == "__main__":
    main()