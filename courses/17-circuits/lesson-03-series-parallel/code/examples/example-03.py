#!/usr/bin/env python3
"""
LED限流电阻计算器

这个程序帮助计算LED电路中所需的限流电阻值，并提供多种配置选项。
"""


def calculate_led_resistor(supply_voltage, led_voltage, led_current):
    """
    计算单个LED的限流电阻

    参数:
        supply_voltage (float): 电源电压 (V)
        led_voltage (float): LED正向电压 (V)
        led_current (float): LED工作电流 (A)

    返回:
        float: 所需电阻值 (Ω)

    异常:
        ValueError: 当参数不合理时
    """
    if supply_voltage <= led_voltage:
        raise ValueError("电源电压必须大于LED正向电压")

    if led_current <= 0:
        raise ValueError("LED电流必须大于零")

    resistor_value = (supply_voltage - led_voltage) / led_current
    return resistor_value


def calculate_power_rating(resistor_value, current):
    """
    计算电阻所需的功率额定值

    参数:
        resistor_value (float): 电阻值 (Ω)
        current (float): 流过电阻的电流 (A)

    返回:
        float: 功率消耗 (W)
    """
    power = current**2 * resistor_value
    # 通常选择额定功率为实际消耗的2倍以确保安全
    recommended_rating = power * 2
    return power, recommended_rating


