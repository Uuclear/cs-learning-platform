/*
 * Example 02: 定时器和非阻塞延时
 *
 * 这个程序演示了如何使用 millis() 实现非阻塞延时，
 * 允许同时处理多个任务而不会阻塞程序执行。
 */

#include <Arduino.h>

// 定义任务间隔
const unsigned long BLINK_INTERVAL = 1000;    // LED 闪烁间隔 1秒
const unsigned long SERIAL_INTERVAL = 2000;   // 串口输出间隔 2秒
const unsigned long SENSOR_INTERVAL = 500;    // 传感器读取间隔 500ms

// 状态变量
bool ledState = false;
unsigned long lastBlinkTime = 0;
unsigned long lastSerialTime = 0;
unsigned long lastSensorTime = 0;

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 定时器和非阻塞延时演示 ===");
  Serial.println();
  Serial.println("这个程序同时执行三个独立任务:");
  Serial.println("- LED 闪烁 (1秒间隔)");
  Serial.println("- 串口状态输出 (2秒间隔)");
  Serial.println("- 模拟传感器读取 (500ms间隔)");
  Serial.println();

  // 初始化 LED 引脚
  pinMode(13, OUTPUT);
}

void loop() {
  unsigned long currentTime = millis();

  // 任务1: LED 闪烁
  if (currentTime - lastBlinkTime >= BLINK_INTERVAL) {
    ledState = !ledState;
    digitalWrite(13, ledState ? HIGH : LOW);
    lastBlinkTime = currentTime;
  }

  // 任务2: 串口状态输出
  if (currentTime - lastSerialTime >= SERIAL_INTERVAL) {
    Serial.print("系统运行时间: ");
    Serial.print(currentTime / 1000);
    Serial.println(" 秒");
    Serial.print("LED 状态: ");
    Serial.println(ledState ? "ON" : "OFF");
    Serial.println();
    lastSerialTime = currentTime;
  }

  // 任务3: 模拟传感器读取
  if (currentTime - lastSensorTime >= SENSOR_INTERVAL) {
    // 模拟读取传感器数据
    int sensorValue = analogRead(A0);
    float voltage = sensorValue * (5.0 / 1023.0);

    Serial.print("传感器读数: ");
    Serial.print(sensorValue);
    Serial.print(" (");
    Serial.print(voltage, 2);
    Serial.println("V)");

    lastSensorTime = currentTime;
  }

  // 主循环可以继续执行其他代码
  // 这里没有 delay()，所以程序不会被阻塞
}