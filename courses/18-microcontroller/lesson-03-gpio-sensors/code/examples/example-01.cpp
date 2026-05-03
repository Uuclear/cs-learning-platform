/*
 * Example 01: 按钮防抖（debounce）算法
 *
 * 机械按钮在按下和释放时会产生机械抖动，
 * 导致短时间内产生多个开关信号。
 * 这个程序演示了软件防抖算法的实现。
 */

#include <Arduino.h>

// 定义按钮引脚
const int BUTTON_PIN = 2;

// 防抖参数
const unsigned long DEBOUNCE_DELAY = 50; // 50ms 防抖时间

// 全局变量
int lastButtonState = HIGH;    // 上次读取的按钮状态（使用内部上拉，未按下为HIGH）
int currentButtonState = HIGH; // 当前按钮状态
unsigned long lastDebounceTime = 0; // 最后一次状态变化的时间

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 按钮防抖演示 ===");
  Serial.println();
  Serial.println("按钮连接到引脚 2（使用内部上拉电阻）");
  Serial.println("按下按钮观察原始状态和防抖状态的差异");
  Serial.println();

  // 设置按钮引脚为输入，启用内部上拉电阻
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // 读取初始状态
  lastButtonState = digitalRead(BUTTON_PIN);
}

void loop() {
  // 读取原始按钮状态
  int reading = digitalRead(BUTTON_PIN);

  // 检查是否发生了状态变化
  if (reading != lastButtonState) {
    // 重置防抖计时器
    lastDebounceTime = millis();
  }

  // 如果超过防抖时间，确认状态变化
  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    // 如果状态确实发生了变化
    if (reading != currentButtonState) {
      currentButtonState = reading;

      // 只在按钮按下时输出（下降沿）
      if (currentButtonState == LOW) {
        Serial.println("✅ 按钮已按下（防抖后）");
      }
    }
  }

  // 更新上次状态
  lastButtonState = reading;

  // 每秒输出一次状态用于调试
  static unsigned long lastDebugTime = 0;
  if (millis() - lastDebugTime >= 1000) {
    Serial.print("原始状态: ");
    Serial.print(reading == LOW ? "按下" : "未按下");
    Serial.print(" | 防抖状态: ");
    Serial.println(currentButtonState == LOW ? "按下" : "未按下");
    lastDebugTime = millis();
  }
}