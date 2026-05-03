/*
 * Solution 02: 完整的串口通信解决方案
 *
 * 这个程序提供了健壮的串口通信功能，包括：
 * - 多种协议格式支持（文本、传感器数据、命令帧）
 * - 自动协议检测
 * - 错误处理和校验和验证
 * - 实时数据流处理
 */

#include <Arduino.h>

// 定义缓冲区大小
const int BUFFER_SIZE = 128;
byte receiveBuffer[BUFFER_SIZE];
int bufferIndex = 0;

// 协议类型枚举
enum ProtocolType {
  PROTOCOL_UNKNOWN,
  PROTOCOL_TEXT,
  PROTOCOL_SENSOR_V1,
  PROTOCOL_COMMAND
};

// 函数声明
ProtocolType detectProtocol();
void handleTextFrame();
void handleSensorFrame();
void handleCommandFrame();
bool isValidASCII(const byte* data, int length);
bool validateChecksum(const byte* data, int length);

void setup() {
  // 初始化高速串口通信（115200 波特率）
  Serial.begin(115200);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 单片机串口通信完整解决方案 ===");
  Serial.println();

  // 发送启动消息
  Serial.println("系统启动中...");
  delay(500);

  Serial.println("支持的协议格式：");
  Serial.println("- 文本消息（以换行符结尾）");
  Serial.println("- 传感器数据 v1: [温度高][温度低][湿度高][湿度低][校验和] (5字节)");
  Serial.println("- 命令帧: [CMD_ID][LENGTH][DATA...][CHECKSUM]");
  Serial.println();
  Serial.println("请通过串口发送数据进行测试！");
}

void loop() {
  // 检查串口是否有可用数据
  if (Serial.available() > 0) {
    byte incomingByte = Serial.read();

    // 将字节添加到缓冲区
    if (bufferIndex < BUFFER_SIZE - 1) {
      receiveBuffer[bufferIndex] = incomingByte;
      bufferIndex++;

      // 尝试自动检测和处理帧
      ProtocolType protocol = detectProtocol();

      if (protocol != PROTOCOL_UNKNOWN) {
        switch (protocol) {
          case PROTOCOL_TEXT:
            handleTextFrame();
            break;
          case PROTOCOL_SENSOR_V1:
            handleSensorFrame();
            break;
          case PROTOCOL_COMMAND:
            handleCommandFrame();
            break;
        }
        // 重置缓冲区用于下一个帧
        bufferIndex = 0;
      }
      // 如果缓冲区满了但没有识别出协议，重置缓冲区
      else if (bufferIndex == BUFFER_SIZE - 1) {
        Serial.println("警告: 缓冲区满，重置");
        bufferIndex = 0;
      }
    }
  }
}

ProtocolType detectProtocol() {
  // 检查是否为文本帧（以换行符结尾）
  if (bufferIndex > 0 && (receiveBuffer[bufferIndex - 1] == '\n' || receiveBuffer[bufferIndex - 1] == '\r')) {
    // 检查是否为有效的ASCII文本
    if (isValidASCII(receiveBuffer, bufferIndex - 1)) {
      return PROTOCOL_TEXT;
    }
  }

  // 检查是否为传感器数据 v1 (固定5字节)
  if (bufferIndex == 5) {
    // 验证校验和
    if (validateChecksum(receiveBuffer, 4)) {
      return PROTOCOL_SENSOR_V1;
    }
  }

  // 检查是否为命令帧
  if (bufferIndex >= 3) {
    byte cmdId = receiveBuffer[0];
    byte length = receiveBuffer[1];
    // 命令帧总长度应为: 1(CMD_ID) + 1(LENGTH) + length(DATA) + 1(CHECKSUM)
    if (bufferIndex == length + 3) {
      // 验证校验和（排除最后的校验和字节）
      if (validateChecksum(receiveBuffer, bufferIndex - 1)) {
        return PROTOCOL_COMMAND;
      }
    }
  }

  return PROTOCOL_UNKNOWN;
}

bool isValidASCII(const byte* data, int length) {
  // 检查是否为可打印的ASCII字符（32-126）
  for (int i = 0; i < length; i++) {
    if (data[i] < 32 || data[i] > 126) {
      return false;
    }
  }
  return true;
}

bool validateChecksum(const byte* data, int length) {
  // 计算数据的校验和（简单求和）
  byte calculatedChecksum = 0;
  for (int i = 0; i < length; i++) {
    calculatedChecksum += data[i];
  }
  // 比较计算的校验和与接收到的校验和
  return calculatedChecksum == data[length]; // data[length] 是校验和字节
}

void handleTextFrame() {
  // 处理文本帧（移除换行符）
  if (bufferIndex > 0) {
    receiveBuffer[bufferIndex - 1] = '\0'; // 替换换行符
  }
  String textMessage = String((char*)receiveBuffer);
  Serial.print("[TEXT] 接收: ");
  Serial.println(textMessage);
}

void handleSensorFrame() {
  // 处理传感器数据 v1: [温度高][温度低][湿度高][湿度低][校验和]
  int temperatureRaw = (receiveBuffer[0] << 8) | receiveBuffer[1];
  int humidityRaw = (receiveBuffer[2] << 8) | receiveBuffer[3];

  float temperature = temperatureRaw / 10.0;
  float humidity = humidityRaw / 10.0;

  Serial.print("[SENSOR] 温度=");
  Serial.print(temperature, 1);
  Serial.print("°C, 湿度=");
  Serial.print(humidity, 1);
  Serial.println("%");
}

void handleCommandFrame() {
  // 处理命令帧: [CMD_ID][LENGTH][DATA...][CHECKSUM]
  byte cmdId = receiveBuffer[0];
  byte length = receiveBuffer[1];

  Serial.print("[CMD] ID=0x");
  Serial.print(cmdId, HEX);
  Serial.print(", 长度=");
  Serial.print(length);

  if (length > 0) {
    Serial.print(", 数据=");
    for (int i = 0; i < length; i++) {
      Serial.print("0x");
      Serial.print(receiveBuffer[2 + i], HEX);
      Serial.print(" ");
    }
  }
  Serial.println();

  // 执行简单的命令响应
  if (cmdId == 0x10) { // 配置命令
    Serial.println("[CMD] 执行: 应用配置");
  }
  else if (cmdId == 0x01) { // 控制命令
    digitalWrite(13, (receiveBuffer[2] > 0) ? HIGH : LOW);
    Serial.println("[CMD] 执行: 控制LED");
  }
}