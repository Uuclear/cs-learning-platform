import numpy as np
import matplotlib.pyplot as plt

# 定义不同时间常数的RC电路
R_values = [1, 2, 5]  # 不同的电阻值 (欧姆)
C = 1  # 电容值固定为1法拉

plt.figure(figsize=(10, 6))
t = np.linspace(0, 10, 1000)

for R in R_values:
    tau = R * C
    v_t = 1 - np.exp(-t / tau)
    plt.plot(t, v_t, label=f'R={R}Ω, C={C}F, τ={tau}s')

plt.xlabel('时间 (s)')
plt.ylabel('电压 (V)')
plt.title('RC电路充电响应 - 不同时间常数对比')
plt.legend()
plt.grid(True)
plt.show()