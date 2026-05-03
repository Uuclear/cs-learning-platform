import numpy as np
import matplotlib.pyplot as plt

# 生成输入交流信号
t = np.linspace(0, 0.1, 1000)  # 0.1秒，足够显示几个周期
f = 50  # 50Hz交流电
V_in = 10 * np.sin(2 * np.pi * f * t)  # 10V峰值的正弦波

# 半波整流
V_half_wave = np.where(V_in > 0, V_in, 0)

# 全波整流（假设使用中心抽头变压器，输出幅度相同）
V_full_wave = np.abs(V_in)

# 创建图形
plt.figure(figsize=(12, 8))

# 输入交流信号
plt.subplot(3, 1, 1)
plt.plot(t * 1000, V_in, 'b-', linewidth=2, label='输入交流信号')
plt.xlabel('时间 (ms)')
plt.ylabel('电压 (V)')
plt.title('输入交流信号')
plt.grid(True, alpha=0.3)
plt.legend()

# 半波整流输出
plt.subplot(3, 1, 2)
plt.plot(t * 1000, V_half_wave, 'r-', linewidth=2, label='半波整流输出')
plt.xlabel('时间 (ms)')
plt.ylabel('电压 (V)')
plt.title('半波整流')
plt.grid(True, alpha=0.3)
plt.legend()

# 全波整流输出
plt.subplot(3, 1, 3)
plt.plot(t * 1000, V_full_wave, 'g-', linewidth=2, label='全波整流输出')
plt.xlabel('时间 (ms)')
plt.ylabel('电压 (V)')
plt.title('全波整流')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# 计算平均值和有效值
V_half_avg = np.mean(V_half_wave)
V_full_avg = np.mean(V_full_wave)

V_half_rms = np.sqrt(np.mean(V_half_wave**2))
V_full_rms = np.sqrt(np.mean(V_full_wave**2))

print("整流电路性能比较:")
print(f"半波整流平均输出电压: {V_half_avg:.2f} V")
print(f"全波整流平均输出电压: {V_full_avg:.2f} V")
print(f"半波整流有效值: {V_half_rms:.2f} V")
print(f"全波整流有效值: {V_full_rms:.2f} V")
print(f"全波整流效率是半波整流的: {V_full_avg/V_half_avg:.1f} 倍")