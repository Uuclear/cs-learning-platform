import numpy as np
import matplotlib.pyplot as plt

def diode_iv_curve(Vd, Is=1e-12, n=1, Vt=0.026):
    """
    计算二极管的电流-电压特性
    使用肖克利二极管方程: I = Is * (exp(Vd/(n*Vt)) - 1)

    参数:
    Vd: 二极管电压 (V)
    Is: 反向饱和电流 (A)
    n: 发射系数 (理想值为1)
    Vt: 热电压 (V)，室温下约为0.026V
    """
    I = Is * (np.exp(Vd / (n * Vt)) - 1)
    return I

# 创建电压范围
V_forward = np.linspace(0, 1.0, 1000)  # 正向偏置 0-1V
V_reverse = np.linspace(-5, 0, 1000)   # 反向偏置 -5V到0V

# 计算电流
I_forward = diode_iv_curve(V_forward)
I_reverse = diode_iv_curve(V_reverse)

# 绘制伏安特性曲线
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.plot(V_forward, I_forward * 1000, 'b-', linewidth=2)
plt.xlabel('正向电压 (V)')
plt.ylabel('正向电流 (mA)')
plt.title('二极管正向特性')
plt.grid(True, alpha=0.3)
plt.xlim(0, 1.0)
plt.ylim(0, 100)

plt.subplot(1, 2, 2)
plt.plot(V_reverse, I_reverse * 1e9, 'r-', linewidth=2)
plt.xlabel('反向电压 (V)')
plt.ylabel('反向电流 (nA)')
plt.title('二极管反向特性')
plt.grid(True, alpha=0.3)
plt.xlim(-5, 0)
plt.ylim(-10, 0)

plt.tight_layout()
plt.show()

# 打印关键参数
print("二极管特性分析:")
print(f"正向导通电压阈值 (约1mA时): {V_forward[np.abs(I_forward - 0.001).argmin()]:.2f} V")
print(f"反向饱和电流: {np.abs(I_reverse[0]):.2e} A")