/*
 * Solution 01: 完整的按钮处理系统
 *
 * 这个程序提供了完整的按钮处理功能，包括：
 * - 软件防抖
 * - 长按检测
 * - 双击检测
 * - 多按钮支持
 */

#include <Arduino.h>

// 按钮配置
const int BUTTON_PINS[] = {2, 3, 4}; // 三个按钮
const int NUM_BUTTONS = 3;

// 按钮状态结构
struct ButtonState {
  int pin;
  int currentState;
  int lastState;
  unsigned long lastDebounceTime;
  unsigned long pressStartTime;
  bool isPressed;
  bool wasLongPress;
  bool doubleClickPending;
  unsigned long lastClickTime;
};

ButtonState buttons[NUM_BUTTONS];

// 配置参数
const unsigned long DEBOUNCE_DELAY = 50;    // 防抖时间 50ms
const unsigned long LONG_PRESS_TIME = 1000; // 长按时间 1秒
const unsigned long DOUBLE_CLICK_TIME = 300; // 双击间隔 300ms

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 完整的按钮处理系统 ===");
  Serial.println();
  Serial.println("支持的功能:");
  Serial.println("- 单击检测");
  Serial.println("- 长按检测 (>1秒)");
  Serial.println("- 双击检测 (<300ms)");
  Serial.println();

  // 初始化按钮
  for (int i = 0; i < NUM_BUTTONS; i++) {
    buttons[i].pin = BUTTON_PINS[i];
    buttons[i].currentState = HIGH;
    buttons[i].lastState = HIGH;
    buttons[i].lastDebounceTime = 0;
    buttons[i].pressStartTime = 0;
    buttons[i].isPressed = false;
    buttons[i].wasLongPress = false;
    buttons[i].doubleClickPending = false;
    buttons[i].lastClickTime = 0;

    pinMode(buttons[i].pin, INPUT_PULLUP);
  }
}

void loop() {
  for (int i = 0; i < NUM_BUTTONS; i++) {
    updateButton(&buttons[i]);
  }
}

void updateButton(ButtonState* btn) {
  int reading = digitalRead(btn->pin);

  // 防抖处理
  if (reading != btn->lastState) {
    btn->lastDebounceTime = millis();
  }

  if ((millis() - btn->lastDebounceTime) > DEBOUNCE_DELAY) {
    if (reading != btn->currentState) {
      btn->currentState = reading;

      if (btn->currentState == LOW) {
        // 按钮按下
        btn->pressStartTime = millis();
        btn->isPressed = true;
        btn->wasLongPress = false;
      } else {
        // 按钮释放
        if (btn->isPressed) {
          unsigned long pressDuration = millis() - btn->pressStartTime;

          if (pressDuration >= LONG_PRESS_TIME) {
            // 长按事件
            handleLongPress(btn->pin);
            btn->wasLongPress = true;
          } else {
            // 短按事件
            if (!btn->wasLongPress) {
              handleShortPress(btn->pin, pressDuration);
            }
          }

          btn->isPressed = false;
        }
      }
    }
  }

  btn->lastState = reading;

  // 双击检测（在按钮释放后）
  if (!btn->isPressed && !btn->wasLongPress && btn->currentState == HIGH) {
    if (btn->doubleClickPending) {
      unsigned long timeSinceLastClick = millis() - btn->lastClickTime;
      if (timeSinceLastClick <= DOUBLE_CLICK_TIME) {
        handleDoubleClick(btn->pin);
        btn->doubleClickPending = false;
      } else {
        btn->doubleClickPending = false;
      }
    } else {
      // 设置双击待处理状态
      btn->doubleClickPending = true;
      btn->lastClickTime = millis();
    }
  }
}

void handleShortPress(int pin, unsigned long duration) {
  Serial.print("按钮 ");
  Serial.print(pin);
  Serial.print(": 单击 (");
  Serial.print(duration);
  Serial.println("ms)");

  // 控制 LED
  digitalWrite(13, !digitalRead(13));
}

void handleLongPress(int pin) {
  Serial.print("按钮 ");
  Serial.print(pin);
  Serial.println(": 长按");

  // 快速闪烁 LED
  for (int i = 0; i < 5; i++) {
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
  }
}

void handleDoubleClick(int pin) {
  Serial.print("按钮 ");
  Serial.print(pin);
  Serial.println(": 双击");

  // 慢速闪烁 LED
  for (int i = 0; i < 3; i++) {
    digitalWrite(13, HIGH);
    delay(300);
    digitalWrite(13, LOW);
    delay(300);
  }
}