import numpy as np
import matplotlib.pyplot as plt

def bridge_rectifier_with_filter(V_ac_peak, f, C, R_load, dt=1e-5):
    """
    仿真桥式整流电路带滤波电容的输出

    参数:
    V_ac_peak: 交流输入峰值电压 (V)
    f: 交流频率 (Hz)
    C: 滤波电容 (F)
    R_load: 负载电阻 (Ω)
    dt: 时间步长 (s)
    """
    # 时间参数
    T = 1.0 / f  # 周期
    t_end = 5 * T  # 仿真5个周期
    t = np.arange(0, t_end, dt)

    # 输入交流电压
    V_in = V_ac_peak * np.sin(2 * np.pi * f * t)

    # 桥式整流（全波整流）
    V_rectified = np.abs(V_in)

    # 仿真滤波电容的充放电过程
    V_out = np.zeros_like(t)
    V_out[0] = 0

    for i in range(1, len(t)):
        dt_step = t[i] - t[i-1]

        # 如果整流电压高于输出电压，电容充电
        if V_rectified[i] > V_out[i-1]:
            V_out[i] = V_rectified[i]
        else:
            # 电容通过负载放电
            tau = R_load * C
            V_out[i] = V_out[i-1] * np.exp(-dt_step / tau)

    return t, V_in, V_rectified, V_out

# 电路参数
V_ac_peak = 10  # 10V峰值
f = 50          # 50Hz
C_values = [100e-6, 1000e-6, 10000e-6]  # 不同电容值：100μF, 1000μF, 10000μF
R_load = 1000   # 1kΩ负载

# 创建图形
plt.figure(figsize=(15, 10))

for idx, C in enumerate(C_values):
    t, V_in, V_rectified, V_out = bridge_rectifier_with_filter(V_ac_peak, f, C, R_load)

    # 计算纹波电压
    V_max = np.max(V_out[-int(1/(f*1e-5)):])  # 最后一个周期的最大值
    V_min = np.min(V_out[-int(1/(f*1e-5)):])  # 最后一个周期的最小值
    V_ripple = V_max - V_min

    plt.subplot(3, 1, idx+1)
    plt.plot(t * 1000, V_rectified, 'r--', alpha=0.7, label='整流后（无滤波）')
    plt.plot(t * 1000, V_out, 'b-', linewidth=2, label=f'滤波后 (C={C*1e6:.0f}μF)')
    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title(f'桥式整流 + 滤波电容 (C={C*1e6:.0f}μF, 纹波={V_ripple:.2f}V)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(16, 24)  # 显示一个完整的周期

plt.tight_layout()
plt.show()

# 理论纹波计算对比
print("理论与仿真纹波对比:")
for C in C_values:
    # 理论纹波公式：V_ripple ≈ V_dc / (2 * f * R * C)
    V_dc_theoretical = V_ac_peak * 0.9  # 全波整流的平均值约等于0.9 * V_rms
    V_ripple_theoretical = V_dc_theoretical / (2 * f * R_load * C)

    # 仿真纹波
    _, _, _, V_out_sim = bridge_rectifier_with_filter(V_ac_peak, f, C, R_load)
    V_max_sim = np.max(V_out_sim[-int(1/(f*1e-5)):])
    V_min_sim = np.min(V_out_sim[-int(1/(f*1e-5)):])
    V_ripple_sim = V_max_sim - V_min_sim

    print(f"C={C*1e6:.0f}μF: 理论纹波={V_ripple_theoretical:.2f}V, 仿真纹波={V_ripple_sim:.2f}V")