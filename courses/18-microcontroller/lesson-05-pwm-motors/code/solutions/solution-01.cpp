/*
 * Solution 01: 完整的 PWM 电机控制系统
 *
 * 这个程序展示了完整的 PWM 电机控制，
 * 包括速度控制、方向控制和安全保护。
 */

#include <Arduino.h>

const int MOTOR_PWM = 10;
const int MOTOR_DIR1 = 8;
const int MOTOR_DIR2 = 9;
const int CURRENT_SENSE = A0;

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }

  Serial.println("=== 完整的 PWM 电机控制系统 ===");

  pinMode(MOTOR_PWM, OUTPUT);
  pinMode(MOTOR_DIR1, OUTPUT);
  pinMode(MOTOR_DIR2, OUTPUT);
  pinMode(CURRENT_SENSE, INPUT);

  stopMotor();
}

void loop() {
  static int mode = 0;
  static unsigned long lastModeTime = 0;
  const unsigned long MODE_TIME = 3000;

  if (millis() - lastModeTime >= MODE_TIME) {
    mode = (mode + 1) % 4;
    lastModeTime = millis();

    switch (mode) {
      case 0:
        setMotorSpeed(0); // 停止
        Serial.println("电机停止");
        break;
      case 1:
        setMotorDirection(1);
        setMotorSpeed(150); // 正转中速
        Serial.println("正转中速");
        break;
      case 2:
        setMotorDirection(-1);
        setMotorSpeed(200); // 反转高速
        Serial.println("反转高速");
        break;
      case 3:
        runMotorSweep(); // 扫描测试
        Serial.println("扫描测试");
        break;
    }
  }

  // 电流监控
  monitorCurrent();
}

void setMotorDirection(int dir) {
  if (dir > 0) {
    digitalWrite(MOTOR_DIR1, HIGH);
    digitalWrite(MOTOR_DIR2, LOW);
  } else if (dir < 0) {
    digitalWrite(MOTOR_DIR1, LOW);
    digitalWrite(MOTOR_DIR2, HIGH);
  } else {
    stopMotor();
  }
}

void setMotorSpeed(int speed) {
  speed = constrain(speed, 0, 255);
  analogWrite(MOTOR_PWM, speed);
}

void stopMotor() {
  digitalWrite(MOTOR_DIR1, LOW);
  digitalWrite(MOTOR_DIR2, LOW);
  analogWrite(MOTOR_PWM, 0);
}

void runMotorSweep() {
  for (int speed = 0; speed <= 255; speed += 10) {
    setMotorSpeed(speed);
    delay(50);
  }
  for (int speed = 255; speed >= 0; speed -= 10) {
    setMotorSpeed(speed);
    delay(50);
  }
}

void monitorCurrent() {
  static unsigned long lastCheck = 0;
  if (millis() - lastCheck >= 100) {
    int currentReading = analogRead(CURRENT_SENSE);
    float current = currentReading * (5.0 / 1023.0) / 0.1; // 假设 0.1Ω 采样电阻

    if (current > 2.0) { // 2A 过流保护
      Serial.println("⚠️ 过流保护触发!");
      stopMotor();
    }

    lastCheck = millis();
  }
}