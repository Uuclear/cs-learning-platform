/*
 * Example 03: SPI 通信基础
 *
 * 这个程序演示 Arduino SPI 通信的基本用法。
 * SPI 使用 MOSI (11), MISO (12), SCK (13), SS (10) 引脚。
 */

#include <Arduino.h>
#include <SPI.h>

// SPI 从设备选择引脚
const int SLAVE_SELECT_PIN = 10;

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  // 初始化 SPI 通信（作为主设备）
  SPI.begin();

  // 设置从设备选择引脚为输出
  pinMode(SLAVE_SELECT_PIN, OUTPUT);
  digitalWrite(SLAVE_SELECT_PIN, HIGH); // 默认不选择从设备

  Serial.println("=== SPI 通信基础演示 ===");
  Serial.println();
  Serial.println("SPI 引脚:");
  Serial.println("- MOSI: 11 (主出从入)");
  Serial.println("- MISO: 12 (主入从出)");
  Serial.println("- SCK: 13 (时钟)");
  Serial.println("- SS: 10 (从设备选择)");
  Serial.println();

  // 显示 SPI 配置
  Serial.println("SPI 配置:");
  Serial.println("- 数据模式: SPI_MODE0");
  Serial.println("- 时钟分频: SPI_CLOCK_DIV4 (4MHz)");
  Serial.println("- 数据顺序: MSBFIRST");
  Serial.println();
}

void loop() {
  static int demoStep = 0;
  static unsigned long lastDemoTime = 0;
  const unsigned long DEMO_INTERVAL = 3000; // 每3秒切换一次演示

  if (millis() - lastDemoTime >= DEMO_INTERVAL) {
    switch (demoStep % 3) {
      case 0:
        // 发送单字节数据
        sendSPIByte(0xAA);
        Serial.println("演示 1: 发送单字节 0xAA");
        break;

      case 1:
        // 发送多字节数据
        sendSPIMultiByte();
        Serial.println("演示 2: 发送多字节数据");
        break;

      case 2:
        // 读取从设备数据
        readSPIFromSlave();
        Serial.println("演示 3: 从从设备读取数据");
        break;
    }

    demoStep++;
    lastDemoTime = millis();
    Serial.println();
  }
}

void sendSPIByte(byte data) {
  // 选择从设备
  digitalWrite(SLAVE_SELECT_PIN, LOW);

  // 发送数据
  SPI.transfer(data);

  // 取消选择从设备
  digitalWrite(SLAVE_SELECT_PIN, HIGH);
}

void sendSPIMultiByte() {
  byte data[] = {0x01, 0x02, 0x03, 0x04};

  // 选择从设备
  digitalWrite(SLAVE_SELECT_PIN, LOW);

  // 发送多个字节
  for (int i = 0; i < 4; i++) {
    SPI.transfer(data[i]);
  }

  // 取消选择从设备
  digitalWrite(SLAVE_SELECT_PIN, HIGH);
}

void readSPIFromSlave() {
  // 选择从设备
  digitalWrite(SLAVE_SELECT_PIN, LOW);

  // 发送虚拟字节以读取响应
  byte response = SPI.transfer(0x00);

  // 取消选择从设备
  digitalWrite(SLAVE_SELECT_PIN, HIGH);

  Serial.print("从设备响应: 0x");
  Serial.println(response, HEX);
}