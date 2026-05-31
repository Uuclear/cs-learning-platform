#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：水平 Pod 自动伸缩器 (HPA) 模拟

这个脚本模拟 Kubernetes HPA 如何根据 CPU 负载自动调整 Pod 数量。
使用 numpy 生成不同的负载模式来测试自动伸缩行为。
"""

import numpy as np
from typing import List, Tuple


class HPASimulator:
    """HPA 模拟器"""
    def __init__(self, min_replicas: int = 1, max_replicas: int = 10, target_cpu: float = 50.0):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu  # 目标 CPU 使用率百分比
        self.current_replicas = min_replicas
        self.cpu_usage_history: List[float] = []
        self.replica_history: List[int] = []

    def calculate_desired_replicas(self, current_cpu: float) -> int:
        """根据当前 CPU 使用率计算期望的副本数"""
        if current_cpu == 0:
            return self.min_replicas

        # HPA 算法：desired_replicas = ceil(current_replicas * (current_cpu / target_cpu))
        desired = np.ceil(self.current_replicas * (current_cpu / self.target_cpu))
        desired = max(self.min_replicas, min(self.max_replicas, desired))
        return int(desired)

    def simulate_load_pattern(self, load_pattern: str, duration: int = 60) -> Tuple[List[float], List[int]]:
        """模拟不同的负载模式"""
        print(f"📈 模拟负载模式: {load_pattern}")
        print(f"目标 CPU 使用率: {self.target_cpu}%")
        print(f"副本范围: {self.min_replicas}-{self.max_replicas}")
        print("-" * 50)

        self.cpu_usage_history = []
        self.replica_history = []

        for t in range(duration):
            # 生成不同的 CPU 负载模式
            if load_pattern == "steady":
                cpu_usage = 45 + np.random.normal(0, 5)  # 稳定负载
            elif load_pattern == "spike":
                if t % 20 == 0:  # 每 20 秒一个峰值
                    cpu_usage = 80 + np.random.normal(0, 10)
                else:
                    cpu_usage = 30 + np.random.normal(0, 5)
            elif load_pattern == "gradual_increase":
                base_load = 20 + (t / duration) * 60  # 从 20% 逐渐增加到 80%
                cpu_usage = base_load + np.random.normal(0, 3)
            elif load_pattern == "oscillating":
                cpu_usage = 50 + 20 * np.sin(t * 0.3) + np.random.normal(0, 4)  # 正弦波负载
            else:
                cpu_usage = 40 + np.random.normal(0, 8)

            cpu_usage = max(0, min(100, cpu_usage))  # 限制在 0-100%

            # 计算新的副本数（每 10 秒检查一次，模拟 HPA 的同步周期）
            if t % 10 == 0:
                desired_replicas = self.calculate_desired_replicas(cpu_usage)
                self.current_replicas = desired_replicas

            self.cpu_usage_history.append(cpu_usage)
            self.replica_history.append(self.current_replicas)

            # 显示实时状态
            if t % 15 == 0 or t == duration - 1:
                print(f"时间 {t}s: CPU={cpu_usage:.1f}%, 副本数={self.current_replicas}")

        return self.cpu_usage_history, self.replica_history

    def plot_results(self, load_patterns: List[str]):
        """绘制结果图表（需要 matplotlib）"""
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(len(load_patterns), 2, figsize=(12, 4 * len(load_patterns)))
        if len(load_patterns) == 1:
            axes = [axes]

        for i, pattern in enumerate(load_patterns):
            cpu_data, replica_data = self.simulate_load_pattern(pattern)

            # CPU 使用率图表
            axes[i][0].plot(cpu_data, 'b-', linewidth=2, label='CPU 使用率')
            axes[i][0].axhline(y=self.target_cpu, color='r', linestyle='--',
                              label=f'目标 ({self.target_cpu}%)')
            axes[i][0].set_title(f'{pattern} - CPU 使用率')
            axes[i][0].set_ylabel('CPU (%)')
            axes[i][0].set_xlabel('时间 (秒)')
            axes[i][0].legend()
            axes[i][0].grid(True, alpha=0.3)

            # 副本数量图表
            axes[i][1].plot(replica_data, 'g-', linewidth=2, label='Pod 副本数')
            axes[i][1].set_title(f'{pattern} - Pod 副本数')
            axes[i][1].set_ylabel('副本数')
            axes[i][1].set_xlabel('时间 (秒)')
            axes[i][1].set_ylim(self.min_replicas - 0.5, self.max_replicas + 0.5)
            axes[i][1].legend()
            axes[i][1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('hpa_simulation.png', dpi=150, bbox_inches='tight')
        print(f"\n📊 图表已保存为 'hpa_simulation.png'")


def main():
    """主函数：演示 HPA 在不同负载模式下的行为"""
    print("=== Kubernetes HPA 模拟 ===\n")

    # 创建 HPA 模拟器
    hpa = HPASimulator(min_replicas=2, max_replicas=8, target_cpu=60.0)

    # 定义要测试的负载模式
    load_patterns = ["steady", "spike", "gradual_increase"]

    # 优先尝试生成图表；无 matplotlib 时仅输出文本模拟
    try:
        hpa.plot_results(load_patterns)
        print("\n✅ HPA 模拟完成！")
    except ImportError:
        print("⚠️  matplotlib 未安装，跳过图表生成（可运行: pip install matplotlib）\n")
        for pattern in load_patterns:
            print(f"--- {pattern.upper()} ---")
            hpa.simulate_load_pattern(pattern, duration=30)

    print("\n💡 观察要点:")
    print("   - 副本数如何响应 CPU 负载变化")
    print("   - 自动伸缩的延迟性（HPA 默认每 15-30 秒同步一次）")
    print("   - 副本数的上下限约束")


if __name__ == "__main__":
    main()