/*
 * Example 02: I2C 通信基础
 *
 * 这个程序演示 Arduino I2C 通信的基本用法。
 * I2C 使用 SDA (A4) 和 SCL (A5) 引脚。
 */

#include <Arduino.h>
#include <Wire.h>

// I2C 设备地址（示例地址）
const byte I2C_DEVICE_ADDRESS = 0x48; // 常见的 I2C 地址示例

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  // 初始化 I2C 通信（作为主设备）
  Wire.begin();

  Serial.println("=== I2C 通信基础演示 ===");
  Serial.println();
  Serial.println("I2C 引脚:");
  Serial.println("- SDA: A4");
  Serial.println("- SCL: A5");
  Serial.println();

  // 扫描 I2C 总线上的设备
  scanI2CDevices();
}

void loop() {
  static unsigned long lastScanTime = 0;
  const unsigned long SCAN_INTERVAL = 10000; // 每10秒扫描一次

  if (millis() - lastScanTime >= SCAN_INTERVAL) {
    Serial.println("重新扫描 I2C 设备...");
    scanI2CDevices();
    lastScanTime = millis();
    Serial.println();
  }

  // 模拟与 I2C 设备通信
  communicateWithI2CDevice();
  delay(2000);
}

void scanI2CDevices() {
  byte error, address;
  int nDevices = 0;

  Serial.println("扫描 I2C 设备...");

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("找到设备: 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
      nDevices++;
    }
    else if (error == 4) {
      Serial.print("未知错误 at 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
    }
  }

  if (nDevices == 0) {
    Serial.println("未找到 I2C 设备");
  }
  else {
    Serial.print("找到 ");
    Serial.print(nDevices);
    Serial.println(" 个设备");
  }
}

void communicateWithI2CDevice() {
  // 尝试与示例设备通信
  Wire.beginTransmission(I2C_DEVICE_ADDRESS);
  Wire.write(0x00); // 发送寄存器地址
  byte error = Wire.endTransmission();

  if (error == 0) {
    // 请求数据
    Wire.requestFrom(I2C_DEVICE_ADDRESS, 2); // 请求2字节数据

    if (Wire.available() >= 2) {
      byte data1 = Wire.read();
      byte data2 = Wire.read();
      Serial.print("从设备 0x");
      Serial.print(I2C_DEVICE_ADDRESS, HEX);
      Serial.print(" 读取数据: 0x");
      Serial.print(data1, HEX);
      Serial.print(", 0x");
      Serial.println(data2, HEX);
    }
  }
  else {
    Serial.print("无法与设备 0x");
    Serial.print(I2C_DEVICE_ADDRESS, HEX);
    Serial.println(" 通信");
  }
}