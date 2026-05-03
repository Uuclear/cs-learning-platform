#!/usr/bin/env python3
"""
Solution 03: Arduino Blink 程序完整解析与扩展

这个完整的解决方案不仅解释了基本的 Blink 程序，
还展示了如何扩展它来实现更复杂的功能，
包括多 LED 控制、按钮交互和状态机。
"""

# 基本 Blink 程序
BASIC_BLINK_CODE = """
const int LED_PIN = 13;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
"""

# 扩展版本：多 LED 闪烁模式
MULTI_LED_CODE = """
// 多个 LED 引脚
const int LED_PINS[] = {8, 9, 10, 11, 12};
const int NUM_LEDS = 5;

void setup() {
  // 初始化所有 LED 引脚为输出
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
  }
}

void loop() {
  // 流水灯效果
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], HIGH);
    delay(200);
  }

  // 全部熄灭
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], LOW);
    delay(100);
  }

  // 反向流水灯
  for (int i = NUM_LEDS - 1; i >= 0; i--) {
    digitalWrite(LED_PINS[i], HIGH);
    delay(200);
  }

  // 全部熄灭
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], LOW);
    delay(100);
  }
}
"""

# 高级版本：带按钮控制的状态机
ADVANCED_BLINK_CODE = """
const int LED_PIN = 13;
const int BUTTON_PIN = 2;

// 状态定义
enum State {
  OFF,
  SLOW_BLINK,
  FAST_BLINK
};

State currentState = OFF;
unsigned long lastToggleTime = 0;
unsigned long blinkInterval = 1000; // 初始间隔 1000ms

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP); // 内部上拉电阻
  digitalWrite(LED_PIN, LOW); // 确保初始状态为关闭
}

void loop() {
  // 检查按钮状态（去抖动）
  static unsigned long lastButtonPress = 0;
  if (digitalRead(BUTTON_PIN) == LOW) { // 按钮按下（低电平）
    if (millis() - lastButtonPress > 50) { // 50ms 去抖动
      // 切换状态
      switch (currentState) {
        case OFF:
          currentState = SLOW_BLINK;
          blinkInterval = 1000;
          break;
        case SLOW_BLINK:
          currentState = FAST_BLINK;
          blinkInterval = 200;
          break;
        case FAST_BLINK:
          currentState = OFF;
          digitalWrite(LED_PIN, LOW); // 关闭 LED
          break;
      }
      lastButtonPress = millis();
    }
  }

  // 根据当前状态执行相应操作
  if (currentState != OFF) {
    if (millis() - lastToggleTime >= blinkInterval) {
      // 切换 LED 状态
      bool ledState = digitalRead(LED_PIN);
      digitalWrite(LED_PIN, !ledState);
      lastToggleTime = millis();
    }
  }
}
"""

def explain_basic_concepts():
    """解释基本概念"""
    print("=== Arduino Blink 程序核心概念 ===\n")

    print("1. 硬件抽象:")
    print("   - pinMode(): 配置引脚功能")
    print("   - digitalWrite(): 控制数字输出")
    print("   - digitalRead(): 读取数字输入")
    print("   - delay(): 阻塞式延时\n")

    print("2. 程序执行模型:")
    print("   - setup(): 只执行一次，用于初始化")
    print("   - loop(): 无限循环，包含主逻辑")
    print("   - 单线程执行，没有操作系统\n")

    print("3. 电气特性:")
    print("   - 数字输出: HIGH (通常 5V 或 3.3V), LOW (0V)")
    print("   - 电流限制: 通常每个引脚最大 20-40mA")
    print("   - 上拉/下拉电阻: 防止浮动输入\n")

def explain_advanced_concepts():
    """解释高级概念"""
    print("=== 高级 Blink 程序概念 ===\n")

    print("1. 非阻塞延时:")
    print("   - 使用 millis() 而不是 delay()")
    print("   - 允许同时处理多个任务")
    print("   - 实现真正的并发行为\n")

    print("2. 状态机设计:")
    print("   - 将程序分解为离散状态")
    print("   - 清晰的状态转换逻辑")
    print("   - 易于扩展和维护\n")

    print("3. 输入去抖动:")
    print("   - 机械开关会产生多次跳变")
    print("   - 软件去抖动: 忽略短时间内的重复触发")
    print("   - 硬件去抖动: 使用 RC 电路\n")

    print("4. 内存考虑:")
    print("   - AVR 微控制器内存有限")
    print("   - 避免动态内存分配")
    print("   - 使用 const 和 PROGMEM 节省 RAM\n")

def demonstrate_execution_flow():
    """演示执行流程"""
    import time

    print("=== 执行流程对比 ===\n")

    print("基础版本 (阻塞式):")
    print("  [setup] → [LED ON] → [等待1s] → [LED OFF] → [等待1s] → 循环")
    print("  ✓ 简单易懂")
    print("  ✗ 无法同时处理其他任务\n")

    print("高级版本 (非阻塞式):")
    print("  [setup] → [检查按钮] → [检查时间] → [更新LED] → 循环")
    print("  ✓ 可以同时响应多个事件")
    print("  ✓ 更高效的资源利用")
    print("  ✗ 代码稍微复杂\n")

    # 模拟非阻塞执行
    print("模拟非阻塞执行 (1秒内):")
    start_time = time.time()
    led_state = False
    last_toggle = start_time
    button_pressed = False

    while time.time() - start_time < 1.0:
        current_time = time.time()

        # 模拟按钮检查 (每100ms)
        if int((current_time - start_time) * 10) % 10 == 0:
            if not button_pressed and random.random() < 0.1:  # 10% 概率按下
                button_pressed = True
                print(f"  {current_time-start_time:.2f}s: 按钮按下!")

        # LED 闪烁逻辑 (每500ms)
        if current_time - last_toggle >= 0.5:
            led_state = not led_state
            last_toggle = current_time
            state_str = "ON" if led_state else "OFF"
            print(f"  {current_time-start_time:.2f}s: LED {state_str}")

        time.sleep(0.01)  # 模拟快速循环

def show_code_comparison():
    """显示代码对比"""
    print("\n=== 代码演进对比 ===\n")

    print("1. 基础 Blink:")
    print("-" * 40)
    print(BASIC_BLINK_CODE.strip())
    print("-" * 40)

    print("\n2. 多 LED 扩展:")
    print("-" * 40)
    print(MULTI_LED_CODE.strip())
    print("-" * 40)

    print("\n3. 高级状态机:")
    print("-" * 40)
    print(ADVANCED_BLINK_CODE.strip())
    print("-" * 40)

def main():
    """主函数"""
    explain_basic_concepts()
    explain_advanced_concepts()
    demonstrate_execution_flow()
    show_code_comparison()

    print("\n=== 学习要点总结 ===")
    print("• 从简单开始: Blink 是验证环境的最佳方式")
    print("• 理解硬件限制: 内存、处理能力和 I/O 约束")
    print("• 掌握非阻塞编程: 这是嵌入式开发的关键技能")
    print("• 状态机模式: 处理复杂逻辑的有效方法")
    print("• 调试技巧: 串口输出、LED 指示、逻辑分析仪")

if __name__ == "__main__":
    main()