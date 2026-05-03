/*
 * Solution 01: 完整的通信协议系统
 *
 * 这个程序展示了完整的通信协议实现，
 * 包括串口、I2C 和 SPI 的综合应用。
 */

#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>

const int I2C_ADDRESS = 0x48;
const int SPI_SS_PIN = 10;

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }

  Wire.begin();
  SPI.begin();
  pinMode(SPI_SS_PIN, OUTPUT);
  digitalWrite(SPI_SS_PIN, HIGH);

  Serial.println("=== 完整的通信协议系统 ===");
}

void loop() {
  // 处理串口命令
  handleSerialCommands();

  // 与 I2C 设备通信
  communicateWithI2C();

  // 与 SPI 设备通信
  communicateWithSPI();

  delay(1000);
}

void handleSerialCommands() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "i2c_scan") {
      scanI2CDevices();
    } else if (cmd == "spi_test") {
      testSPICommunication();
    } else if (cmd.startsWith("i2c_write ")) {
      // 处理 I2C 写入命令
      Serial.println("I2C 写入命令处理");
    }
  }
}

void communicateWithI2C() {
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(0x00);
  if (Wire.endTransmission() == 0) {
    Wire.requestFrom(I2C_ADDRESS, 1);
    if (Wire.available()) {
      byte data = Wire.read();
      Serial.print("I2C 数据: 0x");
      Serial.println(data, HEX);
    }
  }
}

void communicateWithSPI() {
  digitalWrite(SPI_SS_PIN, LOW);
  byte response = SPI.transfer(0x55);
  digitalWrite(SPI_SS_PIN, HIGH);
  Serial.print("SPI 响应: 0x");
  Serial.println(response, HEX);
}

void scanI2CDevices() {
  Serial.println("扫描 I2C 设备...");
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("找到设备: 0x");
      Serial.println(addr, HEX);
    }
  }
}

void testSPICommunication() {
  Serial.println("测试 SPI 通信...");
  digitalWrite(SPI_SS_PIN, LOW);
  SPI.transfer(0xAA);
  SPI.transfer(0x55);
  digitalWrite(SPI_SS_PIN, HIGH);
  Serial.println("SPI 测试完成");
}