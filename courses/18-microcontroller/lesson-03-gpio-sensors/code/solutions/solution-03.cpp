/*
 * Example 03: 数字传感器接口（PIR运动传感器/超声波）
 *
 * 这个程序演示如何与数字传感器交互，
 * 包括 PIR 运动传感器和超声波距离传感器。
 */

#include <Arduino.h>

// 定义传感器引脚
const int PIR_PIN = 3;        // PIR 传感器输出接引脚 3
const int TRIG_PIN = 4;       // 超声波触发引脚
const int ECHO_PIN = 5;       // 超声波回响引脚

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 数字传感器接口演示 ===");
  Serial.println();
  Serial.println("传感器连接:");
  Serial.println("- PIR 运动传感器: 输出接引脚 3");
  Serial.println("- 超声波传感器: Trig接4, Echo接5");
  Serial.println();

  // 设置 PIR 引脚为输入
  pinMode(PIR_PIN, INPUT);

  // 设置超声波引脚
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // 给 PIR 传感器预热时间
  Serial.println("PIR 传感器预热中...");
  delay(2000);
  Serial.println("准备就绪!");
}

void loop() {
  // 读取 PIR 传感器状态
  int pirState = digitalRead(PIR_PIN);

  // 读取超声波距离
  long duration, distance;
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = (duration / 2) / 29.1; // 转换为厘米

  // 输出结果
  Serial.print("PIR 状态: ");
  Serial.print(pirState ? "检测到运动 🚶" : "无运动");
  Serial.print(" | 距离: ");
  if (distance >= 200 || distance <= 0) {
    Serial.print("超出范围");
  } else {
    Serial.print(distance);
    Serial.print(" cm");
  }
  Serial.println();

  // LED 指示
  if (pirState) {
    digitalWrite(13, HIGH); // 板载 LED 亮起表示检测到运动
  } else {
    digitalWrite(13, LOW);
  }

  delay(500);
}