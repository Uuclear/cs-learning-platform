/*
 * Example 03: 多 LED 闪烁模式演示
 *
 * 这个程序演示了多种 LED 闪烁模式，包括：
 * - 基本同步闪烁
 * - 跑马灯效果
 * - 随机闪烁
 * - 交通灯模拟
 */

#include <Arduino.h>

// 定义 LED 引脚（使用数字引脚 8-12）
const int LED_PINS[] = {8, 9, 10, 11, 12};
const int NUM_LEDS = 5;

// 模式枚举
enum PatternMode {
  MODE_SYNC_BLINK,
  MODE_CHASE,
  MODE_RANDOM,
  MODE_TRAFFIC_LIGHT
};

PatternMode currentMode = MODE_SYNC_BLINK;
unsigned long lastModeChange = 0;
const unsigned long MODE_DURATION = 10000; // 每种模式持续 10 秒

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 多 LED 闪烁模式演示 ===");
  Serial.println();
  Serial.println("自动循环以下模式:");
  Serial.println("1. 同步闪烁 (所有 LED 同时亮灭)");
  Serial.println("2. 跑马灯效果 (流水灯)");
  Serial.println("3. 随机闪烁 (随机 LED 亮起)");
  Serial.println("4. 交通灯模拟 (引脚 8,9,10 作为红黄绿)");
  Serial.println();

  // 初始化所有 LED 引脚为输出
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW); // 确保初始状态关闭
  }

  // 初始化随机种子
  randomSeed(analogRead(0));
}

void loop() {
  unsigned long currentTime = millis();

  // 每 MODE_DURATION 毫秒切换一次模式
  if (currentTime - lastModeChange >= MODE_DURATION) {
    currentMode = static_cast<PatternMode>((currentMode + 1) % 4);
    lastModeChange = currentTime;

    // 关闭所有 LED 并显示当前模式
    for (int i = 0; i < NUM_LEDS; i++) {
      digitalWrite(LED_PINS[i], LOW);
    }

    switch (currentMode) {
      case MODE_SYNC_BLINK:
        Serial.println("切换到: 同步闪烁模式");
        break;
      case MODE_CHASE:
        Serial.println("切换到: 跑马灯模式");
        break;
      case MODE_RANDOM:
        Serial.println("切换到: 随机闪烁模式");
        break;
      case MODE_TRAFFIC_LIGHT:
        Serial.println("切换到: 交通灯模式");
        break;
    }
    Serial.println();
  }

  // 根据当前模式执行相应逻辑
  switch (currentMode) {
    case MODE_SYNC_BLINK:
      runSyncBlink();
      break;
    case MODE_CHASE:
      runChasePattern();
      break;
    case MODE_RANDOM:
      runRandomPattern();
      break;
    case MODE_TRAFFIC_LIGHT:
      runTrafficLightPattern();
      break;
  }
}

void runSyncBlink() {
  static unsigned long lastToggle = 0;
  static bool ledState = false;

  if (millis() - lastToggle >= 500) {
    ledState = !ledState;
    for (int i = 0; i < NUM_LEDS; i++) {
      digitalWrite(LED_PINS[i], ledState ? HIGH : LOW);
    }
    lastToggle = millis();
  }
}

void runChasePattern() {
  static unsigned long lastStep = 0;
  static int chaseIndex = 0;
  static bool reverseDirection = false;

  if (millis() - lastStep >= 200) {
    // 关闭所有 LED
    for (int i = 0; i < NUM_LEDS; i++) {
      digitalWrite(LED_PINS[i], LOW);
    }

    // 点亮当前 LED
    digitalWrite(LED_PINS[chaseIndex], HIGH);

    // 更新索引
    if (!reverseDirection) {
      chaseIndex++;
      if (chaseIndex >= NUM_LEDS) {
        reverseDirection = true;
        chaseIndex = NUM_LEDS - 2; // 避免重复点亮最后一个
      }
    } else {
      chaseIndex--;
      if (chaseIndex < 0) {
        reverseDirection = false;
        chaseIndex = 1; // 避免重复点亮第一个
      }
    }

    lastStep = millis();
  }
}

void runRandomPattern() {
  static unsigned long lastToggle = 0;

  if (millis() - lastToggle >= 300) {
    // 关闭所有 LED
    for (int i = 0; i < NUM_LEDS; i++) {
      digitalWrite(LED_PINS[i], LOW);
    }

    // 随机点亮一个 LED
    int randomLed = random(NUM_LEDS);
    digitalWrite(LED_PINS[randomLed], HIGH);

    lastToggle = millis();
  }
}

void runTrafficLightPattern() {
  static unsigned long trafficStartTime = 0;
  static int trafficPhase = 0;

  if (trafficStartTime == 0) {
    trafficStartTime = millis();
  }

  unsigned long phaseTime = millis() - trafficStartTime;

  // 只使用前3个 LED 作为交通灯 (8=红, 9=黄, 10=绿)
  // 关闭所有 LED
  digitalWrite(LED_PINS[0], LOW); // 红
  digitalWrite(LED_PINS[1], LOW); // 黄
  digitalWrite(LED_PINS[2], LOW); // 绿

  if (phaseTime < 5000) {
    // 红灯阶段 (0-5秒)
    digitalWrite(LED_PINS[0], HIGH);
    trafficPhase = 0;
  }
  else if (phaseTime < 7000) {
    // 黄灯阶段 (5-7秒)
    digitalWrite(LED_PINS[1], HIGH);
    trafficPhase = 1;
  }
  else if (phaseTime < 12000) {
    // 绿灯阶段 (7-12秒)
    digitalWrite(LED_PINS[2], HIGH);
    trafficPhase = 2;
  }
  else if (phaseTime < 14000) {
    // 黄灯闪烁阶段 (12-14秒)
    if ((phaseTime / 250) % 2 == 0) {
      digitalWrite(LED_PINS[1], HIGH);
    }
    trafficPhase = 3;
  }
  else {
    // 重置交通灯周期
    trafficStartTime = millis();
  }
}