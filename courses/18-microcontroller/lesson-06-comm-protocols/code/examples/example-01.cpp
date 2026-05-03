/*
 * Example 01: 串口通信基础
 *
 * 这个程序演示 Arduino 串口通信的基本用法，
 * 包括发送和接收数据。
 */

#include <Arduino.h>

void setup() {
  // 初始化串口通信 (9600 波特率)
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接（仅适用于 Leonardo、Micro 等）
  }

  Serial.println("=== 串口通信基础演示 ===");
  Serial.println();
  Serial.println("支持的命令:");
  Serial.println("- 'led on': 打开板载 LED");
  Serial.println("- 'led off': 关闭板载 LED");
  Serial.println("- 'status': 显示系统状态");
  Serial.println("- 'echo [text]': 回显文本");
  Serial.println();
}

void loop() {
  // 检查串口是否有可用数据
  if (Serial.available() > 0) {
    // 读取一行数据
    String inputString = Serial.readStringUntil('\n');
    inputString.trim(); // 移除首尾空白字符

    // 处理命令
    if (inputString.equalsIgnoreCase("led on")) {
      digitalWrite(13, HIGH);
      Serial.println("✅ LED 已打开");
    }
    else if (inputString.equalsIgnoreCase("led off")) {
      digitalWrite(13, LOW);
      Serial.println("✅ LED 已关闭");
    }
    else if (inputString.equalsIgnoreCase("status")) {
      Serial.print("系统运行时间: ");
      Serial.print(millis() / 1000);
      Serial.println(" 秒");
      Serial.print("LED 状态: ");
      Serial.println(digitalRead(13) ? "ON" : "OFF");
    }
    else if (inputString.startsWith("echo ")) {
      String echoText = inputString.substring(5);
      Serial.print("回显: ");
      Serial.println(echoText);
    }
    else {
      Serial.println("❌ 未知命令。支持: led on/off, status, echo [text]");
    }

    Serial.println(); // 空行分隔
  }
}