"""
Example 01: 按钮防抖（debounce）算法模拟

机械按钮在按下和释放时会产生机械抖动，
导致短时间内产生多个开关信号。
防抖算法通过延时确认来消除这种抖动。
"""

import time
import random

class ButtonDebounce:
    def __init__(self, debounce_time_ms=50):
        """
        初始化按钮防抖器

        Args:
            debounce_time_ms (int): 防抖时间，单位毫秒，默认50ms
        """
        self.debounce_time = debounce_time_ms / 1000.0  # 转换为秒
        self.last_state = 0
        self.last_debounce_time = 0

    def read_button_raw(self):
        """
        模拟读取原始按钮状态（包含抖动）
        在实际硬件中，这会直接读取GPIO引脚
        """
        current_time = time.time()
        # 模拟按钮按下的时间段（2-4秒）
        if 2 <= (current_time % 6) <= 4:
            # 模拟抖动：在稳定状态附近随机波动
            return random.choice([1, 1, 1, 0, 1])  # 80%概率为1
        else:
            return random.choice([0, 0, 0, 1, 0])  # 80%概率为0

    def read_button_debounced(self):
        """
        读取经过防抖处理的按钮状态

        Returns:
            int: 防抖后的按钮状态（0或1）
        """
        reading = self.read_button_raw()
        current_time = time.time()

        # 如果读数与上次状态不同，重新计时
        if reading != self.last_state:
            self.last_debounce_time = current_time

        # 如果超过防抖时间，确认状态变化
        if (current_time - self.last_debounce_time) > self.debounce_time:
            if reading != self.last_state:
                self.last_state = reading

        return self.last_state

def main():
    """主函数：演示按钮防抖效果"""
    button = ButtonDebounce(debounce_time_ms=50)

    print("按钮防抖演示 (运行10秒)")
    print("时间(s)\t原始状态\t防抖状态")
    print("-" * 35)

    start_time = time.time()
    while time.time() - start_time < 10:
        raw_state = button.read_button_raw()
        debounced_state = button.read_button_debounced()
        elapsed = int(time.time() - start_time)

        print(f"{elapsed}\t{raw_state}\t\t{debounced_state}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()