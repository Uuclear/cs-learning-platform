#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：水平 Pod 自动伸缩器 (HPA) 模拟

模拟 Kubernetes HPA 如何根据 CPU 负载自动调整 Pod 数量。
仅使用标准库与 numpy，无需 matplotlib。
"""

import math
import random
from typing import List, Tuple


class HPASimulator:
    """HPA 模拟器"""

    def __init__(self, min_replicas: int = 1, max_replicas: int = 10, target_cpu: float = 50.0):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu
        self.current_replicas = min_replicas

    def calculate_desired_replicas(self, current_cpu: float) -> int:
        """根据当前 CPU 使用率计算期望副本数"""
        if current_cpu <= 0:
            return self.min_replicas
        desired = math.ceil(self.current_replicas * (current_cpu / self.target_cpu))
        return max(self.min_replicas, min(self.max_replicas, int(desired)))

    def simulate_load_pattern(self, load_pattern: str, duration: int = 30) -> Tuple[List[float], List[int]]:
        """模拟负载并返回 CPU 与副本历史"""
        print(f"📈 负载模式: {load_pattern} | 目标 CPU: {self.target_cpu}% | 副本: {self.min_replicas}-{self.max_replicas}")
        print("-" * 50)

        cpu_history: List[float] = []
        replica_history: List[int] = []

        for t in range(duration):
            if load_pattern == "steady":
                cpu_usage = 45 + random.gauss(0, 5)
            elif load_pattern == "spike":
                cpu_usage = (80 if t % 10 == 0 else 30) + random.gauss(0, 5)
            elif load_pattern == "gradual_increase":
                cpu_usage = 20 + (t / duration) * 60 + random.gauss(0, 3)
            else:
                cpu_usage = 40 + random.gauss(0, 8)

            cpu_usage = max(0, min(100, cpu_usage))

            if t % 5 == 0:
                self.current_replicas = self.calculate_desired_replicas(cpu_usage)

            cpu_history.append(cpu_usage)
            replica_history.append(self.current_replicas)

            if t % 10 == 0 or t == duration - 1:
                print(f"  t={t:2d}s  CPU={cpu_usage:5.1f}%  副本={self.current_replicas}")

        return cpu_history, replica_history

    def summarize(self, pattern: str, cpu_data: List[float], replica_data: List[int]) -> None:
        """文本摘要（替代图表）"""
        avg_cpu = sum(cpu_data) / len(cpu_data)
        print(f"\n📊 {pattern} 摘要: 平均 CPU={avg_cpu:.1f}%, 副本范围={min(replica_data)}-{max(replica_data)}")


def main():
    """主函数：演示 HPA 在不同负载模式下的行为"""
    print("=== Kubernetes HPA 模拟 ===\n")

    hpa = HPASimulator(min_replicas=2, max_replicas=8, target_cpu=60.0)
    patterns = ["steady", "spike", "gradual_increase"]

    for pattern in patterns:
        cpu_data, replica_data = hpa.simulate_load_pattern(pattern, duration=25)
        hpa.summarize(pattern, cpu_data, replica_data)
        print()

    print("✅ HPA 模拟完成！")
    print("💡 观察要点:")
    print("   - 副本数随 CPU 与目标值的比值伸缩")
    print("   - HPA 有同步周期，不会每个时刻都调整")
    print("   - min/max 副本数会钳制伸缩结果")


if __name__ == "__main__":
    main()
