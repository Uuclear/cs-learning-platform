"""
Solution 01: 按钮防抖（debounce）算法完整实现

这是一个更完善的按钮防抖实现，
包含了状态变化检测和回调函数支持。
"""

import time
import random

class AdvancedButtonDebounce:
    def __init__(self, debounce_time_ms=50, press_callback=None, release_callback=None):
        """
        初始化高级按钮防抖器

        Args:
            debounce_time_ms (int): 防抖时间，单位毫秒
            press_callback (function): 按钮按下时的回调函数
            release_callback (function): 按钮释放时的回调函数
        """
        self.debounce_time = debounce_time_ms / 1000.0
        self.press_callback = press_callback
        self.release_callback = release_callback
        self.current_state = 0
        self.previous_state = 0
        self.last_debounce_time = 0

    def read_hardware(self):
        """
        硬件读取函数（在实际应用中替换为真实的GPIO读取）
        """
        current_time = time.time()
        # 模拟按钮按下的时间段
        if 2 <= (current_time % 6) <= 4:
            return 1  # 按下状态
        else:
            return 0  # 释放状态

    def update(self):
        """
        更新按钮状态并处理防抖逻辑
        返回当前按钮状态
        """
        reading = self.read_hardware()
        current_time = time.time()

        # 如果读数与当前状态不同，重新计时
        if reading != self.current_state:
            self.last_debounce_time = current_time

        # 如果超过防抖时间，确认状态变化
        if (current_time - self.last_debounce_time) > self.debounce_time:
            if reading != self.current_state:
                self.previous_state = self.current_state
                self.current_state = reading

                # 触发回调函数
                if self.current_state == 1 and self.press_callback:
                    self.press_callback()
                elif self.current_state == 0 and self.release_callback:
                    self.release_callback()

        return self.current_state

    def is_pressed(self):
        """检查按钮是否被按下"""
        return self.current_state == 1

    def was_pressed(self):
        """检查按钮是否刚刚被按下（单次触发）"""
        result = (self.previous_state == 0) and (self.current_state == 1)
        if result:
            self.previous_state = 1  # 重置标志，避免重复触发
        return result

def on_button_press():
    """按钮按下回调函数"""
    print(f"[{time.strftime('%H:%M:%S')}] 按钮被按下！")

def on_button_release():
    """按钮释放回调函数"""
    print(f"[{time.strftime('%H:%M:%S')}] 按钮被释放！")

def main():
    """主函数：演示高级按钮防抖功能"""
    button = AdvancedButtonDebounce(
        debounce_time_ms=50,
        press_callback=on_button_press,
        release_callback=on_button_release
    )

    print("高级按钮防抖演示")
    print("观察按钮按下/释放事件...")
    print("-" * 30)

    start_time = time.time()
    while time.time() - start_time < 15:
        state = button.update()

        # 演示was_pressed()的单次触发特性
        if button.was_pressed():
            print(f"[{time.strftime('%H:%M:%S')}] 单次触发：按钮按下事件！")

        time.sleep(0.01)  # 10ms更新间隔

if __name__ == "__main__":
    main()