/*
 * Example 02: 串口通信数据帧解析
 *
 * 这个 Arduino 程序演示了单片机如何通过串口 (UART) 接收和解析数据帧。
 * 在嵌入式系统中，串口通信是调试和设备间通信的重要方式。
 */

#include <Arduino.h>

// 定义缓冲区大小
const int BUFFER_SIZE = 64;
byte receiveBuffer[BUFFER_SIZE];
int bufferIndex = 0;

// 函数声明
void parseTextFrame();
void parseSensorFrame();
void parseCommandFrame();

void setup() {
  // 初始化串口通信（9600 波特率）
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 单片机串口通信演示 ===");
  Serial.println();

  // 发送示例数据用于演示
  Serial.println("1. 发送简单的文本消息:");
  Serial.println("Hello, Microcontroller!");
  delay(1000);

  Serial.println();
  Serial.println("2. 发送传感器数据模拟:");
  // 发送模拟传感器数据（温度: 25.5°C, 湿度: 60.0%）
  // 格式: [温度高字节][温度低字节][湿度高字节][湿度低字节][校验和]
  int temperature = 255; // 25.5 * 10
  int humidity = 600;    // 60.0 * 10
  byte checksum = (temperature + humidity) & 0xFF;

  Serial.write((byte)(temperature >> 8));     // 温度高字节
  Serial.write((byte)(temperature & 0xFF));   // 温度低字节
  Serial.write((byte)(humidity >> 8));        // 湿度高字节
  Serial.write((byte)(humidity & 0xFF));      // 湿度低字节
  Serial.write(checksum);                     // 校验和

  delay(1000);

  Serial.println();
  Serial.println("3. 发送命令帧:");
  // 发送控制命令: [命令ID][参数][校验和]
  byte commandId = 0x01;  // 开灯命令
  byte parameter = 0xFF;  // 参数（全亮）
  byte cmdChecksum = (commandId + parameter) & 0xFF;

  Serial.write(commandId);
  Serial.write(parameter);
  Serial.write(cmdChecksum);

  Serial.println();
  Serial.println("请在串口监视器中发送数据来测试解析功能！");
  Serial.println("支持的数据格式：");
  Serial.println("- 文本消息（以换行符结尾）");
  Serial.println("- 5字节传感器数据帧");
  Serial.println("- 3字节命令帧");
  Serial.println();
}

void loop() {
  // 检查串口是否有可用数据
  if (Serial.available() > 0) {
    byte incomingByte = Serial.read();

    // 将字节添加到缓冲区
    if (bufferIndex < BUFFER_SIZE - 1) {
      receiveBuffer[bufferIndex] = incomingByte;
      bufferIndex++;

      // 检查是否接收到完整的帧
      if (incomingByte == '\n' || incomingByte == '\r') {
        // 文本帧（以换行符结尾）
        receiveBuffer[bufferIndex - 1] = '\0'; // 替换换行符为字符串结束符
        parseTextFrame();
        bufferIndex = 0; // 重置缓冲区
      }
      else if (bufferIndex == 5) {
        // 5字节传感器数据帧
        parseSensorFrame();
        bufferIndex = 0;
      }
      else if (bufferIndex == 3) {
        // 3字节命令帧
        parseCommandFrame();
        bufferIndex = 0;
      }
    }
    else {
      // 缓冲区已满，重置
      bufferIndex = 0;
      Serial.println("错误: 缓冲区溢出");
    }
  }
}

void parseTextFrame() {
  // 解析文本帧
  String textMessage = String((char*)receiveBuffer);
  Serial.print("接收到文本: ");
  Serial.println(textMessage);
}

void parseSensorFrame() {
  // 解析传感器数据帧: [温度(2字节)][湿度(2字节)][校验和(1字节)]
  int temperatureRaw = (receiveBuffer[0] << 8) | receiveBuffer[1];
  int humidityRaw = (receiveBuffer[2] << 8) | receiveBuffer[3];
  byte receivedChecksum = receiveBuffer[4];

  // 计算校验和
  byte calculatedChecksum = (temperatureRaw + humidityRaw) & 0xFF;

  if (calculatedChecksum == receivedChecksum) {
    float temperature = temperatureRaw / 10.0;
    float humidity = humidityRaw / 10.0;
    Serial.print("传感器数据: 温度=");
    Serial.print(temperature, 1);
    Serial.print("°C, 湿度=");
    Serial.print(humidity, 1);
    Serial.println("%");
  }
  else {
    Serial.println("错误: 传感器数据帧校验和错误");
  }
}

void parseCommandFrame() {
  // 解析命令帧: [命令ID][参数][校验和]
  byte commandId = receiveBuffer[0];
  byte parameter = receiveBuffer[1];
  byte receivedChecksum = receiveBuffer[2];

  // 计算校验和
  byte calculatedChecksum = (commandId + parameter) & 0xFF;

  if (calculatedChecksum == receivedChecksum) {
    Serial.print("接收到有效命令: ID=0x");
    Serial.print(commandId, HEX);
    Serial.print(", 参数=0x");
    Serial.println(parameter, HEX);

    // 执行命令（示例）
    if (commandId == 0x01) {
      digitalWrite(13, (parameter > 0) ? HIGH : LOW);
      Serial.println("执行: 控制LED");
    }
  }
  else {
    Serial.println("错误: 命令帧校验和错误");
  }
}