#!/usr/bin/env python3
"""
多 LED 闪烁模式生成器

这个脚本生成多种 LED 闪烁模式的 Arduino 代码，
帮助学习者快速创建有趣的灯光效果。

使用方法：
    python example-03.py
"""

import random
from datetime import datetime

class LEDPatternGenerator:
    """LED 闪烁模式生成器"""

    def __init__(self):
        self.patterns = {
            "blink": self.generate_blink_pattern,
            "chase": self.generate_chase_pattern,
            "fade": self.generate_fade_pattern,
            "random": self.generate_random_pattern,
            "traffic_light": self.generate_traffic_light_pattern
        }

    def generate_blink_pattern(self, pins, **kwargs):
        """生成基本闪烁模式"""
        code = f"""// 基本闪烁模式
const int ledPins[] = {{{', '.join(map(str, pins))}}};
const int numLeds = {len(pins)};

void setup() {{
  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  // 所有 LED 同时亮
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], HIGH);
  }}
  delay(500);

  // 所有 LED 同时灭
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], LOW);
  }}
  delay(500);
}}
"""
        return code

    def generate_chase_pattern(self, pins, **kwargs):
        """生成跑马灯模式"""
        code = f"""// 跑马灯模式
const int ledPins[] = {{{', '.join(map(str, pins))}}};
const int numLeds = {len(pins)};

void setup() {{
  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  // 正向跑马灯
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], HIGH);
    delay(200);
    digitalWrite(ledPins[i], LOW);
  }}

  // 反向跑马灯
  for (int i = numLeds - 1; i >= 0; i--) {{
    digitalWrite(ledPins[i], HIGH);
    delay(200);
    digitalWrite(ledPins[i], LOW);
  }}
}}
"""
        return code

    def generate_fade_pattern(self, pins, **kwargs):
        """生成渐变模式（需要 PWM 引脚）"""
        # 检查是否所有引脚都是 PWM 引脚
        pwm_pins = [pin for pin in pins if pin in [3, 5, 6, 9, 10, 11]]

        if len(pwm_pins) != len(pins):
            return f"// 注意：渐变模式需要 PWM 引脚（3, 5, 6, 9, 10, 11）\n// 您提供的引脚 {pins} 中有些不是 PWM 引脚"

        code = f"""// 渐变模式（呼吸灯效果）
const int ledPins[] = {{{', '.join(map(str, pins))}}};
const int numLeds = {len(pins)};

void setup() {{
  // PWM 引脚不需要设置 pinMode，analogWrite 会自动处理
}}

void loop() {{
  // 逐渐变亮
  for (int brightness = 0; brightness <= 255; brightness++) {{
    for (int i = 0; i < numLeds; i++) {{
      analogWrite(ledPins[i], brightness);
    }}
    delay(10);
  }}

  // 逐渐变暗
  for (int brightness = 255; brightness >= 0; brightness--) {{
    for (int i = 0; i < numLeds; i++) {{
      analogWrite(ledPins[i], brightness);
    }}
    delay(10);
  }}
}}
"""
        return code

    def generate_random_pattern(self, pins, **kwargs):
        """生成随机闪烁模式"""
        code = f"""// 随机闪烁模式
const int ledPins[] = {{{', '.join(map(str, pins))}}};
const int numLeds = {len(pins)};

void setup() {{
  randomSeed(analogRead(0)); // 使用未连接的模拟引脚作为随机种子
  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  // 随机选择一个 LED 亮起
  int randomLed = random(numLeds);
  digitalWrite(ledPins[randomLed], HIGH);
  delay(200);
  digitalWrite(ledPins[randomLed], LOW);
  delay(100);
}}
"""
        return code

    def generate_traffic_light_pattern(self, pins, **kwargs):
        """生成交通灯模式（需要至少3个引脚）"""
        if len(pins) < 3:
            return "// 交通灯模式需要至少3个引脚（红、黄、绿）"

        red_pin, yellow_pin, green_pin = pins[0], pins[1], pins[2]
        code = f"""// 交通灯模式
const int redPin = {red_pin};
const int yellowPin = {yellow_pin};
const int greenPin = {green_pin};

void setup() {{
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
}}

void loop() {{
  // 红灯亮 5 秒
  digitalWrite(redPin, HIGH);
  digitalWrite(yellowPin, LOW);
  digitalWrite(greenPin, LOW);
  delay(5000);

  // 黄灯亮 2 秒
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, HIGH);
  digitalWrite(greenPin, LOW);
  delay(2000);

  // 绿灯亮 5 秒
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, LOW);
  digitalWrite(greenPin, HIGH);
  delay(5000);

  // 黄灯闪烁准备变红
  digitalWrite(greenPin, LOW);
  for (int i = 0; i < 4; i++) {{
    digitalWrite(yellowPin, HIGH);
    delay(250);
    digitalWrite(yellowPin, LOW);
    delay(250);
  }}
}}
"""
        return code

    def list_patterns(self):
        """列出所有可用的模式"""
        print("可用的 LED 闪烁模式:")
        for pattern_name in self.patterns.keys():
            print(f"  - {pattern_name}")

    def generate_code(self, pattern_name, pins):
        """根据模式名称和引脚生成代码"""
        if pattern_name not in self.patterns:
            raise ValueError(f"未知的模式: {pattern_name}")

        return self.patterns[pattern_name](pins)

def main():
    """主函数"""
    generator = LEDPatternGenerator()

    print("=== 多 LED 闪烁模式生成器 ===")
    print()
    generator.list_patterns()
    print()

    try:
        # 获取用户输入
        pattern = input("请选择模式: ").strip().lower()

        if pattern not in generator.patterns:
            print("无效的模式选择")
            return

        pins_input = input("请输入 LED 连接的引脚号（用逗号分隔，例如: 8,9,10）: ").strip()
        pins = [int(x.strip()) for x in pins_input.split(',')]

        # 验证引脚号
        for pin in pins:
            if pin < 0 or pin > 13:
                print(f"警告: 引脚 {pin} 可能超出 Arduino UNO 的数字引脚范围 (0-13)")

        # 生成代码
        code = generator.generate_code(pattern, pins)

        print("\n=== 生成的 Arduino 代码 ===")
        print(code)

        # 询问是否保存到文件
        save_choice = input("\n是否保存到文件? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = f"led_{pattern}_pattern.ino"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"代码已保存到 {filename}")

    except ValueError as e:
        print(f"输入错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()