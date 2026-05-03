"""
Solution 03: 完整的DHT11传感器驱动和错误处理

这是一个完整的DHT11传感器实现，
包含超时检测、重试机制和数据验证。
"""

import time
import random
from typing import Optional, Tuple

class DHT11Driver:
    def __init__(self, max_retries: int = 3, timeout_ms: int = 100):
        """
        初始化DHT11驱动

        Args:
            max_retries: 最大重试次数
            timeout_ms: 超时时间（毫秒）
        """
        self.max_retries = max_retries
        self.timeout = timeout_ms / 1000.0
        self.last_read_time = 0
        self.min_interval = 2.0  # DHT11最小读取间隔2秒

    def _simulate_timing_sequence(self) -> bool:
        """
        模拟DHT11的时序交互
        返回是否成功启动通信
        """
        # 模拟主机启动信号（拉低至少18ms）
        time.sleep(0.02)

        # 模拟DHT11响应（拉低80us，再拉高80us）
        time.sleep(0.00016)

        # 90%的成功率模拟
        return random.random() < 0.9

    def _read_data_bits(self) -> Optional[list]:
        """
        读取40位数据

        Returns:
            40位数据列表，失败返回None
        """
        if not self._simulate_timing_sequence():
            return None

        # 模拟生成合理的温湿度数据
        humidity = random.randint(20, 80)
        temperature = random.randint(15, 35)
        checksum = (humidity + 0 + temperature + 0) & 0xFF

        data_bytes = [humidity, 0, temperature, 0, checksum]
        bit_stream = []

        for byte in data_bytes:
            for i in range(7, -1, -1):
                bit_stream.append(bool((byte >> i) & 1))

        return bit_stream

    def _parse_data(self, bit_stream: list) -> Tuple[Optional[int], Optional[int], bool]:
        """
        解析数据流

        Returns:
            (humidity, temperature, is_valid)
        """
        if len(bit_stream) != 40:
            return None, None, False

        data_bytes = []
        for i in range(0, 40, 8):
            byte = 0
            for j in range(8):
                if bit_stream[i + j]:
                    byte |= (1 << (7 - j))
            data_bytes.append(byte)

        humidity, humidity_frac, temperature, temperature_frac, checksum = data_bytes

        # 验证数据范围（DHT11有效范围）
        if not (0 <= humidity <= 100 and -20 <= temperature <= 60):
            return None, None, False

        calculated_checksum = (humidity + humidity_frac + temperature + temperature_frac) & 0xFF
        is_valid = (checksum == calculated_checksum)

        return humidity, temperature, is_valid

    def read(self) -> Tuple[Optional[int], Optional[int]]:
        """
        读取温湿度数据

        Returns:
            (humidity, temperature) 或 (None, None) 如果失败
        """
        current_time = time.time()

        # 检查最小读取间隔
        if current_time - self.last_read_time < self.min_interval:
            time.sleep(self.min_interval - (current_time - self.last_read_time))

        self.last_read_time = time.time()

        # 重试机制
        for attempt in range(self.max_retries):
            bit_stream = self._read_data_bits()
            if bit_stream is None:
                continue

            humidity, temperature, is_valid = self._parse_data(bit_stream)
            if is_valid:
                return humidity, temperature

            print(f"第{attempt + 1}次尝试失败，重试中...")
            time.sleep(0.1)

        return None, None

    def read_with_validation(self, max_deviation: int = 10) -> Tuple[Optional[int], Optional[int]]:
        """
        带有数据验证的读取（连续读取两次，检查偏差）

        Args:
            max_deviation: 最大允许偏差

        Returns:
            验证后的温湿度数据
        """
        # 第一次读取
        h1, t1 = self.read()
        if h1 is None or t1 is None:
            return None, None

        time.sleep(0.1)

        # 第二次读取
        h2, t2 = self.read()
        if h2 is None or t2 is None:
            return h1, t1  # 返回第一次的结果

        # 验证偏差
        if abs(h1 - h2) <= max_deviation and abs(t1 - t2) <= max_deviation:
            # 返回平均值
            return (h1 + h2) // 2, (t1 + t2) // 2
        else:
            # 偏差过大，可能有干扰，返回第一次的结果
            return h1, t1

class EnvironmentalMonitor:
    def __init__(self):
        """环境监测器"""
        self.dht11 = DHT11Driver()
        self.history = []

    def add_to_history(self, humidity: int, temperature: int):
        """添加到历史记录"""
        timestamp = time.time()
        self.history.append({
            'timestamp': timestamp,
            'humidity': humidity,
            'temperature': temperature
        })

        # 只保留最近10条记录
        if len(self.history) > 10:
            self.history.pop(0)

    def get_trends(self) -> dict:
        """获取趋势信息"""
        if len(self.history) < 2:
            return {'humidity_trend': 'stable', 'temperature_trend': 'stable'}

        first = self.history[0]
        last = self.history[-1]

        humidity_change = last['humidity'] - first['humidity']
        temperature_change = last['temperature'] - first['temperature']

        def get_trend(change):
            if change > 2:
                return 'rising'
            elif change < -2:
                return 'falling'
            else:
                return 'stable'

        return {
            'humidity_trend': get_trend(humidity_change),
            'temperature_trend': get_trend(temperature_change)
        }

    def monitor(self):
        """持续监测环境"""
        print("DHT11环境监测系统启动")
        print("按 Ctrl+C 停止监测")
        print("-" * 50)

        try:
            while True:
                humidity, temperature = self.dht11.read_with_validation()

                if humidity is not None and temperature is not None:
                    self.add_to_history(humidity, temperature)
                    trends = self.get_trends()

                    print(f"[{time.strftime('%H:%M:%S')}] "
                          f"湿度: {humidity}% ({trends['humidity_trend']}) | "
                          f"温度: {temperature}°C ({trends['temperature_trend']})")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] 传感器读取失败")

                time.sleep(2)

        except KeyboardInterrupt:
            print("\n监测结束")

def main():
    """主函数"""
    monitor = EnvironmentalMonitor()
    monitor.monitor()

if __name__ == "__main__":
    main()