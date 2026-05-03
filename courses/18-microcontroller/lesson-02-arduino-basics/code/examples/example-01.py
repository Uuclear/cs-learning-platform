#!/usr/bin/env python3
"""
LED 限流电阻计算器

这个脚本帮助计算点亮 LED 所需的限流电阻值。
用户输入电源电压、LED 电压降和期望的工作电流，
程序会计算出合适的电阻值并推荐标准电阻。

使用方法：
    python example-01.py
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
    # 将 mA 转换为 A
    current_a = desired_current_ma / 1000.0

    # 使用欧姆定律计算电阻值
    # R = (V_supply - V_led) / I
    resistor_value = (voltage_supply - led_voltage_drop) / current_a

    return resistor_value

def find_closest_standard_resistor(calculated_value):
    """
    找到最接近的标准电阻值

    参数:
        calculated_value (float): 计算出的电阻值

    返回:
        tuple: (标准电阻值, 误差百分比)
    """
    # E12 系列标准电阻值 (常用值)
    standard_values = [
        10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82,
        100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820,
        1000, 1200, 1500, 1800, 2200, 2700, 3300, 3900, 4700, 5600, 6800, 8200,
        10000, 12000, 15000, 18000, 22000, 27000, 33000, 39000, 47000, 56000, 68000, 82000,
        100000, 120000, 150000, 180000, 220000, 270000, 330000, 390000, 470000, 560000, 680000, 820000,
        1000000
    ]

    closest_value = None
    min_difference = float('inf')

    for value in standard_values:
        difference = abs(value - calculated_value)
        if difference < min_difference:
            min_difference = difference
            closest_value = value

    # 计算误差百分比
    error_percentage = (abs(closest_value - calculated_value) / calculated_value) * 100

    return closest_value, error_percentage

def main():
    """主函数"""
    print("=== LED 限流电阻计算器 ===")
    print()

    try:
        # 获取用户输入
        voltage_supply = float(input("请输入电源电压 (V，例如 5): "))
        led_voltage_drop = float(input("请输入 LED 电压降 (V，红色约 2.0，蓝色约 3.2): "))
        desired_current_ma = float(input("请输入期望的 LED 工作电流 (mA，通常 5-20): "))

        # 验证输入
        if voltage_supply <= 0:
            print("错误：电源电压必须大于 0V")
            return

        if led_voltage_drop <= 0 or led_voltage_drop >= voltage_supply:
            print(f"错误：LED 电压降必须大于 0V 且小于电源电压 ({voltage_supply}V)")
            return

        if desired_current_ma <= 0:
            print("错误：工作电流必须大于 0mA")
            return

        # 计算电阻值
        calculated_resistor = calculate_resistor(voltage_supply, led_voltage_drop, desired_current_ma)

        # 找到最接近的标准电阻
        standard_resistor, error_percent = find_closest_standard_resistor(calculated_resistor)

        # 显示结果
        print("\n=== 计算结果 ===")
        print(f"计算出的电阻值: {calculated_resistor:.2f} Ω")
        print(f"推荐的标准电阻: {standard_resistor} Ω")
        print(f"误差: {error_percent:.2f}%")

        # 安全检查
        actual_current = (voltage_supply - led_voltage_drop) / (standard_resistor / 1000.0)
        print(f"实际工作电流: {actual_current:.2f} mA")

        if actual_current > 30:
            print("⚠️  警告：实际电流可能过高，建议使用更大的电阻值！")
        elif actual_current < 2:
            print("💡 提示：实际电流较低，LED 可能不够亮")
        else:
            print("✅ 电流在安全范围内")

    except ValueError:
        print("错误：请输入有效的数字")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    main()