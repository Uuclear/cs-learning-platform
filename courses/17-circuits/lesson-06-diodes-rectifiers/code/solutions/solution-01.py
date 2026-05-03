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
    # 处理数值溢出问题
    with np.errstate(over='ignore'):
        I = Is * (np.exp(np.clip(Vd / (n * Vt), -700, 700)) - 1)
    return I

# 创建电压范围
V_forward = np.linspace(0, 1.0, 1000)  # 正向偏置 0-1V
V_reverse = np.linspace(-5, 0, 1000)   # 反向偏置 -5V到0V

# 计算电流
I_forward = diode_iv_curve(V_forward)
I_reverse = diode_iv_curve(V_reverse)

# 绘制伏安特性曲线
plt.figure(figsize=(12, 5))

# 正向特性（对数坐标）
plt.subplot(1, 2, 1)
plt.semilogy(V_forward, np.abs(I_forward) + 1e-15, 'b-', linewidth=2)
plt.xlabel('正向电压 (V)')
plt.ylabel('正向电流 (A) - 对数坐标')
plt.title('二极管正向特性（对数坐标）')
plt.grid(True, alpha=0.3)
plt.xlim(0, 1.0)

# 反向特性（线性坐标，放大显示）
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

# 分析关键参数
V_threshold = V_forward[np.abs(I_forward - 0.001).argmin()]  # 1mA时的电压
I_reverse_sat = np.mean(I_reverse[-100:])  # 平均反向饱和电流

print("二极管特性分析结果:")
print(f"正向导通阈值电压 (1mA): {V_threshold:.2f} V")
print(f"反向饱和电流: {np.abs(I_reverse_sat):.2e} A")
print(f"硅二极管典型正向压降: 0.6-0.7V")
print(f"实际应用中通常取 0.7V 作为估算值")