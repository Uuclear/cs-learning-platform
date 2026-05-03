#!/usr/bin/env python3
"""
Solution 01: 模拟单片机 GPIO 高低电平输出

这是完整的解决方案，包含了更完善的 GPIO 模拟功能，
包括中断模拟、PWM 输出模拟等高级特性。
"""

import time
import threading
import random
from typing import Callable, Optional

class GPIOPin:
    """增强版 GPIO 引脚类"""
    def __init__(self, pin_number: int):
        self.pin_number = pin_number
        self.state = False
        self.mode = "INPUT"
        self.pull_mode = None  # PULLUP, PULLDOWN, or None
        self.interrupt_callback: Optional[Callable] = None
        self.interrupt_enabled = False
        self.pwm_duty_cycle = 0.0
        self.pwm_frequency = 1000  # Hz
        self.pwm_active = False
        self._pwm_thread = None
        self._stop_pwm = False

    def digitalWrite(self, state: bool) -> None:
        """设置引脚输出状态"""
        if self.mode != "OUTPUT":
            raise ValueError(f"引脚 {self.pin_number} 不是输出模式!")

        old_state = self.state
        self.state = bool(state)
        voltage = "高电平 (3.3V)" if self.state else "低电平 (0V)"
        print(f"GPIO{self.pin_number}: 设置为 {voltage}")

        # 如果启用了中断并且状态发生变化，触发回调
        if self.interrupt_enabled and self.interrupt_callback and old_state != self.state:
            self.interrupt_callback(self.pin_number, self.state)

    def digitalRead(self) -> bool:
        """读取引脚输入状态"""
        if self.mode != "INPUT":
            raise ValueError(f"引脚 {self.pin_number} 不是输入模式!")

        # 在真实硬件中，这里会读取实际的电压水平
        # 这里我们根据上拉/下拉模式返回合理的默认值
        if self.pull_mode == "PULLUP":
            return True  # 默认高电平
        elif self.pull_mode == "PULLDOWN":
            return False  # 默认低电平
        else:
            # 无上拉/下拉，随机返回（模拟浮动输入）
            return random.choice([True, False])

    def setMode(self, mode: str, pull_mode: Optional[str] = None) -> None:
        """设置引脚模式和上拉/下拉电阻"""
        mode = mode.upper()
        if mode not in ["INPUT", "OUTPUT"]:
            raise ValueError("模式必须是 INPUT 或 OUTPUT")

        if pull_mode:
            pull_mode = pull_mode.upper()
            if pull_mode not in ["PULLUP", "PULLDOWN"]:
                raise ValueError("上拉/下拉模式必须是 PULLUP 或 PULLDOWN")
            self.pull_mode = pull_mode
        else:
            self.pull_mode = None

        self.mode = mode
        print(f"GPIO{self.pin_number}: 设置为 {self.mode} 模式" +
              (f" ({self.pull_mode})" if self.pull_mode else ""))

    def attachInterrupt(self, callback: Callable, mode: str = "CHANGE") -> None:
        """附加中断回调函数（模拟）"""
        self.interrupt_callback = callback
        self.interrupt_enabled = True
        print(f"GPIO{self.pin_number}: 中断已启用 ({mode})")

    def detachInterrupt(self) -> None:
        """禁用中断"""
        self.interrupt_enabled = False
        self.interrupt_callback = None
        print(f"GPIO{self.pin_number}: 中断已禁用")

    def analogWrite(self, value: int) -> None:
        """模拟 PWM 输出 (0-255)"""
        if self.mode != "OUTPUT":
            raise ValueError(f"引脚 {self.pin_number} 不是输出模式!")

        if not 0 <= value <= 255:
            raise ValueError("PWM 值必须在 0-255 范围内")

        self.pwm_duty_cycle = value / 255.0
        self.pwm_active = True

        # 启动 PWM 模拟线程
        if self._pwm_thread is None or not self._pwm_thread.is_alive():
            self._stop_pwm = False
            self._pwm_thread = threading.Thread(target=self._simulate_pwm)
            self._pwm_thread.daemon = True
            self._pwm_thread.start()

        print(f"GPIO{self.pin_number}: PWM 启动 - 占空比 {self.pwm_duty_cycle:.1%}")

    def _simulate_pwm(self) -> None:
        """内部 PWM 模拟线程"""
        period = 1.0 / self.pwm_frequency
        on_time = period * self.pwm_duty_cycle
        off_time = period * (1 - self.pwm_duty_cycle)

        while not self._stop_pwm and self.pwm_active:
            if self.pwm_duty_cycle > 0:
                self.state = True
                time.sleep(on_time)
            if self.pwm_duty_cycle < 1:
                self.state = False
                time.sleep(off_time)

    def stopPWM(self) -> None:
        """停止 PWM 输出"""
        self.pwm_active = False
        self._stop_pwm = True
        if self._pwm_thread:
            self._pwm_thread.join(timeout=0.1)
        self._pwm_thread = None
        print(f"GPIO{self.pin_number}: PWM 已停止")

def button_interrupt_handler(pin: int, state: bool) -> None:
    """按钮中断处理函数"""
    action = "按下" if state else "释放"
    print(f"按钮中断! 引脚 {pin} {action}")

def main() -> None:
    """主函数 - 演示完整的 GPIO 功能"""
    print("=== 单片机 GPIO 完整功能演示 ===\n")

    # LED 控制演示
    led_pin = GPIOPin(13)
    led_pin.setMode("OUTPUT")

    print("1. 基本 LED 闪烁:")
    for i in range(3):
        led_pin.digitalWrite(True)
        time.sleep(0.3)
        led_pin.digitalWrite(False)
        time.sleep(0.3)

    print("\n2. PWM LED 亮度控制:")
    led_pin.analogWrite(64)   # 25% 亮度
    time.sleep(1)
    led_pin.analogWrite(128)  # 50% 亮度
    time.sleep(1)
    led_pin.analogWrite(192)  # 75% 亮度
    time.sleep(1)
    led_pin.stopPWM()

    # 按钮输入演示
    print("\n3. 按钮输入与中断:")
    button_pin = GPIOPin(2)
    button_pin.setMode("INPUT", "PULLUP")  # 内部上拉电阻

    # 模拟按钮按下事件
    print("读取按钮状态 (上拉模式，未按下时为高电平):")
    for i in range(3):
        state = button_pin.digitalRead()
        status = "未按下" if state else "按下"
        print(f"  按钮状态: {status}")
        time.sleep(0.5)

    # 启用中断（模拟）
    button_pin.attachInterrupt(button_interrupt_handler, "FALLING")

    # 模拟按钮按下触发中断
    print("\n模拟按钮按下触发中断:")
    button_pin.digitalWrite(False)  # 模拟按下
    time.sleep(0.1)
    button_pin.digitalWrite(True)   # 模拟释放

    button_pin.detachInterrupt()
    print("\n演示完成!")

if __name__ == "__main__":
    main()