def design_multiple_leds(supply_voltage, led_voltage, led_current, num_leds, configuration='series'):
    """
    设计多个LED的电路配置

    参数:
        supply_voltage (float): 电源电压 (V)
        led_voltage (float): 单个LED正向电压 (V)
        led_current (float): 单个LED工作电流 (A)
        num_leds (int): LED数量
        configuration (str): 配置方式 ('series', 'parallel', 'mixed')

    返回:
        dict: 电路设计参数
    """
    if configuration == 'series':
        # 串联：所有LED串联，共享同一个限流电阻
        total_led_voltage = led_voltage * num_leds
        if supply_voltage <= total_led_voltage:
            raise ValueError(f"电源电压({supply_voltage}V)不足以驱动{num_leds}个串联LED(需要{total_led_voltage}V)")

        resistor = calculate_led_resistor(supply_voltage, total_led_voltage, led_current)
        total_current = led_current
        power, rating = calculate_power_rating(resistor, total_current)

        return {
            'configuration': 'series',
            'resistor_value': resistor,
            'total_current': total_current,
            'power_dissipation': power,
            'recommended_rating': rating,
            'notes': f'{num_leds}个LED串联，使用单个限流电阻'
        }

    elif configuration == 'parallel':
        # 并联：每个LED都有自己的限流电阻
        resistor = calculate_led_resistor(supply_voltage, led_voltage, led_current)
        total_current = led_current * num_leds
        power_per_resistor, rating_per_resistor = calculate_power_rating(resistor, led_current)
        total_power = power_per_resistor * num_leds

        return {
            'configuration': 'parallel',
            'resistor_value': resistor,
            'resistors_needed': num_leds,
            'total_current': total_current,
            'power_per_resistor': power_per_resistor,
            'recommended_rating_per_resistor': rating_per_resistor,
            'total_power': total_power,
            'notes': f'{num_leds}个LED并联，每个LED都需要独立的限流电阻'
        }

    elif configuration == 'mixed':
        # 混合：尽可能串联以减少电流，然后并联多组
        max_series_per_string = int(supply_voltage // led_voltage)
        if max_series_per_string < 1:
            raise ValueError("电源电压不足以驱动任何LED")

        if max_series_per_string >= num_leds:
            # 可以全部串联
            return design_multiple_leds(supply_voltage, led_voltage, led_current, num_leds, 'series')
        else:
            # 计算需要多少串
            strings_needed = (num_leds + max_series_per_string - 1) // max_series_per_string
            leds_per_string = min(max_series_per_string, num_leds)

            # 如果最后一串LED数量不同，可能需要调整
            if num_leds % max_series_per_string != 0:
                # 简化处理：假设我们使用相同数量的LED每串，可能会有多余的LED位置
                actual_leds_used = strings_needed * max_series_per_string
                if actual_leds_used > num_leds:
                    # 调整最后一串
                    last_string_leds = num_leds % max_series_per_string
                    if last_string_leds == 0:
                        last_string_leds = max_series_per_string

                    # 这里简化：假设所有串都有max_series_per_string个LED
                    # 实际应用中可能需要为不同长度的串使用不同的电阻
                    leds_per_string = max_series_per_string

            total_string_voltage = led_voltage * leds_per_string
            string_resistor = calculate_led_resistor(supply_voltage, total_string_voltage, led_current)
            total_current = led_current * strings_needed
            power_per_resistor, rating_per_resistor = calculate_power_rating(string_resistor, led_current)

            return {
                'configuration': 'mixed',
                'strings': strings_needed,
                'leds_per_string': leds_per_string,
                'resistor_value': string_resistor,
                'resistors_needed': strings_needed,
                'total_current': total_current,
                'power_per_resistor': power_per_resistor,
                'recommended_rating_per_resistor': rating_per_resistor,
                'notes': f'混合配置：{strings_needed}串，每串{leds_per_string}个LED'
            }

    else:
        raise ValueError(f"不支持的配置方式: {configuration}")


def main():
    """主函数 - 演示LED限流电阻计算"""
    print("=== LED限流电阻计算器演示 ===\n")

    # 示例1: 单个LED
    print("1. 单个LED计算:")
    supply_v = 5.0      # 5V电源
    led_v = 2.0         # 红色LED典型值
    led_i = 0.02        # 20mA

    resistor = calculate_led_resistor(supply_v, led_v, led_i)
    power, rating = calculate_power_rating(resistor, led_i)

    print(f"   电源电压: {supply_v}V")
    print(f"   LED电压: {led_v}V")
    print(f"   LED电流: {led_i*1000}mA")
    print(f"   所需电阻: {resistor}Ω")
    print(f"   功率消耗: {power*1000:.2f}mW")
    print(f"   推荐额定功率: {rating*1000:.2f}mW ({rating:.3f}W)\n")

    # 示例2: 多个LED串联
    print("2. 多个LED串联:")
    num_leds_series = 3
    try:
        series_design = design_multiple_leds(supply_v, led_v, led_i, num_leds_series, 'series')
        print(f"   配置: {series_design['notes']}")
        print(f"   所需电阻: {series_design['resistor_value']:.1f}Ω")
        print(f"   总电流: {series_design['total_current']*1000:.1f}mA")
        print(f"   推荐电阻功率: {series_design['recommended_rating']:.3f}W")
    except ValueError as e:
        print(f"   错误: {e}")
    print()

    # 示例3: 多个LED并联
    print("3. 多个LED并联:")
    num_leds_parallel = 3
    parallel_design = design_multiple_leds(supply_v, led_v, led_i, num_leds_parallel, 'parallel')
    print(f"   配置: {parallel_design['notes']}")
    print(f"   每个电阻: {parallel_design['resistor_value']}Ω")
    print(f"   电阻数量: {parallel_design['resistors_needed']}")
    print(f"   总电流: {parallel_design['total_current']*1000:.1f}mA")
    print(f"   每个电阻推荐功率: {parallel_design['recommended_rating_per_resistor']:.3f}W\n")

    # 示例4: 不同颜色LED
    print("4. 不同颜色LED比较:")
    led_types = {
        '红色': {'voltage': 2.0, 'current': 0.02},
        '绿色': {'voltage': 2.1, 'current': 0.02},
        '蓝色': {'voltage': 3.3, 'current': 0.02},
        '白色': {'voltage': 3.3, 'current': 0.02}
    }

    for color, specs in led_types.items():
        try:
            r = calculate_led_resistor(supply_v, specs['voltage'], specs['current'])
            print(f"   {color}LED: {r}Ω")
        except ValueError as e:
            print(f"   {color}LED: 错误 - {e}")
    print()

    # 示例5: 9V电池供电
    print("5. 9V电池供电示例:")
    battery_supply = 9.0
    num_blue_leds = 2

    try:
        blue_series = design_multiple_leds(battery_supply, 3.3, 0.02, num_blue_leds, 'series')
        print(f"   2个蓝色LED串联:")
        print(f"   所需电阻: {blue_series['resistor_value']:.1f}Ω")
        print(f"   总电流: {blue_series['total_current']*1000:.1f}mA")
        print(f"   9V电池理论续航: {200/(blue_series['total_current']*1000):.1f}小时")
        # 假设9V电池容量为200mAh
    except ValueError as e:
        print(f"   错误: {e}")


if __name__ == "__main__":
    main()