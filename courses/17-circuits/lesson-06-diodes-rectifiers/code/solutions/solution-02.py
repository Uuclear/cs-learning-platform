import numpy as np
import matplotlib.pyplot as plt

def analyze_rectifier_circuits():
    """
    分析半波和全波整流电路的性能
    """
    # 电路参数
    V_rms = 10  # 输入RMS电压
    V_peak = V_rms * np.sqrt(2)  # 峰值电压
    f = 50  # 频率 (Hz)

    # 时间向量
    t = np.linspace(0, 0.1, 2000)  # 0.1秒，高分辨率

    # 输入信号
    V_in = V_peak * np.sin(2 * np.pi * f * t)

    # 半波整流（考虑二极管压降）
    Vd = 0.7  # 硅二极管正向压降
    V_half_wave = np.where(V_in > Vd, V_in - Vd, 0)

    # 全波整流（考虑两个二极管压降）
    V_full_wave = np.where(np.abs(V_in) > Vd, np.abs(V_in) - Vd, 0)

    # 计算理论值
    V_half_avg_theoretical = (V_peak - Vd) / np.pi
    V_full_avg_theoretical = 2 * (V_peak - Vd) / np.pi

    V_half_rms_theoretical = (V_peak - Vd) / 2
    V_full_rms_theoretical = (V_peak - Vd) / np.sqrt(2)

    # 计算实际值
    V_half_avg_actual = np.mean(V_half_wave)
    V_full_avg_actual = np.mean(V_full_wave)

    V_half_rms_actual = np.sqrt(np.mean(V_half_wave**2))
    V_full_rms_actual = np.sqrt(np.mean(V_full_wave**2))

    # 绘图
    plt.figure(figsize=(14, 10))

    # 输入信号
    plt.subplot(3, 1, 1)
    plt.plot(t * 1000, V_in, 'b-', linewidth=2, label=f'输入交流 ({V_rms}V RMS)')
    plt.axhline(y=Vd, color='r', linestyle='--', alpha=0.7, label='二极管阈值')
    plt.axhline(y=-Vd, color='r', linestyle='--', alpha=0.7)
    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title('输入交流信号')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # 半波整流
    plt.subplot(3, 1, 2)
    plt.plot(t * 1000, V_half_wave, 'r-', linewidth=2, label='半波整流输出')
    plt.axhline(y=V_half_avg_actual, color='g', linestyle='--',
                label=f'平均值: {V_half_avg_actual:.2f}V')
    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title(f'半波整流 (理论平均: {V_half_avg_theoretical:.2f}V)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # 全波整流
    plt.subplot(3, 1, 3)
    plt.plot(t * 1000, V_full_wave, 'g-', linewidth=2, label='全波整流输出')
    plt.axhline(y=V_full_avg_actual, color='purple', linestyle='--',
                label=f'平均值: {V_full_avg_actual:.2f}V')
    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title(f'全波整流 (理论平均: {V_full_avg_theoretical:.2f}V)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

    # 输出分析结果
    print("整流电路性能分析:")
    print("=" * 50)
    print(f"输入参数: {V_rms}V RMS, {f}Hz, 二极管压降: {Vd}V")
    print()
    print("半波整流:")
    print(f"  理论平均输出: {V_half_avg_theoretical:.2f}V")
    print(f"  实际平均输出: {V_half_avg_actual:.2f}V")
    print(f"  理论有效值:   {V_half_rms_theoretical:.2f}V")
    print(f"  实际有效值:   {V_half_rms_actual:.2f}V")
    print()
    print("全波整流:")
    print(f"  理论平均输出: {V_full_avg_theoretical:.2f}V")
    print(f"  实际平均输出: {V_full_avg_actual:.2f}V")
    print(f"  理论有效值:   {V_full_rms_theoretical:.2f}V")
    print(f"  实际有效值:   {V_full_rms_actual:.2f}V")
    print()
    print(f"效率比较: 全波整流平均输出是半波整流的 {V_full_avg_actual/V_half_avg_actual:.1f} 倍")
    print(f"纹波频率: 半波={f}Hz, 全波={2*f}Hz")

# 运行分析
analyze_rectifier_circuits()