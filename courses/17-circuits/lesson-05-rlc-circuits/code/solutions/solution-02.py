import numpy as np
import matplotlib.pyplot as plt

def rlc_response(R, L, C, V0=1, t_max=10):
    """计算RLC电路的响应"""
    alpha = R / (2 * L)
    omega0 = 1 / np.sqrt(L * C)

    t = np.linspace(0, t_max, 1000)

    if alpha > omega0:  # 过阻尼
        s1 = -alpha + np.sqrt(alpha**2 - omega0**2)
        s2 = -alpha - np.sqrt(alpha**2 - omega0**2)
        v_t = V0 * (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1)
        case = "过阻尼"
    elif alpha == omega0:  # 临界阻尼
        v_t = V0 * (1 + alpha * t) * np.exp(-alpha * t)
        case = "临界阻尼"
    else:  # 欠阻尼
        omega_d = np.sqrt(omega0**2 - alpha**2)
        v_t = V0 * np.exp(-alpha * t) * (np.cos(omega_d * t) + (alpha/omega_d) * np.sin(omega_d * t))
        case = "欠阻尼"

    return t, v_t, case

# 绘制三种阻尼状态
L, C = 1, 1  # 电感1H，电容1F
R_values = [3, 2, 0.5]  # 对应过阻尼、临界阻尼、欠阻尼

plt.figure(figsize=(12, 8))
for i, R in enumerate(R_values):
    t, v_t, case = rlc_response(R, L, C)
    plt.subplot(3, 1, i+1)
    plt.plot(t, v_t)
    plt.title(f'RLC电路响应 - {case} (R={R}Ω, L={L}H, C={C}F)')
    plt.xlabel('时间 (s)')
    plt.ylabel('电压 (V)')
    plt.grid(True)

    # 标记关键点
    if case == "欠阻尼":
        # 找到第一个峰值
        peak_idx = np.argmax(v_t[:200])  # 在前200个点中找峰值
        plt.plot(t[peak_idx], v_t[peak_idx], 'ro', markersize=8, label=f'第一个峰值')
        plt.legend()

plt.tight_layout()
plt.show()

# 验证临界阻尼条件
print("临界阻尼条件验证：")
print(f"对于 L={L}H, C={C}F")
print(f"临界电阻 R_critical = 2*sqrt(L/C) = {2*np.sqrt(L/C):.2f}Ω")
print(f"我们使用的临界阻尼电阻 R = {R_values[1]}Ω")