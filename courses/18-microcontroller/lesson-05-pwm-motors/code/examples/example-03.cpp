/*
 * Example 03: 舵机 PWM 控制
 *
 * 这个程序演示如何使用 PWM 控制舵机的角度。
 * 舵机通常需要 50Hz 的 PWM 信号（20ms 周期），
 * 脉冲宽度在 1-2ms 之间对应 0-180 度。
 */

#include <Arduino.h>

// 定义舵机控制引脚
const int SERVO_PIN = 6;

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 舵机 PWM 控制演示 ===");
  Serial.println();
  Serial.println("舵机角度范围: 0-180 度");
  Serial.println("PWM 脉冲宽度: 1ms (0°) - 2ms (180°)");
  Serial.println();

  // 设置舵机引脚为输出
  pinMode(SERVO_PIN, OUTPUT);

  // 初始位置：90度（中间位置）
  setServoAngle(90);
}

void loop() {
  static int demoStep = 0;
  static unsigned long lastDemoTime = 0;
  const unsigned long DEMO_INTERVAL = 2000; // 每2秒切换一次演示

  if (millis() - lastDemoTime >= DEMO_INTERVAL) {
    switch (demoStep % 4) {
      case 0:
        setServoAngle(0);
        Serial.println("演示 1: 舵机 0° (最左)");
        break;

      case 1:
        setServoAngle(90);
        Serial.println("演示 2: 舵机 90° (中间)");
        break;

      case 2:
        setServoAngle(180);
        Serial.println("演示 3: 舵机 180° (最右)");
        break;

      case 3:
        // 扫描运动
        scanServo();
        Serial.println("演示 4: 舵机扫描运动");
        break;
    }

    demoStep++;
    lastDemoTime = millis();
    Serial.println();
  }
}

void setServoAngle(int angle) {
  // 将角度 (0-180) 转换为脉冲宽度 (1000-2000 微秒)
  int pulseWidth = map(angle, 0, 180, 1000, 2000);

  // 发送 PWM 脉冲
  digitalWrite(SERVO_PIN, HIGH);
  delayMicroseconds(pulseWidth);
  digitalWrite(SERVO_PIN, LOW);

  // 等待剩余的周期时间 (20ms - pulseWidth)
  delay(20 - (pulseWidth / 1000));
}

void scanServo() {
  // 从 0° 扫描到 180°
  for (int angle = 0; angle <= 180; angle += 10) {
    setServoAngle(angle);
    delay(100);
  }

  // 从 180° 扫描回 0°
  for (int angle = 180; angle >= 0; angle -= 10) {
    setServoAngle(angle);
    delay(100);
  }
}