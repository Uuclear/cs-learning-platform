/*
 * Example 02: 直流电机 PWM 控制
 *
 * 这个程序演示如何使用 PWM 控制直流电机的速度。
 * 注意：实际应用中需要电机驱动电路（如 L298N 或 TB6612FNG）。
 */

#include <Arduino.h>

// 定义电机控制引脚
const int MOTOR_PWM_PIN = 10;    // 电机速度控制 (PWM)
const int MOTOR_DIR_PIN1 = 8;    // 电机方向控制 1
const int MOTOR_DIR_PIN2 = 9;    // 电机方向控制 2

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 直流电机 PWM 控制演示 ===");
  Serial.println();
  Serial.println("注意: 实际电路需要电机驱动模块!");
  Serial.println("引脚连接:");
  Serial.println("- PWM 控制: 引脚 10");
  Serial.println("- 方向控制: 引脚 8, 9");
  Serial.println();

  // 设置电机控制引脚为输出
  pinMode(MOTOR_PWM_PIN, OUTPUT);
  pinMode(MOTOR_DIR_PIN1, OUTPUT);
  pinMode(MOTOR_DIR_PIN2, OUTPUT);

  // 初始状态：电机停止
  stopMotor();
}

void loop() {
  static int demoStep = 0;
  static unsigned long lastDemoTime = 0;
  const unsigned long DEMO_INTERVAL = 3000; // 每3秒切换一次演示

  if (millis() - lastDemoTime >= DEMO_INTERVAL) {
    switch (demoStep % 4) {
      case 0:
        // 正转 - 低速
        setMotorDirection(1);
        analogWrite(MOTOR_PWM_PIN, 100); // 40% 占空比
        Serial.println("演示 1: 正转 - 低速 (40%)");
        break;

      case 1:
        // 正转 - 高速
        setMotorDirection(1);
        analogWrite(MOTOR_PWM_PIN, 200); // 80% 占空比
        Serial.println("演示 2: 正转 - 高速 (80%)");
        break;

      case 2:
        // 反转 - 低速
        setMotorDirection(-1);
        analogWrite(MOTOR_PWM_PIN, 100); // 40% 占空比
        Serial.println("演示 3: 反转 - 低速 (40%)");
        break;

      case 3:
        // 停止
        stopMotor();
        Serial.println("演示 4: 电机停止");
        break;
    }

    demoStep++;
    lastDemoTime = millis();
    Serial.println();
  }
}

void setMotorDirection(int direction) {
  // direction: 1 = 正转, -1 = 反转, 0 = 停止
  if (direction > 0) {
    digitalWrite(MOTOR_DIR_PIN1, HIGH);
    digitalWrite(MOTOR_DIR_PIN2, LOW);
  } else if (direction < 0) {
    digitalWrite(MOTOR_DIR_PIN1, LOW);
    digitalWrite(MOTOR_DIR_PIN2, HIGH);
  } else {
    stopMotor();
  }
}

void stopMotor() {
  digitalWrite(MOTOR_DIR_PIN1, LOW);
  digitalWrite(MOTOR_DIR_PIN2, LOW);
  analogWrite(MOTOR_PWM_PIN, 0);
}