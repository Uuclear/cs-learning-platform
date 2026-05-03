/*
 * Solution 01: LED 限流电阻完整演示
 *
 * 这个程序演示了不同 LED 类型的限流电阻计算和实际效果，
 * 包括安全电流检查和多 LED 配置。
 */

#include <Arduino.h>

// 定义 LED 引脚（使用 PWM 引脚以支持亮度控制）
const int RED_LED_PIN = 9;
const int GREEN_LED_PIN = 10;
const int BLUE_LED_PIN = 11;

// LED 参数结构体
struct LEDParams {
  const char* name;
  float forwardVoltage; // 正向电压降 (V)
  float maxCurrent;     // 最大电流 (mA)
  int pin;              // 连接的引脚
};

// 不同 LED 的典型参数
LEDParams ledTypes[] = {
  {"红色 LED", 2.0, 25.0, RED_LED_PIN},
  {"绿色 LED", 2.2, 25.0, GREEN_LED_PIN},
  {"蓝色 LED", 3.2, 25.0, BLUE_LED_PIN}
};

const int NUM_LED_TYPES = 3;

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== LED 限流电阻完整演示 ===");
  Serial.println();
  Serial.println("电源电压: 5.0V (Arduino UNO)");
  Serial.println();
  Serial.println("LED 参数:");

  for (int i = 0; i < NUM_LED_TYPES; i++) {
    Serial.print("- ");
    Serial.print(ledTypes[i].name);
    Serial.print(": Vf=");
    Serial.print(ledTypes[i].forwardVoltage, 1);
    Serial.print("V, Imax=");
    Serial.print(ledTypes[i].maxCurrent, 0);
    Serial.println("mA");
  }

  Serial.println();
  Serial.println("限流电阻计算公式: R = (Vcc - Vf) / I");
  Serial.println("其中 Vcc = 5.0V (Arduino 电源)");
  Serial.println();

  // 初始化 LED 引脚
  for (int i = 0; i < NUM_LED_TYPES; i++) {
    pinMode(ledTypes[i].pin, OUTPUT);
    digitalWrite(ledTypes[i].pin, LOW);
  }
}

void loop() {
  static int demoStep = 0;
  static unsigned long lastDemoTime = 0;
  const unsigned long DEMO_INTERVAL = 4000; // 每4秒切换一次演示

  if (millis() - lastDemoTime >= DEMO_INTERVAL) {
    // 关闭所有 LED
    for (int i = 0; i < NUM_LED_TYPES; i++) {
      analogWrite(ledTypes[i].pin, 0);
    }

    switch (demoStep % 4) {
      case 0:
        demoSafeCurrent();
        break;
      case 1:
        demoHighCurrent();
        break;
      case 2:
        demoLowCurrent();
        break;
      case 3:
        demoAllTogether();
        break;
    }

    demoStep++;
    lastDemoTime = millis();
  }
}

void demoSafeCurrent() {
  Serial.println("演示 1: 安全电流范围 (10-20mA)");

  for (int i = 0; i < NUM_LED_TYPES; i++) {
    // 计算安全电流下的 PWM 值
    // 假设使用 220Ω 电阻，计算实际电流
    float actualCurrent = (5.0 - ledTypes[i].forwardVoltage) / 220.0 * 1000.0; // mA
    // 映射到 PWM 值 (0-255)，假设最大亮度对应 20mA
    int pwmValue = constrain(map(actualCurrent, 0, 20, 0, 255), 0, 255);

    analogWrite(ledTypes[i].pin, pwmValue);

    Serial.print("  ");
    Serial.print(ledTypes[i].name);
    Serial.print(": ");
    Serial.print(actualCurrent, 1);
    Serial.print("mA (R=220Ω) → PWM=");
    Serial.println(pwmValue);
  }
  Serial.println();
}

void demoHighCurrent() {
  Serial.println("演示 2: 高电流警告 (>25mA)");

  for (int i = 0; i < NUM_LED_TYPES; i++) {
    // 模拟使用过小电阻 (100Ω) 导致高电流
    float actualCurrent = (5.0 - ledTypes[i].forwardVoltage) / 100.0 * 1000.0;
    int pwmValue = constrain(map(actualCurrent, 0, 50, 0, 255), 0, 255);

    analogWrite(ledTypes[i].pin, pwmValue);

    Serial.print("  ");
    Serial.print(ledTypes[i].name);
    Serial.print(": ");
    Serial.print(actualCurrent, 1);
    Serial.print("mA (R=100Ω) → ");

    if (actualCurrent > ledTypes[i].maxCurrent) {
      Serial.print("⚠️ 超过最大电流!");
    }
    Serial.println();
  }
  Serial.println();
}

void demoLowCurrent() {
  Serial.println("演示 3: 低电流效果 (<5mA)");

  for (int i = 0; i < NUM_LED_TYPES; i++) {
    // 模拟使用过大电阻 (1kΩ) 导致低电流
    float actualCurrent = (5.0 - ledTypes[i].forwardVoltage) / 1000.0 * 1000.0;
    int pwmValue = constrain(map(actualCurrent, 0, 10, 0, 255), 0, 255);

    analogWrite(ledTypes[i].pin, pwmValue);

    Serial.print("  ");
    Serial.print(ledTypes[i].name);
    Serial.print(": ");
    Serial.print(actualCurrent, 1);
    Serial.print("mA (R=1kΩ) → ");

    if (actualCurrent < 5.0) {
      Serial.print("💡 可能不够亮");
    }
    Serial.println();
  }
  Serial.println();
}

void demoAllTogether() {
  Serial.println("演示 4: 多 LED 串联/并联考虑");

  // 红色 LED - 串联配置模拟
  float seriesCurrent = (5.0 - 2.0 - 2.0) / 100.0 * 1000.0; // 两个红色 LED 串联
  int redPWM = constrain(map(seriesCurrent, 0, 20, 0, 255), 0, 255);
  analogWrite(RED_LED_PIN, redPWM);

  // 绿色 LED - 并联配置模拟
  float parallelCurrent = (5.0 - 2.2) / 220.0 * 1000.0 * 2; // 两个绿色 LED 并联
  int greenPWM = constrain(map(parallelCurrent, 0, 40, 0, 255), 0, 255);
  analogWrite(GREEN_LED_PIN, greenPWM);

  // 蓝色 LED - 单独配置
  float singleCurrent = (5.0 - 3.2) / 180.0 * 1000.0;
  int bluePWM = constrain(map(singleCurrent, 0, 20, 0, 255), 0, 255);
  analogWrite(BLUE_LED_PIN, bluePWM);

  Serial.print("  红色 (串联): ");
  Serial.print(seriesCurrent, 1);
  Serial.println("mA");
  Serial.print("  绿色 (并联): ");
  Serial.print(parallelCurrent, 1);
  Serial.println("mA");
  Serial.print("  蓝色 (单独): ");
  Serial.print(singleCurrent, 1);
  Serial.println("mA");
  Serial.println();
}