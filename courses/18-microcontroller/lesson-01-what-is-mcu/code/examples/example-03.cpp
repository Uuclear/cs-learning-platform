/*
 * Example 03: Arduino Blink 程序
 *
 * 这是经典的 Arduino Blink 程序，是嵌入式开发的 "Hello World"。
 * 用于验证开发环境和基本功能。
 */

// 引脚13通常连接到Arduino板载LED
const int LED_PIN = 13;

void setup() {
  // 初始化LED引脚为输出模式
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // 点亮LED (设置引脚为高电平)
  digitalWrite(LED_PIN, HIGH);
  // 延迟1000毫秒 (1秒)
  delay(1000);

  // 熄灭LED (设置引脚为低电平)
  digitalWrite(LED_PIN, LOW);
  // 再次延迟1000毫秒
  delay(1000);
}