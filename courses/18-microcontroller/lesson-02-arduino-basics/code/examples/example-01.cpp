/*
 * Example 01: LED 限流电阻演示
 *
 * 这个程序演示了如何在 Arduino 中使用不同阻值的限流电阻
 * 来控制 LED 的亮度。虽然实际电阻值是在硬件上选择的，
 * 但我们可以用 PWM 来模拟不同电流的效果。
 */

#include <Arduino.h>

// 定义引脚和常量
const int LED_PIN = 9;  // 使用支持 PWM 的引脚 (9, 10, 11 等)

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== LED 限流电阻演示 ===");
  Serial.println();
  Serial.println("这个程序使用 PWM 模拟不同限流电阻的效果:");
  Serial.println("- 高 PWM 值 = 小电阻 = 高电流 = 亮 LED");
  Serial.println("- 低 PWM 值 = 大电阻 = 低电流 = 暗 LED");
  Serial.println();
  Serial.println("电阻计算公式: R = (Vcc - Vled) / I");
  Serial.println("其中:");
  Serial.println("- Vcc = 电源电压 (5V)");
  Serial.println("- Vled = LED 正向电压降 (红色约 2.0V)");
  Serial.println("- I = 期望电流 (通常 5-20mA)");
  Serial.println();

  // 设置 LED 引脚为输出
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  static int demoStep = 0;
  static unsigned long lastDemoTime = 0;
  const unsigned long DEMO_INTERVAL = 3000; // 每3秒切换一次演示

  if (millis() - lastDemoTime >= DEMO_INTERVAL) {
    switch (demoStep % 4) {
      case 0:
        // 模拟小电阻 (高电流，约 20mA)
        analogWrite(LED_PIN, 255); // 100% 占空比
        Serial.println("演示 1: 小电阻效果 (高亮度)");
        Serial.println("  计算: R = (5V - 2V) / 0.02A = 150Ω");
        break;

      case 1:
        // 模拟中等电阻 (中等电流，约 10mA)
        analogWrite(LED_PIN, 128); // 50% 占空比
        Serial.println("演示 2: 中等电阻效果 (中等亮度)");
        Serial.println("  计算: R = (5V - 2V) / 0.01A = 300Ω");
        break;

      case 2:
        // 模拟大电阻 (低电流，约 5mA)
        analogWrite(LED_PIN, 64); // 25% 占空比
        Serial.println("演示 3: 大电阻效果 (低亮度)");
        Serial.println("  计算: R = (5V - 2V) / 0.005A = 600Ω");
        break;

      case 3:
        // 关闭 LED
        analogWrite(LED_PIN, 0);
        Serial.println("演示 4: LED 关闭");
        Serial.println("  注意: 实际电路中仍需要限流电阻!");
        break;
    }

    demoStep++;
    lastDemoTime = millis();
    Serial.println();
  }
}