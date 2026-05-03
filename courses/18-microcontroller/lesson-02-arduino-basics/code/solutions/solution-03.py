#!/usr/bin/env python3
"""
多 LED 闪烁模式生成器 - 完整解决方案

这个脚本提供完整的 LED 模式生成功能，
包括错误处理、引脚验证和代码优化。
"""

import os
from typing import List, Dict, Optional

class LEDPatternGenerator:
    """完整的 LED 闪烁模式生成器"""

    def __init__(self):
        self.arduino_pins = list(range(0, 14))  # Arduino UNO 数字引脚 0-13
        self.pwm_pins = [3, 5, 6, 9, 10, 11]   # PWM 引脚

        self.patterns = {
            "blink": {
                "name": "基本闪烁",
                "description": "所有 LED 同时闪烁",
                "min_pins": 1,
                "requires_pwm": False,
                "generator": self._generate_blink_code
            },
            "chase": {
                "name": "跑马灯",
                "description": "LED 依次点亮形成流动效果",
                "min_pins": 2,
                "requires_pwm": False,
                "generator": self._generate_chase_code
            },
            "fade": {
                "name": "渐变呼吸",
                "description": "LED 亮度逐渐变化（需要 PWM 引脚）",
                "min_pins": 1,
                "requires_pwm": True,
                "generator": self._generate_fade_code
            },
            "random": {
                "name": "随机闪烁",
                "description": "随机选择 LED 闪烁",
                "min_pins": 2,
                "requires_pwm": False,
                "generator": self._generate_random_code
            },
            "traffic_light": {
                "name": "交通灯",
                "description": "模拟红绿灯工作流程",
                "min_pins": 3,
                "requires_pwm": False,
                "generator": self._generate_traffic_light_code
            },
            "binary_counter": {
                "name": "二进制计数器",
                "description": "LED 显示二进制数值递增",
                "min_pins": 1,
                "requires_pwm": False,
                "generator": self._generate_binary_counter_code
            }
        }

    def validate_pins(self, pins: List[int]) -> bool:
        """验证引脚号是否有效"""
        for pin in pins:
            if pin not in self.arduino_pins:
                return False
        return True

    def validate_pwm_pins(self, pins: List[int]) -> bool:
        """验证是否所有引脚都是 PWM 引脚"""
        return all(pin in self.pwm_pins for pin in pins)

    def get_available_patterns(self, pins: List[int]) -> List[str]:
        """根据提供的引脚获取可用的模式"""
        available = []
        has_pwm = self.validate_pwm_pins(pins)

        for pattern_name, pattern_info in self.patterns.items():
            if (len(pins) >= pattern_info["min_pins"] and
                (not pattern_info["requires_pwm"] or has_pwm)):
                available.append(pattern_name)

        return available

    def _generate_blink_code(self, pins: List[int], **kwargs) -> str:
        """生成基本闪烁代码"""
        pins_str = ", ".join(map(str, pins))
        num_leds = len(pins)

        return f"""// 基本闪烁模式 - 所有 LED 同时亮灭
const int ledPins[] = {{{pins_str}}};
const int numLeds = {num_leds};

void setup() {{
  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  // 全部点亮
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], HIGH);
  }}
  delay(500);

  // 全部熄灭
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], LOW);
  }}
  delay(500);
}}
"""

    def _generate_chase_code(self, pins: List[int], **kwargs) -> str:
        """生成跑马灯代码"""
        pins_str = ", ".join(map(str, pins))
        num_leds = len(pins)

        return f"""// 跑马灯模式 - LED 依次点亮
const int ledPins[] = {{{pins_str}}};
const int numLeds = {num_leds};

void setup() {{
  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  // 正向流动
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], HIGH);
    delay(200);
    digitalWrite(ledPins[i], LOW);
  }}

  // 反向流动
  for (int i = numLeds - 1; i >= 0; i--) {{
    digitalWrite(ledPins[i], HIGH);
    delay(200);
    digitalWrite(ledPins[i], LOW);
  }}
}}
"""

    def _generate_fade_code(self, pins: List[int], **kwargs) -> str:
        """生成渐变代码"""
        pins_str = ", ".join(map(str, pins))
        num_leds = len(pins)

        return f"""// 渐变呼吸灯效果 - 需要 PWM 引脚
const int ledPins[] = {{{pins_str}}};
const int numLeds = {num_leds};

void setup() {{
  // analogWrite 自动处理 PWM 引脚配置
}}

void loop() {{
  // 逐渐变亮
  for (int brightness = 0; brightness <= 255; brightness += 2) {{
    for (int i = 0; i < numLeds; i++) {{
      analogWrite(ledPins[i], brightness);
    }}
    delay(15);
  }}

  // 逐渐变暗
  for (int brightness = 255; brightness >= 0; brightness -= 2) {{
    for (int i = 0; i < numLeds; i++) {{
      analogWrite(ledPins[i], brightness);
    }}
    delay(15);
  }}
}}
"""

    def _generate_random_code(self, pins: List[int], **kwargs) -> str:
        """生成随机闪烁代码"""
        pins_str = ", ".join(map(str, pins))
        num_leds = len(pins)

        return f"""// 随机闪烁模式
const int ledPins[] = {{{pins_str}}};
const int numLeds = {num_leds};

void setup() {{
  randomSeed(analogRead(0)); // 使用浮动模拟引脚作为随机种子

  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  // 关闭所有 LED
  for (int i = 0; i < numLeds; i++) {{
    digitalWrite(ledPins[i], LOW);
  }}

  // 随机点亮一个 LED
  int randomLed = random(numLeds);
  digitalWrite(ledPins[randomLed], HIGH);
  delay(300);
}}
"""

    def _generate_traffic_light_code(self, pins: List[int], **kwargs) -> str:
        """生成交通灯代码"""
        red_pin, yellow_pin, green_pin = pins[0], pins[1], pins[2]

        return f"""// 交通灯模拟器
const int redPin = {red_pin};
const int yellowPin = {yellow_pin};
const int greenPin = {green_pin};

void setup() {{
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
}}

void loop() {{
  // 红灯阶段 - 5秒
  digitalWrite(redPin, HIGH);
  digitalWrite(yellowPin, LOW);
  digitalWrite(greenPin, LOW);
  delay(5000);

  // 黄灯准备 - 2秒
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, HIGH);
  digitalWrite(greenPin, LOW);
  delay(2000);

  // 绿灯阶段 - 5秒
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, LOW);
  digitalWrite(greenPin, HIGH);
  delay(5000);

  // 黄灯警告 - 闪烁2秒
  digitalWrite(greenPin, LOW);
  for (int i = 0; i < 4; i++) {{
    digitalWrite(yellowPin, HIGH);
    delay(250);
    digitalWrite(yellowPin, LOW);
    delay(250);
  }}
}}
"""

    def _generate_binary_counter_code(self, pins: List[int], **kwargs) -> str:
        """生成二进制计数器代码"""
        pins_str = ", ".join(map(str, pins))
        num_leds = len(pins)
        max_count = 2 ** num_leds

        return f"""// 二进制计数器 - 显示 0 到 {(max_count-1)}
const int ledPins[] = {{{pins_str}}};
const int numLeds = {num_leds};

void setup() {{
  for (int i = 0; i < numLeds; i++) {{
    pinMode(ledPins[i], OUTPUT);
  }}
}}

void loop() {{
  for (int count = 0; count < {max_count}; count++) {{
    // 设置每个 LED 的状态
    for (int i = 0; i < numLeds; i++) {{
      digitalWrite(ledPins[i], (count >> i) & 1 ? HIGH : LOW);
    }}
    delay(500);
  }}
}}
"""

    def generate_code(self, pattern_name: str, pins: List[int]) -> str:
        """生成指定模式的代码"""
        if pattern_name not in self.patterns:
            raise ValueError(f"未知的模式: {pattern_name}")

        pattern_info = self.patterns[pattern_name]

        # 验证引脚数量
        if len(pins) < pattern_info["min_pins"]:
            raise ValueError(f"{pattern_info['name']} 模式至少需要 {pattern_info['min_pins']} 个引脚")

        # 验证 PWM 要求
        if pattern_info["requires_pwm"] and not self.validate_pwm_pins(pins):
            non_pwm_pins = [pin for pin in pins if pin not in self.pwm_pins]
            raise ValueError(f"渐变模式需要 PWM 引脚，但 {non_pwm_pins} 不是 PWM 引脚")

        return pattern_info["generator"](pins)

    def list_patterns(self):
        """列出所有模式及其描述"""
        print("可用的 LED 闪烁模式:")
        print("-" * 50)
        for name, info in self.patterns.items():
            print(f"{name:15} - {info['description']}")
        print()

