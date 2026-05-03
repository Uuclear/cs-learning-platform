/*
 * Example 01: PWM 基础 - LED 亮度控制
 *
 * 这个程序演示 PWM（脉宽调制）的基本原理，
 * 通过改变占空比来控制 LED 的亮度。
 */

#include <Arduino.h>

// 定义 PWM 引脚
const int LED_PIN = 9;  // 使用支持 PWM 的引脚

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== PWM 基础 - LED 亮度控制 ===");
  Serial.println();
  Serial.println("PWM 占空比范围: 0-255 (0% - 100%)");
  Serial.println("这个程序演示不同占空比的效果");
  Serial.println();

  // 设置 LED 引脚为输出
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  static int demoStep = 0;
  static unsigned long lastDemoTime = 0;
  const unsigned long DEMO_INTERVAL = 2000; // 每2秒切换一次演示

  if (millis() - lastDemoTime >= DEMO_INTERVAL) {
    switch (demoStep % 5) {
      case 0:
        // 0% 占空比 (关闭)
        analogWrite(LED_PIN, 0);
        Serial.println("演示 1: 0% 占空比 (LED 关闭)");
        break;

      case 1:
        // 25% 占空比
        analogWrite(LED_PIN, 64);
        Serial.println("演示 2: 25% 占空比 (低亮度)");
        break;

      case 2:
        // 50% 占空比
        analogWrite(LED_PIN, 128);
        Serial.println("演示 3: 50% 占空比 (中等亮度)");
        break;

      case 3:
        // 75% 占空比
        analogWrite(LED_PIN, 192);
        Serial.println("演示 4: 75% 占空比 (高亮度)");
        break;

      case 4:
        // 100% 占空比 (全亮)
        analogWrite(LED_PIN, 255);
        Serial.println("演示 5: 100% 占空比 (LED 全亮)");
        break;
    }

    demoStep++;
    lastDemoTime = millis();
    Serial.println();
  }
}