/*
 * Example 02: 模拟传感器读取（电位器/光敏电阻）
 *
 * 这个程序演示如何读取模拟传感器的数据，
 * 如电位器、光敏电阻、温度传感器等。
 */

#include <Arduino.h>

// 定义模拟输入引脚
const int POTENTIOMETER_PIN = A0;    // 电位器连接到 A0
const int LDR_PIN = A1;              // 光敏电阻连接到 A1

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 模拟传感器读取演示 ===");
  Serial.println();
  Serial.println("连接说明:");
  Serial.println("- 电位器: 中间引脚接 A0，两边分别接 5V 和 GND");
  Serial.println("- 光敏电阻: 与 10kΩ 电阻组成分压电路，接 A1");
  Serial.println();
}

void loop() {
  // 读取电位器值 (0-1023)
  int potValue = analogRead(POTENTIOMETER_PIN);

  // 读取光敏电阻值 (0-1023)
  int ldrValue = analogRead(LDR_PIN);

  // 转换为电压值 (0-5V)
  float potVoltage = potValue * (5.0 / 1023.0);
  float ldrVoltage = ldrValue * (5.0 / 1023.0);

  // 转换为百分比
  int potPercentage = map(potValue, 0, 1023, 0, 100);
  int ldrPercentage = map(ldrValue, 0, 1023, 0, 100);

  // 输出结果
  Serial.print("电位器: ");
  Serial.print(potValue);
  Serial.print(" (");
  Serial.print(potVoltage, 2);
  Serial.print("V, ");
  Serial.print(potPercentage);
  Serial.print("%) | ");

  Serial.print("光敏电阻: ");
  Serial.print(ldrValue);
  Serial.print(" (");
  Serial.print(ldrVoltage, 2);
  Serial.print("V, ");
  Serial.print(ldrPercentage);
  Serial.println("%)");

  // 控制 LED 亮度基于电位器值
  analogWrite(9, potValue / 4); // 映射 0-1023 到 0-255

  delay(500); // 短暂延迟避免串口输出过快
}