def main():
    """主函数"""
    generator = LEDPatternGenerator()

    print("=== 多 LED 闪烁模式生成器 ===")
    generator.list_patterns()

    try:
        # 获取用户输入
        pattern_input = input("请输入模式名称: ").strip().lower()

        if pattern_input not in generator.patterns:
            print("无效的模式名称")
            return

        pins_input = input("请输入引脚号（逗号分隔）: ").strip()
        pins = [int(x.strip()) for x in pins_input.split(',')]

        # 验证引脚
        if not generator.validate_pins(pins):
            invalid_pins = [p for p in pins if p not in generator.arduino_pins]
            print(f"无效的引脚: {invalid_pins} (Arduino UNO 数字引脚范围: 0-13)")
            return

        # 检查可用模式
        available_patterns = generator.get_available_patterns(pins)
        if pattern_input not in available_patterns:
            print(f"所选模式 '{pattern_input}' 对于这些引脚不可用")
            print("可用模式:", ", ".join(available_patterns))
            return

        # 生成代码
        code = generator.generate_code(pattern_input, pins)

        print("\n" + "="*60)
        print("生成的 Arduino 代码:")
        print("="*60)
        print(code)
        print("="*60)

        # 保存选项
        save_choice = input("\n是否保存到文件? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = f"led_{pattern_input}_{'_'.join(map(str, pins))}.ino"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"✅ 代码已保存到: {filename}")

    except ValueError as e:
        print(f"❌ 输入错误: {e}")
    except KeyboardInterrupt:
        print("\n\n操作被取消")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()