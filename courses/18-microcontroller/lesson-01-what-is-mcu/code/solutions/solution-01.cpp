/*
 * Solution 01: 完整的 GPIO 功能演示
 *
 * 这个程序演示了单片机 GPIO 的完整功能，包括：
 * - 基本数字输入/输出
 * - 内部上拉/下拉电阻
 * - 外部中断
 * - PWM 输出
 */

#include <Arduino.h>

// 定义引脚常量
const int LED_PIN = 13;      // LED 连接到引脚 13
const int BUTTON_PIN = 2;    // 按钮连接到引脚 2 (支持外部中断)

// 全局变量用于中断处理
volatile bool buttonPressed = false;

// 中断服务函数 (ISR)
void buttonInterruptHandler() {
  // 在 ISR 中只做最简单的操作
  buttonPressed = true;
}

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 单片机 GPIO 完整功能演示 ===");
  Serial.println();

  // 1. LED 控制设置
  pinMode(LED_PIN, OUTPUT);
  Serial.println("1. LED 控制初始化完成");

  // 2. 按钮输入设置（内部上拉电阻）
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("2. 按钮输入设置为 INPUT_PULLUP 模式");

  // 3. 启用外部中断（下降沿触发）
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonInterruptHandler, FALLING);
  Serial.println("3. 外部中断已启用 (FALLING edge)");
  Serial.println();
}

void loop() {
  static unsigned long lastBlinkTime = 0;
  static unsigned long lastPWMTime = 0;
  static unsigned long lastButtonCheckTime = 0;
  static int pwmStep = 0;
  static bool demoPhase1Complete = false;
  static bool demoPhase2Complete = false;
  static bool demoPhase3Complete = false;

  unsigned long currentTime = millis();

  // 阶段1: 基本 LED 闪烁 (前 3 秒)
  if (!demoPhase1Complete && currentTime < 3000) {
    if (currentTime - lastBlinkTime >= 300) {
      digitalWrite(LED_PIN, !digitalRead(LED_PIN));
      lastBlinkTime = currentTime;
    }
  }
  else if (!demoPhase1Complete) {
    demoPhase1Complete = true;
    digitalWrite(LED_PIN, LOW); // 确保LED熄灭
    Serial.println("1. 基本 LED 闪烁完成");
  }

  // 阶段2: PWM LED 亮度控制 (3-7秒)
  if (demoPhase1Complete && !demoPhase2Complete && currentTime >= 3000 && currentTime < 7000) {
    if (currentTime - lastPWMTime >= 500) {
      // 循环不同的PWM值：25%, 50%, 75%
      int pwmValues[] = {64, 128, 192}; // 对应 25%, 50%, 75%
      analogWrite(LED_PIN, pwmValues[pwmStep % 3]);

      Serial.print("2. PWM 亮度控制: ");
      Serial.print((pwmStep % 3 + 1) * 25);
      Serial.println("%");

      pwmStep++;
      lastPWMTime = currentTime;
    }
  }
  else if (demoPhase1Complete && !demoPhase2Complete && currentTime >= 7000) {
    demoPhase2Complete = true;
    analogWrite(LED_PIN, 0); // 关闭PWM
    Serial.println("2. PWM LED 亮度控制完成");
  }

  // 阶段3: 按钮输入与中断 (7-12秒)
  if (demoPhase2Complete && !demoPhase3Complete && currentTime >= 7000 && currentTime < 12000) {
    if (currentTime - lastButtonCheckTime >= 500) {
      // 读取按钮状态（使用内部上拉，按下时为LOW）
      int buttonState = digitalRead(BUTTON_PIN);
      String status = (buttonState == LOW) ? "按下" : "未按下";
      Serial.print("3. 按钮状态: ");
      Serial.println(status);

      lastButtonCheckTime = currentTime;
    }

    // 检查中断标志
    if (buttonPressed) {
      Serial.println("3. 按钮中断触发! 按钮被按下");
      buttonPressed = false; // 清除标志

      // 快速闪烁LED确认中断
      for (int i = 0; i < 3; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(100);
        digitalWrite(LED_PIN, LOW);
        delay(100);
      }
    }
  }
  else if (demoPhase2Complete && !demoPhase3Complete && currentTime >= 12000) {
    demoPhase3Complete = true;
    Serial.println("3. 按钮输入与中断演示完成");
  }

  // 演示完成
  if (demoPhase3Complete && currentTime >= 12000 && currentTime < 12100) {
    Serial.println();
    Serial.println("=== 所有演示完成! ===");
  }
}