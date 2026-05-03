#!/usr/bin/env python3
"""
运算放大器示例 3: 运放比较器与积分器响应

本示例演示了运放作为比较器和积分器的工作原理。
比较器用于比较两个电压并输出高/低电平。
积分器对输入信号进行积分运算，常用于波形变换。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

def op_amp_comparator(Vin, Vref, Vsat_pos=12, Vsat_neg=-12):
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
    if isinstance(Vin, np.ndarray):
        Vout = np.where(Vin > Vref, Vsat_pos, Vsat_neg)
    else:
        Vout = Vsat_pos if Vin > Vref else Vsat_neg
    return Vout

def op_amp_integrator(R, C, Vin_func, t_start=0, t_end=0.01, num_points=1000):
    """
    运放积分器仿真

    参数:
    R: 输入电阻 (欧姆)
    C: 积分电容 (法拉)
    Vin_func: 输入电压函数，接受时间t作为参数
    t_start: 开始时间 (秒)
    t_end: 结束时间 (秒)
    num_points: 采样点数

    返回:
    t_array: 时间数组
    Vout_array: 输出电压数组
    """
    t_array = np.linspace(t_start, t_end, num_points)
    tau = R * C  # 时间常数

    # 计算积分
    Vout_array = np.zeros_like(t_array)
    for i, t in enumerate(t_array):
        if i == 0:
            Vout_array[i] = 0  # 初始条件
        else:
            # 数值积分: Vout = -1/(RC) * ∫Vin dt
            dt = t_array[i] - t_array[i-1]
            Vout_array[i] = Vout_array[i-1] - (1/tau) * Vin_func(t) * dt

    return t_array, Vout_array

def simulate_square_wave_integrator():
    """
    仿真方波输入的积分器响应（产生三角波）
    """
    R = 10000      # 10kΩ
    C = 1e-6       # 1μF

    # 方波输入函数
    def square_wave(t, freq=100, amplitude=1):
        period = 1/freq
        if (t % period) < period/2:
            return amplitude
        else:
            return -amplitude

    t, Vout = op_amp_integrator(R, C, square_wave, t_end=0.03)

    # 输入方波
    Vin = np.array([square_wave(ti, freq=100, amplitude=1) for ti in t])

    plt.figure(figsize=(12, 8))

    # 输入信号
    plt.subplot(2, 1, 1)
    plt.plot(t*1000, Vin, 'b-', linewidth=2)
    plt.ylabel('输入电压 Vin (V)')
    plt.title('方波输入')
    plt.grid(True, alpha=0.3)

    # 输出信号（积分结果）
    plt.subplot(2, 1, 2)
    plt.plot(t*1000, Vout, 'r-', linewidth=2)
    plt.xlabel('时间 (ms)')
    plt.ylabel('输出电压 Vout (V)')
    plt.title('积分器输出（三角波）')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def simulate_comparator_with_sine_wave():
    """
    仿真正弦波输入的比较器响应
    """
    t = np.linspace(0, 0.02, 1000)  # 20ms
    Vin = np.sin(2*np.pi*50*t)      # 50Hz 正弦波
    Vref = 0.5                      # 0.5V 参考电压

    Vout = op_amp_comparator(Vin, Vref)

    plt.figure(figsize=(12, 6))
    plt.plot(t*1000, Vin, 'b-', linewidth=2, label='输入正弦波 (50Hz)')
    plt.plot(t*1000, Vout, 'r-', linewidth=2, label='比较器输出')
    plt.axhline(y=Vref, color='g', linestyle='--', label=f'参考电压 = {Vref}V')
    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title('运放比较器响应')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    print("=== 运放比较器示例 ===")
    # 简单比较器测试
    test_Vin = 1.2
    test_Vref = 1.0
    Vout = op_amp_comparator(test_Vin, test_Vref)
    print(f"输入电压: {test_Vin}V, 参考电压: {test_Vref}V")
    print(f"比较器输出: {Vout}V")

    print("\n=== 运放积分器示例 ===")
    print("积分器将方波转换为三角波...")

    # 显示比较器响应
    simulate_comparator_with_sine_wave()

    # 显示积分器响应
    simulate_square_wave_integrator()