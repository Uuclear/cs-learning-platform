#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：水平 Pod 自动伸缩器 (HPA) 模拟

这个脚本模拟 Kubernetes HPA 如何根据 CPU 负载自动调整 Pod 数量。
使用 numpy 生成不同的负载模式来测试自动伸缩行为（纯文本输出，无需 matplotlib）。
"""

import numpy as np
from typing import List, Tuple


class HPASimulator:
    """HPA 模拟器"""

    def __init__(self, min_replicas: int = 1, max_replicas: int = 10, target_cpu: float = 50.0):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu
        self.current_replicas = min_replicas
        self.cpu_usage_history: List[float] = []
        self.replica_history: List[int] = []

    def calculate_desired_replicas(self, current_cpu: float) -> int:
        """根据当前 CPU 使用率计算期望的副本数"""
        if current_cpu == 0:
            return self.min_replicas

        desired = np.ceil(self.current_replicas * (current_cpu / self.target_cpu))
        desired = max(self.min_replicas, min(self.max_replicas, desired))
        return int(desired)

    def simulate_load_pattern(self, load_pattern: str, duration: int = 30) -> Tuple[List[float], List[int]]:
        """模拟不同的负载模式"""
        print(f"📈 模拟负载模式: {load_pattern}")
        print(f"目标 CPU 使用率: {self.target_cpu}%")
        print(f"副本范围: {self.min_replicas}-{self.max_replicas}")
        print("-" * 50)

        self.cpu_usage_history = []
        self.replica_history = []
        self.current_replicas = self.min_replicas

        for t in range(duration):
            if load_pattern == "steady":
                cpu_usage = 45 + np.random.normal(0, 5)
            elif load_pattern == "spike":
                cpu_usage = 80 + np.random.normal(0, 10) if t % 10 == 0 else 30 + np.random.normal(0, 5)
            elif load_pattern == "gradual_increase":
                base_load = 20 + (t / duration) * 60
                cpu_usage = base_load + np.random.normal(0, 3)
            elif load_pattern == "oscillating":
                cpu_usage = 50 + 20 * np.sin(t * 0.3) + np.random.normal(0, 4)
            else:
                cpu_usage = 40 + np.random.normal(0, 8)

            cpu_usage = max(0, min(100, cpu_usage))

            if t % 5 == 0:
                self.current_replicas = self.calculate_desired_replicas(cpu_usage)

            self.cpu_usage_history.append(cpu_usage)
            self.replica_history.append(self.current_replicas)

            if t % 10 == 0 or t == duration - 1:
                print(f"时间 {t}s: CPU={cpu_usage:.1f}%, 副本数={self.current_replicas}")

        avg_cpu = float(np.mean(self.cpu_usage_history))
        print(f"平均 CPU: {avg_cpu:.1f}%, 峰值副本: {max(self.replica_history)}")
        return self.cpu_usage_history, self.replica_history


def main():
    """主函数：演示 HPA 在不同负载模式下的行为"""
    print("=== Kubernetes HPA 模拟 ===\n")

    hpa = HPASimulator(min_replicas=2, max_replicas=8, target_cpu=60.0)
    load_patterns = ["steady", "spike", "gradual_increase"]

    for pattern in load_patterns:
        print(f"\n--- {pattern.upper()} ---")
        hpa.simulate_load_pattern(pattern, duration=30)

    print("\n✅ HPA 模拟完成！")
    print("💡 观察要点:")
    print("   - 副本数如何响应 CPU 负载变化")
    print("   - HPA 同步周期带来的伸缩延迟")
    print("   - min/max 副本数对伸缩范围的约束")


if __name__ == "__main__":
    main()
