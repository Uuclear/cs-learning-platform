#!/usr/bin/env python3
"""
Arduino Blink 程序逻辑模拟器

这个脚本模拟 Arduino Blink 程序的执行逻辑，
帮助理解程序如何控制 LED 的亮灭。

使用方法：
    python example-02.py
"""

import time
import threading
from datetime import datetime

class ArduinoSimulator:
    """Arduino 模拟器类"""

    def __init__(self):
        self.pins = {}  # 存储引脚状态
        self.running = False
        self.start_time = None

    def pinMode(self, pin, mode):
        """设置引脚模式"""
        if mode not in ['INPUT', 'OUTPUT']:
            raise ValueError("模式必须是 'INPUT' 或 'OUTPUT'")

        self.pins[pin] = {
            'mode': mode,
            'value': 'LOW' if mode == 'OUTPUT' else 'UNDEFINED'
        }
        print(f"引脚 {pin} 设置为 {mode} 模式")

    def digitalWrite(self, pin, value):
        """向引脚写入数字值"""
        if pin not in self.pins:
            raise ValueError(f"引脚 {pin} 未初始化，请先调用 pinMode()")

        if self.pins[pin]['mode'] != 'OUTPUT':
            raise ValueError(f"引脚 {pin} 不是 OUTPUT 模式")

        if value not in ['HIGH', 'LOW']:
            raise ValueError("值必须是 'HIGH' 或 'LOW'")

        self.pins[pin]['value'] = value
        current_time = time.time() - self.start_time if self.start_time else 0
        status = "💡" if value == 'HIGH' else "🌑"
        print(f"[{current_time:.3f}s] 引脚 {pin}: {value} {status}")

    def delay(self, milliseconds):
        """延迟指定毫秒数"""
        time.sleep(milliseconds / 1000.0)

    def setup(self):
        """setup 函数 - 在这里初始化硬件"""
        # 这里会被子类重写
        pass

    def loop(self):
        """loop 函数 - 主循环"""
        # 这里会被子类重写
        pass

    def run(self, duration_seconds=10):
        """运行模拟器"""
        print("=== Arduino Blink 模拟器 ===")
        print(f"模拟运行 {duration_seconds} 秒...")
        print()

        self.running = True
        self.start_time = time.time()

        # 执行 setup 一次
        self.setup()

        # 记录开始时间
        start_time = time.time()

        # 执行 loop 直到达到指定时间
        iteration = 0
        while self.running and (time.time() - start_time) < duration_seconds:
            iteration += 1
            # print(f"\n--- 第 {iteration} 次循环 ---")
            self.loop()

        self.running = False
        print(f"\n模拟结束，共执行了 {iteration} 次循环")

class BlinkSimulator(ArduinoSimulator):
    """Blink 程序模拟器"""

    def __init__(self):
        super().__init__()
        self.ledPin = 13  # LED 连接到引脚 13

    def setup(self):
        """初始化函数"""
        self.pinMode(self.ledPin, 'OUTPUT')

    def loop(self):
        """主循环函数"""
        # 点亮 LED
        self.digitalWrite(self.ledPin, 'HIGH')
        self.delay(1000)  # 等待 1 秒

        # 熄灭 LED
        self.digitalWrite(self.ledPin, 'LOW')
        self.delay(1000)  # 等待 1 秒

class CustomBlinkSimulator(ArduinoSimulator):
    """自定义闪烁模式模拟器"""

    def __init__(self, led_pin=8, on_time=500, off_time=1500):
        super().__init__()
        self.ledPin = led_pin
        self.onTime = on_time    # LED 亮的时间 (ms)
        self.offTime = off_time  # LED 灭的时间 (ms)

    def setup(self):
        """初始化函数"""
        self.pinMode(self.ledPin, 'OUTPUT')
        print(f"自定义闪烁模式: 亮 {self.onTime}ms, 灭 {self.offTime}ms")
        print()

    def loop(self):
        """主循环函数"""
        # 点亮 LED
        self.digitalWrite(self.ledPin, 'HIGH')
        self.delay(self.onTime)

        # 熄灭 LED
        self.digitalWrite(self.ledPin, 'LOW')
        self.delay(self.offTime)

def main():
    """主函数"""
    print("选择要运行的模拟器:")
    print("1. 标准 Blink (1秒亮/1秒灭)")
    print("2. 自定义闪烁模式")

    try:
        choice = input("请输入选择 (1 或 2): ").strip()

        if choice == "1":
            simulator = BlinkSimulator()
            simulator.run(duration_seconds=6)  # 运行 6 秒，显示 3 个完整周期

        elif choice == "2":
            led_pin = int(input("LED 连接的引脚号 (默认 8): ") or "8")
            on_time = int(input("LED 亮的时间 (ms，默认 500): ") or "500")
            off_time = int(input("LED 灭的时间 (ms，默认 1500): ") or "1500")

            simulator = CustomBlinkSimulator(led_pin, on_time, off_time)
            simulator.run(duration_seconds=5)

        else:
            print("无效选择")

    except KeyboardInterrupt:
        print("\n模拟被用户中断")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()