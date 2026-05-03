/*
 * Solution 03: 高级 Blink 程序 - 带按钮控制的状态机
 *
 * 这个程序展示了如何使用状态机和非阻塞延时来创建
 * 更复杂的交互式程序，包括多状态 LED 控制。
 */

#include <Arduino.h>

// 定义引脚常量
const int LED_PIN = 13;      // LED 连接到引脚 13
const int BUTTON_PIN = 2;    // 按钮连接到引脚 2

// 状态定义
enum State {
  OFF,
  SLOW_BLINK,
  FAST_BLINK
};

// 全局变量
State currentState = OFF;
unsigned long lastToggleTime = 0;
unsigned long blinkInterval = 1000; // 初始间隔 1000ms

void setup() {
  // 初始化串口通信（用于调试）
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 高级 Blink 状态机演示 ===");
  Serial.println("按按钮切换状态:");
  Serial.println("- OFF: LED 关闭");
  Serial.println("- SLOW_BLINK: 慢速闪烁 (1秒)");
  Serial.println("- FAST_BLINK: 快速闪烁 (200ms)");
  Serial.println();

  // 初始化 LED 引脚为输出
  pinMode(LED_PIN, OUTPUT);

  // 初始化按钮引脚为输入，启用内部上拉电阻
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // 确保初始状态为关闭
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // 检查按钮状态（软件去抖动）
  static unsigned long lastButtonPress = 0;
  if (digitalRead(BUTTON_PIN) == LOW) { // 按钮按下（低电平，因为使用内部上拉）
    if (millis() - lastButtonPress > 50) { // 50ms 去抖动延迟
      // 切换状态
      switch (currentState) {
        case OFF:
          currentState = SLOW_BLINK;
          blinkInterval = 1000;
          Serial.println("状态: SLOW_BLINK (慢速闪烁)");
          break;
        case SLOW_BLINK:
          currentState = FAST_BLINK;
          blinkInterval = 200;
          Serial.println("状态: FAST_BLINK (快速闪烁)");
          break;
        case FAST_BLINK:
          currentState = OFF;
          digitalWrite(LED_PIN, LOW); // 关闭 LED
          Serial.println("状态: OFF (关闭)");
          break;
      }
      lastButtonPress = millis();
    }
  }

  // 根据当前状态执行相应操作（非阻塞方式）
  if (currentState != OFF) {
    if (millis() - lastToggleTime >= blinkInterval) {
      // 切换 LED 状态
      bool ledState = digitalRead(LED_PIN);
      digitalWrite(LED_PIN, !ledState);
      lastToggleTime = millis();
    }
  }
}