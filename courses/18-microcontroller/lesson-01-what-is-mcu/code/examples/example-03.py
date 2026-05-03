#!/usr/bin/env python3
"""
Example 03: Arduino Blink 程序解析

这个文件包含了经典的 Arduino Blink 程序，并提供了详细的注释解释。
Blink 程序是嵌入式开发的 "Hello World"，用于验证开发环境和基本功能。
"""

# Arduino Blink 程序 (C++ 代码)
ARDUINO_BLINK_CODE = """
// 引脚13通常连接到Arduino板载LED
const int LED_PIN = 13;

void setup() {
  // 初始化LED引脚为输出模式
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // 点亮LED (设置引脚为高电平)
  digitalWrite(LED_PIN, HIGH);
  // 延迟1000毫秒 (1秒)
  delay(1000);

  // 熄灭LED (设置引脚为低电平)
  digitalWrite(LED_PIN, LOW);
  // 再次延迟1000毫秒
  delay(1000);
}
"""

def explain_arduino_blink():
    """解释 Arduino Blink 程序的关键概念"""
    print("=== Arduino Blink 程序详细解析 ===\n")

    print("1. 程序结构:")
    print("   Arduino 程序有两个必需的函数:")
    print("   - setup(): 在程序开始时只运行一次，用于初始化")
    print("   - loop(): 在 setup() 之后重复运行，包含主要逻辑\n")

    print("2. 关键函数说明:")
    print("   - pinMode(pin, mode): 设置引脚模式")
    print("     * pin: 引脚编号 (如 13)")
    print("     * mode: INPUT (输入) 或 OUTPUT (输出)")
    print("   - digitalWrite(pin, value): 设置输出引脚的电平")
    print("     * value: HIGH (高电平, 通常5V) 或 LOW (低电平, 0V)")
    print("   - delay(milliseconds): 暂停指定的毫秒数\n")

    print("3. 硬件连接:")
    print("   - Arduino Uno 板载 LED 连接到数字引脚 13")
    print("   - 当引脚13输出 HIGH 时，LED 点亮")
    print("   - 当引脚13输出 LOW 时，LED 熄灭\n")

    print("4. 执行流程:")
    print("   Step 1: setup() 函数运行一次 -> 设置引脚13为输出模式")
    print("   Step 2: loop() 函数开始执行:")
    print("           -> 设置引脚13为 HIGH -> LED 点亮")
    print("           -> 等待 1000ms (1秒)")
    print("           -> 设置引脚13为 LOW -> LED 熄灭")
    print("           -> 等待 1000ms (1秒)")
    print("   Step 3: loop() 函数重复执行步骤2\n")

    print("5. 为什么这是重要的第一个程序?")
    print("   - 验证开发环境是否正确安装")
    print("   - 确认 Arduino 板能够接收和运行程序")
    print("   - 测试基本的数字输出功能")
    print("   - 学习 Arduino 程序的基本结构\n")

    print("完整的 Arduino Blink 代码:")
    print("-" * 50)
    print(ARDUINO_BLINK_CODE.strip())
    print("-" * 50)

def simulate_blink_execution():
    """模拟 Blink 程序的执行过程"""
    import time

    print("\n=== 模拟 Blink 程序执行 ===")
    print("执行 setup()...")
    time.sleep(0.5)
    print("✓ 引脚13设置为OUTPUT模式")

    print("\n开始 loop() 循环 (演示2个周期):")
    for cycle in range(2):
        print(f"\n循环 {cycle + 1}:")
        print("  digitalWrite(13, HIGH) → LED 点亮")
        time.sleep(0.3)  # 加速演示
        print("  delay(1000) → 等待1秒")
        time.sleep(0.2)
        print("  digitalWrite(13, LOW) → LED 熄灭")
        time.sleep(0.3)
        print("  delay(1000) → 等待1秒")
        time.sleep(0.2)

    print("\n✓ Blink 程序模拟完成!")

def main():
    """主函数"""
    explain_arduino_blink()
    simulate_blink_execution()

if __name__ == "__main__":
    main()