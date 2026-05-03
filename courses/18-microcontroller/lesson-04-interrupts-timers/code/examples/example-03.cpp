/*
 * Example 03: 硬件定时器中断（使用 Timer1）
 *
 * 这个程序演示如何使用硬件定时器中断来实现精确的定时任务。
 * 注意：Arduino Uno 使用 ATmega328P，有多个硬件定时器。
 */

#include <Arduino.h>

// 使用 Timer1 进行精确定时
volatile unsigned long timer1Counter = 0;
const unsigned long TIMER1_INTERVAL_MS = 100; // 100ms 定时器间隔

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口连接
  }

  Serial.println("=== 硬件定时器中断演示 ===");
  Serial.println();
  Serial.println("使用 Timer1 实现 100ms 精确定时中断");
  Serial.println();

  // 配置 Timer1
  configureTimer1();

  // 启用全局中断
  sei();
}

void loop() {
  static unsigned long lastDisplayTime = 0;

  // 显示定时器计数值（每秒一次）
  if (millis() - lastDisplayTime >= 1000) {
    unsigned long counter;

    // 在读取 volatile 变量时禁用中断以避免竞争条件
    cli();
    counter = timer1Counter;
    sei();

    Serial.print("Timer1 计数: ");
    Serial.println(counter);
    lastDisplayTime = millis();
  }

  // 主程序可以执行其他任务
  // LED 闪烁作为主程序任务
  static bool ledState = false;
  static unsigned long lastBlinkTime = 0;

  if (millis() - lastBlinkTime >= 500) {
    ledState = !ledState;
    digitalWrite(13, ledState ? HIGH : LOW);
    lastBlinkTime = millis();
  }
}

// 配置 Timer1 为 CTC 模式，产生 100ms 中断
void configureTimer1() {
  // 设置 Timer1 为 CTC 模式
  TCCR1A = 0; // 清除控制寄存器 A
  TCCR1B = 0; // 清除控制寄存器 B

  // 设置预分频器为 64
  TCCR1B |= (1 << CS11) | (1 << CS10); // 64 分频

  // 设置比较匹配值 (16MHz / 64 / 10Hz = 25000)
  OCR1A = 24999; // 100ms 周期 (10Hz)

  // 启用比较匹配中断
  TIMSK1 |= (1 << OCIE1A);

  // 初始化计数器
  TCNT1 = 0;
}

// Timer1 比较匹配中断服务程序
ISR(TIMER1_COMPA_vect) {
  timer1Counter++;

  // 可以在这里执行精确定时的任务
  // 例如：读取传感器、更新 PWM、处理通信等

  // 注意：ISR 应该尽可能快！
}