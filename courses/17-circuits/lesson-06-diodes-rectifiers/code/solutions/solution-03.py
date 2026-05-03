import numpy as np
import matplotlib.pyplot as plt

def advanced_bridge_rectifier_simulation(V_ac_rms=12, f=50, C=2200e-6, R_load=100,
                                       include_diode_drop=True, Vd=0.7):
    """
    高级桥式整流电路仿真，包含二极管压降和负载变化

    参数:
    V_ac_rms: 交流输入RMS电压 (V)
    f: 频率 (Hz)
    C: 滤波电容 (F)
    R_load: 负载电阻 (Ω)
    include_diode_drop: 是否考虑二极管压降
    Vd: 二极管正向压降 (V)
    """
    # 计算峰值电压
    V_peak = V_ac_rms * np.sqrt(2)

    # 时间参数
    T = 1.0 / f
    dt = T / 1000  # 高时间分辨率
    t_end = 4 * T  # 仿真4个周期
    t = np.arange(0, t_end, dt)

    # 输入交流电压
    V_ac = V_peak * np.sin(2 * np.pi * f * t)

    # 桥式整流（考虑二极管压降）
    if include_diode_drop:
        V_rect_raw = np.abs(V_ac) - 2 * Vd  # 桥式整流有两个二极管导通
        V_rectified = np.maximum(V_rect_raw, 0)
    else:
        V_rectified = np.abs(V_ac)

    # 仿真RC滤波电路
    V_out = np.zeros_like(t)
    I_load = np.zeros_like(t)
    I_cap = np.zeros_like(t)

    for i in range(1, len(t)):
        dt_step = t[i] - t[i-1]

        # 负载电流
        I_load[i-1] = V_out[i-1] / R_load if R_load > 0 else 0

        # 如果整流电压高于输出电压，二极管导通，电容充电
        if V_rectified[i] > V_out[i-1]:
            V_out[i] = V_rectified[i]
            # 电容充电电流（近似）
            I_cap[i-1] = max((V_rectified[i] - V_out[i-1]) / (dt_step * 1e-3), 0)  # 简化模型
        else:
            # 二极管截止，电容通过负载放电
            tau = R_load * C
            V_out[i] = V_out[i-1] * np.exp(-dt_step / tau)
            I_cap[i-1] = -I_load[i-1]  # 电容放电电流等于负载电流的负值

    # 计算最后几个周期的纹波
    last_cycles = int(2 * T / dt)
    V_out_last = V_out[-last_cycles:]
    V_max = np.max(V_out_last)
    V_min = np.min(V_out_last)
    V_ripple = V_max - V_min
    V_dc_avg = np.mean(V_out_last)

    # 理论计算对比
    if include_diode_drop:
        V_rect_avg_theoretical = 2 * (V_peak - 2 * Vd) / np.pi
    else:
        V_rect_avg_theoretical = 2 * V_peak / np.pi

    V_ripple_theoretical = V_dc_avg / (2 * f * R_load * C)

    return {
        't': t,
        'V_ac': V_ac,
        'V_rectified': V_rectified,
        'V_out': V_out,
        'V_ripple': V_ripple,
        'V_dc_avg': V_dc_avg,
        'V_ripple_theoretical': V_ripple_theoretical,
        'V_rect_avg_theoretical': V_rect_avg_theoretical
    }

# 仿真不同负载条件下的性能
load_conditions = [
    {'R_load': 1000, 'name': '轻载 (1kΩ)'},
    {'R_load': 220, 'name': '中等负载 (220Ω)'},
    {'R_load': 100, 'name': '重载 (100Ω)'}
]

C_value = 2200e-6  # 2200μF

plt.figure(figsize=(15, 12))

for idx, condition in enumerate(load_conditions):
    result = advanced_bridge_rectifier_simulation(
        V_ac_rms=12, f=50, C=C_value, R_load=condition['R_load']
    )

    plt.subplot(3, 1, idx+1)
    plt.plot(result['t'] * 1000, result['V_rectified'], 'r--', alpha=0.6,
             label='整流后')
    plt.plot(result['t'] * 1000, result['V_out'], 'b-', linewidth=2,
             label=f"滤波输出 (纹波={result['V_ripple']:.2f}V)")
    plt.axhline(y=result['V_dc_avg'], color='g', linestyle=':',
                label=f"平均值: {result['V_dc_avg']:.2f}V")

    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title(f"{condition['name']} - C={C_value*1e6:.0f}μF")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(16, 24)  # 显示一个完整周期

plt.tight_layout()
plt.show()

# 输出详细分析
print("桥式整流电源设计分析:")
print("=" * 60)
print(f"输入: 12V RMS, 50Hz, C={C_value*1e6:.0f}μF")
print()

for condition in load_conditions:
    result = advanced_bridge_rectifier_simulation(
        V_ac_rms=12, f=50, C=C_value, R_load=condition['R_load']
    )

    print(f"{condition['name']}:")
    print(f"  输出平均电压: {result['V_dc_avg']:.2f}V")
    print(f"  纹波电压:     {result['V_ripple']:.2f}V ({result['V_ripple']/result['V_dc_avg']*100:.1f}%)")
    print(f"  理论纹波:     {result['V_ripple_theoretical']:.2f}V")
    print(f"  负载电流:     {result['V_dc_avg']/condition['R_load']*1000:.1f}mA")
    print()

# 设计建议
print("设计建议:")
print("• 对于小电流应用 (<100mA)，2200μF电容通常足够")
print("• 对于大电流应用，需要更大的电容或额外的稳压电路")
print("• 实际设计中还需考虑变压器内阻、二极管动态特性等因素")
print("• 建议在关键应用中使用线性稳压器或开关稳压器进一步稳定输出")