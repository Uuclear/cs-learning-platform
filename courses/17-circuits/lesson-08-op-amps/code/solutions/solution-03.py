#!/usr/bin/env python3
"""
运算放大器解决方案 3: 运放比较器与积分器响应

完整实现比较器和积分器的仿真，包括实际应用示例。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

def op_amp_comparator(Vin, Vref, Vsat_pos=15, Vsat_neg=-15):
    """
    运放比较器仿真

    参数:
    Vin: 输入电压 (伏特)
    Vref: 参考电压 (伏特)
    Vsat_pos: 正饱和电压 (伏特)
    Vsat_neg: 负饱和电压 (伏特)

    返回:
    输出电压 (伏特)
    """
    if np.isscalar(Vin):
        return Vsat_pos if Vin > Vref else Vsat_neg
    else:
        return np.where(Vin > Vref, Vsat_pos, Vsat_neg)

def op_amp_integrator(R, C, Vin_array, t_array):
    """
    运放积分器数值仿真

    参数:
    R: 输入电阻 (欧姆)
    C: 积分电容 (法拉)
    Vin_array: 输入电压数组
    t_array: 时间数组

    返回:
    Vout_array: 输出电压数组
    """
    tau = R * C
    Vout_array = np.zeros_like(Vin_array)

    # 数值积分: Vout(t) = -1/(RC) * ∫Vin(t)dt
    for i in range(1, len(t_array)):
        dt = t_array[i] - t_array[i-1]
        Vout_array[i] = Vout_array[i-1] - (1/tau) * Vin_array[i-1] * dt

    return Vout_array

def practical_comparator_application():
    """
    实际比较器应用：温度传感器信号处理
    """
    # 模拟温度传感器输出（0-5V 对应 0-100°C）
    temperatures = np.linspace(0, 100, 200)
    sensor_output = temperatures * 0.05  # 0.05V/°C

    # 设置阈值：70°C 对应 3.5V
    threshold_temp = 70
    threshold_voltage = threshold_temp * 0.05

    # 比较器输出
    comparator_output = op_amp_comparator(sensor_output, threshold_voltage)

    # 绘图
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(temperatures, sensor_output, 'b-', linewidth=2, label='传感器输出')
    plt.axhline(y=threshold_voltage, color='r', linestyle='--',
                label=f'阈值 = {threshold_voltage}V ({threshold_temp}°C)')
    plt.xlabel('温度 (°C)')
    plt.ylabel('电压 (V)')
    plt.title('温度传感器输出')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(temperatures, comparator_output, 'r-', linewidth=2, label='比较器输出')
    plt.xlabel('温度 (°C)')
    plt.ylabel('输出电压 (V)')
    plt.title('比较器输出（温度报警）')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

def integrator_waveform_transformation():
    """
    积分器波形变换应用
    """
    # 时间设置
    t = np.linspace(0, 0.02, 1000)  # 20ms

    # 不同输入信号
    sine_input = np.sin(2*np.pi*100*t)           # 100Hz 正弦波
    square_input = np.sign(np.sin(2*np.pi*50*t)) # 50Hz 方波

    # 积分器参数
    R = 10000    # 10kΩ
    C = 1e-6     # 1μF

    # 积分计算
    sine_integral = op_amp_integrator(R, C, sine_input, t)
    square_integral = op_amp_integrator(R, C, square_input, t)

    # 绘图
    plt.figure(figsize=(14, 10))

    # 正弦波积分
    plt.subplot(2, 2, 1)
    plt.plot(t*1000, sine_input, 'b-', linewidth=2)
    plt.title('正弦波输入 (100Hz)')
    plt.ylabel('Vin (V)')
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 2)
    plt.plot(t*1000, -sine_integral, 'r-', linewidth=2)  # 负号因为反相积分
    plt.title('积分器输出（余弦波）')
    plt.ylabel('Vout (V)')
    plt.grid(True, alpha=0.3)

    # 方波积分
    plt.subplot(2, 2, 3)
    plt.plot(t*1000, square_input, 'b-', linewidth=2)
    plt.title('方波输入 (50Hz)')
    plt.xlabel('时间 (ms)')
    plt.ylabel('Vin (V)')
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 4)
    plt.plot(t*1000, -square_integral, 'r-', linewidth=2)
    plt.title('积分器输出（三角波）')
    plt.xlabel('时间 (ms)')
    plt.ylabel('Vout (V)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== 运放比较器与积分器完整解决方案 ===")

    # 比较器应用示例
    print("\n1. 温度传感器比较器应用:")
    practical_comparator_application()

    # 积分器应用示例
    print("\n2. 积分器波形变换应用:")
    integrator_waveform_transformation()

    # 基本功能验证
    print("\n3. 基本功能验证:")
    test_Vin = 2.3
    test_Vref = 2.0
    Vout = op_amp_comparator(test_Vin, test_Vref)
    print(f"比较器测试: Vin={test_Vin}V, Vref={test_Vref}V → Vout={Vout}V")