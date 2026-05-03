/*
 * Solution 01: 完整的中断和定时器系统
 *
 * 这个程序展示了完整的中断和定时器应用，
 * 包括外部中断、定时器中断和非阻塞任务调度。
 */

#include <Arduino.h>

// 外部中断变量
volatile bool externalInterruptTriggered = false;
volatile unsigned long interruptTimestamp = 0;

// 定时器计数器
volatile unsigned long timerCounter = 0;

// 任务调度
unsigned long lastTask1Time = 0;
unsigned long lastTask2Time = 0;
const unsigned long TASK1_INTERVAL = 1000; // 1秒
const unsigned long TASK2_INTERVAL = 2500; // 2.5秒

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }

  Serial.println("=== 完整的中断和定时器系统 ===");

  // 设置外部中断（引脚2）
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), externalISR, FALLING);

  // 配置 Timer1
  configureTimer1();

  // 启用全局中断
  sei();

  pinMode(13, OUTPUT);
}

void loop() {
  unsigned long currentTime = millis();

  // 处理外部中断事件
  if (externalInterruptTriggered) {
    cli(); // 禁用中断
    unsigned long timestamp = interruptTimestamp;
    sei(); // 启用中断

    Serial.print("外部中断触发于: ");
    Serial.print(timestamp);
    Serial.println("ms");

    // LED 闪烁确认
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);

    externalInterruptTriggered = false;
  }

  // 任务1：每1秒执行
  if (currentTime - lastTask1Time >= TASK1_INTERVAL) {
    Serial.println("任务1执行");
    lastTask1Time = currentTime;
  }

  // 任务2：每2.5秒执行
  if (currentTime - lastTask2Time >= TASK2_INTERVAL) {
    Serial.println("任务2执行");
    lastTask2Time = currentTime;
  }

  // 显示定时器计数（每5秒）
  static unsigned long lastDisplayTime = 0;
  if (currentTime - lastDisplayTime >= 5000) {
    cli();
    unsigned long counter = timerCounter;
    sei();
    Serial.print("Timer1 计数: ");
    Serial.println(counter);
    lastDisplayTime = currentTime;
  }
}

void externalISR() {
  externalInterruptTriggered = true;
  interruptTimestamp = millis();
}

void configureTimer1() {
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1B |= (1 << CS11) | (1 << CS10); // 64分频
  OCR1A = 24999; // 100ms
  TIMSK1 |= (1 << OCIE1A);
  TCNT1 = 0;
}

ISR(TIMER1_COMPA_vect) {
  timerCounter++;
}