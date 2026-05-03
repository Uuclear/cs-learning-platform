import numpy as np
import matplotlib.pyplot as plt

def calculate_resonance_and_q(L, C, R):
    """计算RLC电路的谐振频率和品质因数"""
    # 谐振角频率 (rad/s)
    omega0 = 1 / np.sqrt(L * C)
    # 谐振频率 (Hz)
    f0 = omega0 / (2 * np.pi)
    # 品质因数
    Q = omega0 * L / R

    return f0, Q

def plot_frequency_response(L, C, R_values, f_range=(1e3, 1e7)):
    """绘制不同R值下的频率响应曲线"""
    f = np.logspace(np.log10(f_range[0]), np.log10(f_range[1]), 1000)
    omega = 2 * np.pi * f

    plt.figure(figsize=(12, 8))

    for i, R in enumerate(R_values):
        # 串联RLC阻抗
        Z = R + 1j * (omega * L - 1 / (omega * C))
        # 电流幅度（假设电压源为1V）
        I_mag = 1 / np.abs(Z)

        plt.subplot(2, 2, i+1)
        plt.semilogx(f, I_mag)
        f0, Q = calculate_resonance_and_q(L, C, R)
        plt.axvline(x=f0, color='r', linestyle='--', label=f'f₀={f0/1e6:.2f}MHz')
        plt.title(f'频率响应 - R={R}Ω, Q={Q:.2f}')
        plt.xlabel('频率 (Hz)')
        plt.ylabel('电流幅度 (A)')
        plt.grid(True)
        plt.legend()

    plt.tight_layout()
    plt.show()

# 示例参数
L = 10e-6  # 10μH
C = 100e-12  # 100pF
R_values = [1, 5, 20]  # 不同电阻值

# 计算谐振频率和品质因数
for R in R_values:
    f0, Q = calculate_resonance_and_q(L, C, R)
    print(f"R = {R}Ω: 谐振频率 = {f0/1e6:.2f} MHz, 品质因数 Q = {Q:.2f}")

# 绘制频率响应
plot_frequency_response(L, C, R_values)