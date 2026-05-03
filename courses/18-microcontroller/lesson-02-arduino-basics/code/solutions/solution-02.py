#!/usr/bin/env python3
"""
Arduino Blink 程序逻辑模拟器 - 完整解决方案

这个脚本完整模拟 Arduino 的执行环境，
包括准确的时间戳和引脚状态跟踪。
"""

import time
from datetime import datetime

class Pin:
    """引脚类"""
    def __init__(self, pin_number):
        self.pin_number = pin_number
        self.mode = None  # 'INPUT' or 'OUTPUT'
        self.value = None  # 'HIGH', 'LOW', or None

    def __str__(self):
        return f"Pin({self.pin_number}, mode={self.mode}, value={self.value})"

class ArduinoSimulator:
    """完整的 Arduino 模拟器"""

    def __init__(self):
        self.pins = {}  # pin_number -> Pin object
        self.start_time = None
        self.elapsed_time = 0

    def pinMode(self, pin_number, mode):
        """设置引脚模式"""
        if mode not in ['INPUT', 'OUTPUT']:
            raise ValueError(f"无效的模式: {mode}")

        if pin_number not in self.pins:
            self.pins[pin_number] = Pin(pin_number)

        self.pins[pin_number].mode = mode
        self.pins[pin_number].value = 'LOW' if mode == 'OUTPUT' else None

        self.log(f"pinMode({pin_number}, {mode})")

    def digitalWrite(self, pin_number, value):
        """写入数字值到引脚"""
        if pin_number not in self.pins:
            raise ValueError(f"引脚 {pin_number} 未初始化")

        if self.pins[pin_number].mode != 'OUTPUT':
            raise ValueError(f"引脚 {pin_number} 不是 OUTPUT 模式")

        if value not in ['HIGH', 'LOW']:
            raise ValueError(f"无效的值: {value}")

        self.pins[pin_number].value = value
        self.log(f"digitalWrite({pin_number}, {value}) {'💡' if value == 'HIGH' else '🌑'}")

    def digitalRead(self, pin_number):
        """从引脚读取数字值"""
        if pin_number not in self.pins:
            raise ValueError(f"引脚 {pin_number} 未初始化")

        if self.pins[pin_number].mode != 'INPUT':
            raise ValueError(f"引脚 {pin_number} 不是 INPUT 模式")

        return self.pins[pin_number].value

    def delay(self, milliseconds):
        """延迟指定毫秒数"""
        if self.start_time is None:
            self.start_time = time.time()

        sleep_time = milliseconds / 1000.0
        time.sleep(sleep_time)
        self.elapsed_time += milliseconds

    def log(self, message):
        """记录带时间戳的消息"""
        current_time = self.elapsed_time if self.start_time else 0
        print(f"[{current_time:6.0f}ms] {message}")

    def setup(self):
        """setup 函数 - 子类重写"""
        pass

    def loop(self):
        """loop 函数 - 子类重写"""
        pass

    def run(self, max_iterations=None, max_duration_ms=None):
        """运行模拟器"""
        print("=== Arduino 模拟器启动 ===")
        self.start_time = time.time()
        self.elapsed_time = 0

        # 执行 setup
        self.setup()

        iteration = 0
        while True:
            iteration += 1

            # 检查迭代限制
            if max_iterations and iteration > max_iterations:
                break

            # 检查时间限制
            if max_duration_ms and self.elapsed_time >= max_duration_ms:
                break

            self.loop()

        print(f"\n模拟结束: {iteration} 次循环, 总时间: {self.elapsed_time:.0f}ms")

class AdvancedBlinkSimulator(ArduinoSimulator):
    """高级 Blink 模拟器，支持多个 LED 和不同闪烁模式"""

    def __init__(self, led_pins=None, patterns=None):
        super().__init__()
        self.led_pins = led_pins or [13]
        self.patterns = patterns or ['blink']

    def setup(self):
        """初始化所有 LED 引脚"""
        for pin in self.led_pins:
            self.pinMode(pin, 'OUTPUT')

    def loop(self):
        """根据模式执行不同的闪烁效果"""
        for pattern in self.patterns:
            if pattern == 'blink':
                self.blink_pattern()
            elif pattern == 'chase':
                self.chase_pattern()
            elif pattern == 'strobe':
                self.strobe_pattern()

    def blink_pattern(self):
        """基本闪烁模式"""
        for pin in self.led_pins:
            self.digitalWrite(pin, 'HIGH')
        self.delay(500)

        for pin in self.led_pins:
            self.digitalWrite(pin, 'LOW')
        self.delay(500)

    def chase_pattern(self):
        """跑马灯模式"""
        if len(self.led_pins) <= 1:
            return

        # 正向
        for pin in self.led_pins:
            self.digitalWrite(pin, 'HIGH')
            self.delay(100)
            self.digitalWrite(pin, 'LOW')

        # 反向
        for pin in reversed(self.led_pins):
            self.digitalWrite(pin, 'HIGH')
            self.delay(100)
            self.digitalWrite(pin, 'LOW')

    def strobe_pattern(self):
        """频闪模式"""
        for _ in range(3):
            for pin in self.led_pins:
                self.digitalWrite(pin, 'HIGH')
            self.delay(50)
            for pin in self.led_pins:
                self.digitalWrite(pin, 'LOW')
            self.delay(50)
        self.delay(900)  # 休息

def main():
    """主函数 - 演示不同的模拟场景"""
    print("选择演示场景:")
    print("1. 标准 Blink (引脚 13)")
    print("2. 多 LED 同步闪烁 (引脚 8,9,10)")
    print("3. 跑马灯效果 (引脚 8,9,10,11)")
    print("4. 高级模式组合")

    choice = input("请选择 (1-4): ").strip()

    if choice == "1":
        sim = AdvancedBlinkSimulator([13], ['blink'])
        sim.run(max_duration_ms=3000)

    elif choice == "2":
        sim = AdvancedBlinkSimulator([8, 9, 10], ['blink'])
        sim.run(max_duration_ms=3000)

    elif choice == "3":
        sim = AdvancedBlinkSimulator([8, 9, 10, 11], ['chase'])
        sim.run(max_duration_ms=5000)

    elif choice == "4":
        sim = AdvancedBlinkSimulator([8, 9, 10], ['blink', 'strobe'])
        sim.run(max_iterations=5)

    else:
        print("无效选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n模拟被中断")
    except Exception as e:
        print(f"错误: {e}")