#!/usr/bin/env python3
"""
LED 限流电阻计算器 - 完整解决方案

这个脚本帮助计算点亮 LED 所需的限流电阻值，
并提供详细的电路参数分析。
"""

def calculate_resistor(voltage_supply, led_voltage_drop, desired_current_ma):
    """
    计算 LED 限流电阻值

    参数:
        voltage_supply (float): 电源电压 (V)
        led_voltage_drop (float): LED 电压降 (V)
        desired_current_ma (float): 期望的 LED 工作电流 (mA)

    返回:
        float: 所需的电阻值 (Ω)
    """
    if desired_current_ma <= 0:
        raise ValueError("工作电流必须大于 0")

    if led_voltage_drop >= voltage_supply:
        raise ValueError("LED 电压降不能大于或等于电源电压")

    current_a = desired_current_ma / 1000.0
    resistor_value = (voltage_supply - led_voltage_drop) / current_a
    return resistor_value

def find_closest_standard_resistor(calculated_value):
    """
    找到最接近的标准电阻值（E12 系列）
    """
    standard_values = [
        10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82,
        100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820,
        1000, 1200, 1500, 1800, 2200, 2700, 3300, 3900, 4700, 5600, 6800, 8200,
        10000, 12000, 15000, 18000, 22000, 27000, 33000, 39000, 47000, 56000, 68000, 82000,
        100000, 120000, 150000, 180000, 220000, 270000, 330000, 390000, 470000, 560000, 680000, 820000,
        1000000
    ]

    closest_value = min(standard_values, key=lambda x: abs(x - calculated_value))
    error_percentage = abs(closest_value - calculated_value) / calculated_value * 100

    return closest_value, error_percentage

def get_led_voltage_drop(color):
    """根据 LED 颜色返回典型电压降"""
    voltage_drops = {
        'red': 2.0,
        'orange': 2.1,
        'yellow': 2.1,
        'green': 2.2,
        'blue': 3.2,
        'white': 3.2,
        'purple': 3.0
    }
    return voltage_drops.get(color.lower(), 2.0)

def main():
    print("=== LED 限流电阻计算器 ===")
    print()

    try:
        # 获取输入
        voltage_supply = float(input("电源电压 (V): "))

        # 支持颜色输入或直接电压降输入
        color_or_voltage = input("LED 颜色 (red/blue/green/white) 或电压降 (V): ")
        try:
            led_voltage_drop = float(color_or_voltage)
        except ValueError:
            led_voltage_drop = get_led_voltage_drop(color_or_voltage)
            print(f"使用 {color_or_voltage} LED 的典型电压降: {led_voltage_drop}V")

        desired_current_ma = float(input("期望工作电流 (mA): "))

        # 计算
        calculated_resistor = calculate_resistor(voltage_supply, led_voltage_drop, desired_current_ma)
        standard_resistor, error_percent = find_closest_standard_resistor(calculated_resistor)
        actual_current = (voltage_supply - led_voltage_drop) / (standard_resistor / 1000.0)

        # 输出结果
        print("\n=== 结果 ===")
        print(f"计算电阻值: {calculated_resistor:.2f} Ω")
        print(f"推荐标准电阻: {standard_resistor} Ω")
        print(f"实际工作电流: {actual_current:.2f} mA")
        print(f"误差: {error_percent:.2f}%")

        # 安全提示
        if actual_current > 25:
            print("⚠️  警告: 电流过高，可能损坏 LED!")
        elif actual_current < 3:
            print("💡 提示: 电流较低，LED 可能不够亮")
        else:
            print("✅ 电流在安全范围内 (3-25mA)")

    except ValueError as e:
        print(f"输入错误: {e}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()