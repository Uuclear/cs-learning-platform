#!/usr/bin/env python3
"""
LED限流电阻计算器 - 完整解决方案

这个程序提供了LED电路设计的完整解决方案，
包括多种配置、颜色选择、电源类型和安全考虑。
"""


import json
from typing import Dict, List, Optional


class LED:
    """LED参数类"""
    def __init__(self, name: str, forward_voltage: float, max_current: float,
                 typical_current: float = None):
        self.name = name
        self.forward_voltage = forward_voltage
        self.max_current = max_current
        self.typical_current = typical_current or (max_current * 0.8)

    def __str__(self):
        return f"{self.name} (Vf={self.forward_voltage}V, If_max={self.max_current*1000}mA)"


class PowerSupply:
    """电源类"""
    def __init__(self, name: str, voltage: float, max_current: float = float('inf')):
        self.name = name
        self.voltage = voltage
        self.max_current = max_current

    def __str__(self):
        if self.max_current == float('inf'):
            return f"{self.name} ({self.voltage}V)"
        else:
            return f"{self.name} ({self.voltage}V, {self.max_current*1000}mA max)"


class LEDCircuitDesigner:
    """LED电路设计器"""

    # 常见LED参数数据库
    COMMON_LEDS = {
        'red': LED('红色', 2.0, 0.03, 0.02),
        'green': LED('绿色', 2.1, 0.03, 0.02),
        'yellow': LED('黄色', 2.1, 0.03, 0.02),
        'blue': LED('蓝色', 3.3, 0.03, 0.02),
        'white': LED('白色', 3.3, 0.03, 0.02),
        'uv': LED('紫外', 3.6, 0.03, 0.02),
        'infrared': LED('红外', 1.2, 0.1, 0.05)
    }

    # 常见电源类型
    COMMON_POWER_SUPPLIES = {
        'usb': PowerSupply('USB', 5.0, 0.5),
        'aa_battery': PowerSupply('AA电池', 1.5, 1.0),
        'aaa_battery': PowerSupply('AAA电池', 1.5, 0.5),
        '9v_battery': PowerSupply('9V电池', 9.0, 0.5),
        '12v_supply': PowerSupply('12V电源', 12.0, 2.0),
        '3.3v_supply': PowerSupply('3.3V电源', 3.3, 1.0)
    }

    def __init__(self):
        self.led_database = self.COMMON_LEDS.copy()
        self.power_supply_database = self.COMMON_POWER_SUPPLIES.copy()

    def calculate_resistor(self, supply_voltage: float, led_voltage: float,
                          led_current: float) -> float:
        """
        计算单个LED的限流电阻

        参数:
            supply_voltage: 电源电压 (V)
            led_voltage: LED正向电压 (V)
            led_current: LED工作电流 (A)

        返回:
            所需电阻值 (Ω)
        """
        if supply_voltage <= led_voltage:
            raise ValueError(f"电源电压({supply_voltage}V)必须大于LED电压({led_voltage}V)")

        if led_current <= 0:
            raise ValueError("LED电流必须大于零")

        return (supply_voltage - led_voltage) / led_current

    def calculate_power_rating(self, resistor_value: float, current: float) -> tuple:
        """
        计算电阻功率额定值

        参数:
            resistor_value: 电阻值 (Ω)
            current: 电流 (A)

        返回:
            (实际功耗, 推荐额定功率)
        """
        power = current ** 2 * resistor_value
        # 安全系数：推荐额定功率为实际功耗的2倍
        recommended_rating = power * 2.0
        return power, recommended_rating

    def design_series_circuit(self, supply: PowerSupply, leds: List[LED],
                             use_typical_current: bool = True) -> dict:
        """设计串联LED电路"""
        total_led_voltage = sum(led.forward_voltage for led in leds)

        if supply.voltage <= total_led_voltage:
            raise ValueError(f"电源电压({supply.voltage}V)不足以驱动{len(leds)}个串联LED"
                           f"(需要{total_led_voltage:.1f}V)")

        # 使用典型电流或最大电流
        current = leds[0].typical_current if use_typical_current else leds[0].max_current

        # 验证电源能否提供所需电流
        if current > supply.max_current:
            raise ValueError(f"电源无法提供所需电流({current*1000:.1f}mA > "
                           f"{supply.max_current*1000:.1f}mA)")

        resistor_value = self.calculate_resistor(supply.voltage, total_led_voltage, current)
        power, rating = self.calculate_power_rating(resistor_value, current)

        return {
            'configuration': 'series',
            'num_leds': len(leds),
            'leds': [led.name for led in leds],
            'supply': supply.name,
            'resistor_value': resistor_value,
            'current': current,
            'total_power': supply.voltage * current,
            'resistor_power': power,
            'recommended_resistor_rating': rating,
            'efficiency': total_led_voltage / supply.voltage * 100
        }

    def design_parallel_circuit(self, supply: PowerSupply, leds: List[LED],
                               use_typical_current: bool = True) -> dict:
        """设计并联LED电路"""
        # 验证每个LED都能被电源驱动
        for led in leds:
            if supply.voltage <= led.forward_voltage:
                raise ValueError(f"电源电压({supply.voltage}V)不足以驱动{led.name}"
                               f"({led.forward_voltage}V)")

        # 使用典型电流或最大电流
        current_per_led = leds[0].typical_current if use_typical_current else leds[0].max_current
        total_current = current_per_led * len(leds)

        # 验证电源能否提供总电流
        if total_current > supply.max_current:
            raise ValueError(f"电源无法提供总电流({total_current*1000:.1f}mA > "
                           f"{supply.max_current*1000:.1f}mA)")

        # 每个LED都需要独立的限流电阻
        resistor_value = self.calculate_resistor(supply.voltage, leds[0].forward_voltage,
                                               current_per_led)
        power_per_resistor, rating_per_resistor = self.calculate_power_rating(
            resistor_value, current_per_led)

        total_resistor_power = power_per_resistor * len(leds)

        return {
            'configuration': 'parallel',
            'num_leds': len(leds),
            'leds': [led.name for led in leds],
            'supply': supply.name,
            'resistor_value': resistor_value,
            'resistors_needed': len(leds),
            'current_per_led': current_per_led,
            'total_current': total_current,
            'power_per_resistor': power_per_resistor,
            'recommended_rating_per_resistor': rating_per_resistor,
            'total_resistor_power': total_resistor_power,
            'total_power': supply.voltage * total_current
        }

    def design_optimal_circuit(self, supply: PowerSupply, leds: List[LED],
                              use_typical_current: bool = True) -> dict:
        """设计最优LED电路（混合配置）"""
        if not leds:
            raise ValueError("LED列表不能为空")

        # 如果所有LED相同，尝试最大化串联数量以提高效率
        if len(set(led.forward_voltage for led in leds)) == 1:
            # 所有LED具有相同的正向电压
            led_vf = leds[0].forward_voltage
            max_series_per_string = int(supply.voltage // led_vf)

            if max_series_per_string >= len(leds):
                # 可以全部串联
                return self.design_series_circuit(supply, leds, use_typical_current)
            elif max_series_per_string >= 1:
                # 需要混合配置
                strings_needed = (len(leds) + max_series_per_string - 1) // max_series_per_string
                leds_per_string = min(max_series_per_string, len(leds))

                # 创建虚拟LED列表用于计算（假设所有串长度相同）
                virtual_leds = [leds[0]] * leds_per_string

                string_design = self.design_series_circuit(supply, virtual_leds, use_typical_current)

                total_current = string_design['current'] * strings_needed
                if total_current > supply.max_current:
                    # 电流超限，回退到并联
                    return self.design_parallel_circuit(supply, leds, use_typical_current)

                return {
                    'configuration': 'mixed',
                    'strings': strings_needed,
                    'leds_per_string': leds_per_string,
                    'total_leds': len(leds),
                    'leds': [led.name for led in leds],
                    'supply': supply.name,
                    'resistor_value': string_design['resistor_value'],
                    'resistors_needed': strings_needed,
                    'current_per_string': string_design['current'],
                    'total_current': total_current,
                    'resistor_power': string_design['resistor_power'],
                    'recommended_resistor_rating': string_design['recommended_resistor_rating'],
                    'total_power': supply.voltage * total_current,
                    'efficiency': string_design['efficiency']
                }
            else:
                # 只能并联
                return self.design_parallel_circuit(supply, leds, use_typical_current)
        else:
            # LED不同，只能并联
            return self.design_parallel_circuit(supply, leds, use_typical_current)

    def format_design_result(self, design: dict) -> str:
        """格式化设计结果为可读字符串"""
        result = []
        result.append(f"=== LED电路设计结果 ===")
        result.append(f"配置方式: {design['configuration']}")
        result.append(f"LED类型: {', '.join(design['leds'])}")
        result.append(f"LED数量: {design['num_leds'] if 'num_leds' in design else design.get('total_leds', 0)}")
        result.append(f"电源: {design['supply']}")

        if design['configuration'] == 'series':
            result.append(f"限流电阻: {self.format_resistance(design['resistor_value'])}")
            result.append(f"工作电流: {design['current']*1000:.1f}mA")
            result.append(f"电阻功率: {design['resistor_power']*1000:.2f}mW")
            result.append(f"推荐电阻功率等级: ≥{design['recommended_resistor_rating']*1000:.1f}mW")
            result.append(f"电路效率: {design['efficiency']:.1f}%")

        elif design['configuration'] == 'parallel':
            result.append(f"每个LED的限流电阻: {self.format_resistance(design['resistor_value'])}")
            result.append(f"电阻数量: {design['resistors_needed']}")
            result.append(f"每个LED电流: {design['current_per_led']*1000:.1f}mA")
            result.append(f"总电流: {design['total_current']*1000:.1f}mA")
            result.append(f"每个电阻功率: {design['power_per_resistor']*1000:.2f}mW")
            result.append(f"推荐电阻功率等级: ≥{design['recommended_rating_per_resistor']*1000:.1f}mW")

        elif design['configuration'] == 'mixed':
            result.append(f"串数: {design['strings']}")
            result.append(f"每串LED数: {design['leds_per_string']}")
            result.append(f"每串限流电阻: {self.format_resistance(design['resistor_value'])}")
            result.append(f"电阻总数: {design['resistors_needed']}")
            result.append(f"每串电流: {design['current_per_string']*1000:.1f}mA")
            result.append(f"总电流: {design['total_current']*1000:.1f}mA")
            result.append(f"每个电阻功率: {design['resistor_power']*1000:.2f}mW")
            result.append(f"推荐电阻功率等级: ≥{design['recommended_resistor_rating']*1000:.1f}mW")
            result.append(f"电路效率: {design['efficiency']:.1f}%")

        return "\n".join(result)

    @staticmethod
    def format_resistance(value: float) -> str:
        """格式化电阻值显示"""
        if value >= 1e6:
            return f"{value/1e6:.2f}MΩ"
        elif value >= 1e3:
            return f"{value/1e3:.2f}kΩ"
        else:
            return f"{value:.2f}Ω"


def main():
    """主函数 - 演示完整的LED电路设计"""
    designer = LEDCircuitDesigner()

    print("=== LED限流电阻计算器 - 完整解决方案 ===\n")

    # 示例1: 单色LED设计
    print("1. 单色LED电路设计:")
    try:
        red_led = designer.led_database['red']
        usb_supply = designer.power_supply_database['usb']

        # 串联设计
        series_design = designer.design_series_circuit(usb_supply, [red_led, red_led, red_led])
        print(designer.format_design_result(series_design))
        print()

        # 并联设计
        parallel_design = designer.design_parallel_circuit(usb_supply, [red_led, red_led, red_led])
        print(designer.format_design_result(parallel_design))
        print()

    except Exception as e:
        print(f"错误: {e}\n")

    # 示例2: 多色LED设计
    print("2. 多色LED电路设计:")
    try:
        mixed_leds = [
            designer.led_database['red'],
            designer.led_database['green'],
            designer.led_database['blue']
        ]
        usb_supply = designer.power_supply_database['usb']

        mixed_design = designer.design_optimal_circuit(usb_supply, mixed_leds)
        print(designer.format_design_result(mixed_design))
        print()

    except Exception as e:
        print(f"错误: {e}\n")

    # 示例3: 9V电池供电
    print("3. 9V电池供电设计:")
    try:
        white_led = designer.led_database['white']
        battery_supply = designer.power_supply_database['9v_battery']

        # 设计多个白色LED
        white_leds = [white_led] * 2
        battery_design = designer.design_optimal_circuit(battery_supply, white_leds)
        print(designer.format_design_result(battery_design))
        print()

    except Exception as e:
        print(f"错误: {e}\n")

    # 示例4: 低电压电源
    print("4. 3.3V电源供电:")
    try:
        red_led = designer.led_database['red']
        low_supply = designer.power_supply_database['3.3v_supply']

        low_design = designer.design_optimal_circuit(low_supply, [red_led])
        print(designer.format_design_result(low_design))
        print()

    except Exception as e:
        print(f"错误: {e}\n")

    # 示例5: 添加自定义LED
    print("5. 自定义高功率LED:")
    try:
        # 添加一个高功率白色LED
        high_power_white = LED('高功率白色', 3.2, 0.35, 0.3)  # 350mA最大电流
        designer.led_database['high_power_white'] = high_power_white

        supply_12v = designer.power_supply_database['12v_supply']
        high_power_design = designer.design_optimal_circuit(supply_12v, [high_power_white] * 3)
        print(designer.format_design_result(high_power_design))

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()