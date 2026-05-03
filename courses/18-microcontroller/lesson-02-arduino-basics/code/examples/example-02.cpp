/*
 * Example 02: Arduino Blink 程序逻辑演示
 *
 * 这个程序展示了 Arduino Blink 程序的真实执行逻辑，
 * 包括标准闪烁模式和自定义闪烁模式。
 */

#include <Arduino.h>

// 定义引脚常量
const int STANDARD_LED_PIN = 13;  // 标准 LED 引脚 (板载 LED)
const int CUSTOM_LED_PIN = 8;     // 自定义 LED 引脚

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== Arduino Blink 程序逻辑演示 ===");
  Serial.println();
  Serial.println("这个程序同时演示两种闪烁模式:");
  Serial.println("- 标准模式: 引脚 13 (1秒亮/1秒灭)");
  Serial.println("- 自定义模式: 引脚 8 (500ms亮/1500ms灭)");
  Serial.println();

  // 初始化 LED 引脚为输出
  pinMode(STANDARD_LED_PIN, OUTPUT);
  pinMode(CUSTOM_LED_PIN, OUTPUT);
}

void loop() {
  static unsigned long lastStandardToggle = 0;
  static unsigned long lastCustomToggle = 0;
  static bool standardLedState = false;
  static bool customLedState = false;
  static bool customPhase = true; // true = 亮相, false = 灭相

  unsigned long currentTime = millis();

  // 标准 Blink 模式 (1秒间隔)
  if (currentTime - lastStandardToggle >= 1000) {
    standardLedState = !standardLedState;
    digitalWrite(STANDARD_LED_PIN, standardLedState ? HIGH : LOW);

    // 输出调试信息（每10秒一次，避免串口过载）
    static unsigned long lastDebugTime = 0;
    if (currentTime - lastDebugTime >= 10000) {
      Serial.print("[标准模式] 引脚 ");
      Serial.print(STANDARD_LED_PIN);
      Serial.print(": ");
      Serial.println(standardLedState ? "HIGH 💡" : "LOW 🌑");
      lastDebugTime = currentTime;
    }

    lastStandardToggle = currentTime;
  }

  // 自定义闪烁模式 (500ms亮/1500ms灭)
  if (customPhase) {
    // 亮相 (500ms)
    if (!customLedState) {
      digitalWrite(CUSTOM_LED_PIN, HIGH);
      customLedState = true;
    }
    if (currentTime - lastCustomToggle >= 500) {
      customPhase = false;
      lastCustomToggle = currentTime;
    }
  } else {
    // 灭相 (1500ms)
    if (customLedState) {
      digitalWrite(CUSTOM_LED_PIN, LOW);
      customLedState = false;
    }
    if (currentTime - lastCustomToggle >= 1500) {
      customPhase = true;
      lastCustomToggle = currentTime;
    }
  }
}