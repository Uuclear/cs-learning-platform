#!/usr/bin/env python3
"""
Example 01: 模拟单片机 GPIO 高低电平输出

这个简单的 Python 程序模拟了单片机如何控制 GPIO 引脚的高低电平。
在真实的单片机中，这通常用于控制 LED、继电器或其他数字设备。
"""

import time
import random

class GPIOPin:
    """模拟 GPIO 引脚类"""
    def __init__(self, pin_number):
        self.pin_number = pin_number
        self.state = False  # False 表示低电平 (0V), True 表示高电平 (通常 3.3V 或 5V)
        self.mode = "OUTPUT"  # 引脚模式：INPUT 或 OUTPUT

    def digitalWrite(self, state):
        """设置引脚输出状态"""
        if self.mode != "OUTPUT":
            print(f"警告: 引脚 {self.pin_number} 不是输出模式!")
            return

        self.state = bool(state)
        voltage = "高电平 (3.3V)" if self.state else "低电平 (0V)"
        print(f"GPIO{self.pin_number}: 设置为 {voltage}")

    def digitalRead(self):
        """读取引脚输入状态"""
        if self.mode != "INPUT":
            print(f"警告: 引脚 {self.pin_number} 不是输入模式!")
            return None

        # 在真实硬件中，这里会读取实际的电压水平
        # 这里我们随机返回一个值来模拟外部信号
        return random.choice([True, False])

    def setMode(self, mode):
        """设置引脚模式"""
        if mode.upper() in ["INPUT", "OUTPUT"]:
            self.mode = mode.upper()
            print(f"GPIO{self.pin_number}: 设置为 {self.mode} 模式")
        else:
            print("错误: 模式必须是 INPUT 或 OUTPUT")

def main():
    """主函数 - 演示 GPIO 基本操作"""
    print("=== 单片机 GPIO 模拟演示 ===\n")

    # 创建一个模拟的 GPIO 引脚 (比如连接到 LED)
    led_pin = GPIOPin(13)  # Arduino Uno 的内置 LED 通常在引脚 13

    # 设置引脚为输出模式
    led_pin.setMode("OUTPUT")

    print("\n--- LED 闪烁演示 ---")
    for i in range(5):
        # 点亮 LED (高电平)
        led_pin.digitalWrite(True)
        time.sleep(0.5)

        # 熄灭 LED (低电平)
        led_pin.digitalWrite(False)
        time.sleep(0.5)

    print("\n--- 按钮输入模拟 ---")
    button_pin = GPIOPin(2)
    button_pin.setMode("INPUT")

    for i in range(3):
        button_state = button_pin.digitalRead()
        status = "按下" if button_state else "未按下"
        print(f"按钮状态: {status}")
        time.sleep(1)

    print("\n演示完成!")

if __name__ == "__main__":
    main()