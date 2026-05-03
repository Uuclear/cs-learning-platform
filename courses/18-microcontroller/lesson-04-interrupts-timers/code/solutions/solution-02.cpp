/*
 * Example 01: 中断与轮询对比演示
 *
 * 这个程序展示了中断驱动和轮询方式在处理按钮事件时的差异。
 * 使用外部中断可以显著降低CPU使用率并提高响应性。
 */

#include <Arduino.h>

// 定义引脚
const int BUTTON_POLL_PIN = 4;    // 轮询方式的按钮（引脚4）
const int BUTTON_INT_PIN = 2;     // 中断方式的按钮（引脚2，支持外部中断）

// 全局变量用于中断
volatile bool buttonPressed = false;
volatile unsigned long interruptCount = 0;

// 计数器用于轮询
unsigned long pollingCount = 0;
unsigned long lastPollTime = 0;

// 防抖参数
const unsigned long DEBOUNCE_DELAY = 50;

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 中断 vs 轮询对比演示 ===");
  Serial.println();
  Serial.println("连接说明:");
  Serial.println("- 轮询按钮: 连接到引脚 4");
  Serial.println("- 中断按钮: 连接到引脚 2 (支持外部中断)");
  Serial.println();
  Serial.println("按下按钮观察两种方式的响应差异");

  // 设置轮询按钮引脚（内部上拉）
  pinMode(BUTTON_POLL_PIN, INPUT_PULLUP);

  // 设置中断按钮引脚（内部上拉）
  pinMode(BUTTON_INT_PIN, INPUT_PULLUP);

  // 启用外部中断（下降沿触发）
  attachInterrupt(digitalPinToInterrupt(BUTTON_INT_PIN), buttonISR, FALLING);
}

// 中断服务程序 (ISR)
void buttonISR() {
  // ISR 必须尽可能快！只设置标志位
  static unsigned long lastInterruptTime = 0;
  unsigned long currentTime = millis();

  // 简单软件防抖（在ISR中要小心使用millis()）
  if (currentTime - lastInterruptTime > DEBOUNCE_DELAY) {
    buttonPressed = true;
    interruptCount++;
    lastInterruptTime = currentTime;
  }
}

void loop() {
  // === 轮询方式处理 ===
  static int lastPollState = HIGH;
  static unsigned long lastDebounceTime = 0;

  int pollReading = digitalRead(BUTTON_POLL_PIN);

  if (pollReading != lastPollState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    if (pollReading != digitalRead(BUTTON_POLL_PIN)) {
      // 按钮状态确认变化
      if (pollReading == LOW) {
        Serial.print("[轮询] 按钮按下! ");
        Serial.print("轮询计数: ");
        Serial.println(pollingCount);
      }
    }
  }
  lastPollState = pollReading;
  pollingCount++;

  // === 中断方式处理 ===
  if (buttonPressed) {
    Serial.print("[中断] 按钮按下! ");
    Serial.print("中断计数: ");
    Serial.println(interruptCount);
    buttonPressed = false; // 清除标志位
  }

  // 显示统计信息（每5秒）
  if (millis() - lastPollTime >= 5000) {
    Serial.println();
    Serial.print("统计信息 (5秒内):");
    Serial.print(" 轮询次数=");
    Serial.print(pollingCount);
    Serial.print(", 中断次数=");
    Serial.println(interruptCount);
    Serial.println();

    // 重置计数器
    pollingCount = 0;
    lastPollTime = millis();
  }

  // 主程序可以做其他有用的工作
  // 这里模拟一些计算工作
  static unsigned long lastWorkTime = 0;
  if (millis() - lastWorkTime >= 100) {
    // 执行一些简单的计算
    int workResult = 0;
    for (int i = 0; i < 100; i++) {
      workResult += i * i;
    }
    lastWorkTime = millis();
  }
}