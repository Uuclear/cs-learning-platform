/*
 * Example 01: 单片机 GPIO 高低电平输出
 *
 * 这个 Arduino 程序演示了单片机如何控制 GPIO 引脚的高低电平。
 * 在真实的单片机中，这通常用于控制 LED、继电器或其他数字设备。
 */

// 包含 Arduino 核心库
#include <Arduino.h>

// 定义引脚常量
const int LED_PIN = 13;    // Arduino Uno 的内置 LED 通常在引脚 13
const int BUTTON_PIN = 2;  // 按钮连接到引脚 2

void setup() {
  // 初始化串口通信（用于调试输出）
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接（仅适用于 Leonardo、Micro 等）
  }

  Serial.println("=== 单片机 GPIO 演示 ===");
  Serial.println();

  // 设置 LED 引脚为输出模式
  pinMode(LED_PIN, OUTPUT);
  Serial.println("LED 引脚设置为 OUTPUT 模式");

  // 设置按钮引脚为输入模式，启用内部上拉电阻
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("按钮引脚设置为 INPUT_PULLUP 模式");
  Serial.println();
}

void loop() {
  static bool ledState = false;
  static unsigned long lastBlinkTime = 0;
  static unsigned long lastButtonCheckTime = 0;
  const unsigned long BLINK_INTERVAL = 500;    // 500ms 闪烁间隔
  const unsigned long BUTTON_CHECK_INTERVAL = 1000; // 1s 按钮检查间隔

  unsigned long currentTime = millis();

  // LED 闪烁演示（前 5 秒）
  if (currentTime < 5000) {
    if (currentTime - lastBlinkTime >= BLINK_INTERVAL) {
      ledState = !ledState;
      digitalWrite(LED_PIN, ledState);

      if (ledState) {
        Serial.println("GPIO13: 设置为 高电平 (5V)");
      } else {
        Serial.println("GPIO13: 设置为 低电平 (0V)");
      }

      lastBlinkTime = currentTime;
    }
  }
  // 按钮输入模拟（5秒后）
  else if (currentTime >= 5000 && currentTime < 8000) {
    if (currentTime - lastButtonCheckTime >= BUTTON_CHECK_INTERVAL) {
      // 读取按钮状态（由于使用内部上拉，按下时为 LOW）
      int buttonState = digitalRead(BUTTON_PIN);
      String status = (buttonState == LOW) ? "按下" : "未按下";
      Serial.println("按钮状态: " + status);

      lastButtonCheckTime = currentTime;
    }
  }
  // 演示完成
  else if (currentTime >= 8000 && currentTime < 8100) {
    Serial.println();
    Serial.println("演示完成!");
  }
}