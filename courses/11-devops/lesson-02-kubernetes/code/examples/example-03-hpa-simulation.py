#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：水平 Pod 自动伸缩器 (HPA) 模拟

模拟 Kubernetes HPA 如何根据 CPU 负载自动调整 Pod 数量。
不依赖 matplotlib，适合标准 Python 环境直接运行。
"""

import random
import math
from typing import List, Tuple


class HPASimulator:
    """HPA 模拟器"""

    def __init__(
        self,
        min_replicas: int = 1,
        max_replicas: int = 10,
        target_cpu: float = 50.0,
    ):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu
        self.current_replicas = min_replicas

    def calculate_desired_replicas(self, current_cpu: float) -> int:
        if current_cpu <= 0:
            return self.min_replicas
        desired = math.ceil(
            self.current_replicas * (current_cpu / self.target_cpu)
        )
        return max(self.min_replicas, min(self.max_replicas, desired))

    def simulate_load_pattern(
        self, load_pattern: str, duration: int = 30
    ) -> Tuple[List[float], List[int]]:
        print(f"📈 负载模式: {load_pattern}（{duration} 步）")
        cpu_history: List[float] = []
        replica_history: List[int] = []

        for t in range(duration):
            if load_pattern == "steady":
                cpu_usage = 45 + random.gauss(0, 5)
            elif load_pattern == "spike":
                cpu_usage = (
                    80 + random.gauss(0, 10)
                    if t % 10 == 0
                    else 30 + random.gauss(0, 5)
                )
            elif load_pattern == "gradual_increase":
                base = 20 + (t / max(duration, 1)) * 60
                cpu_usage = base + random.gauss(0, 3)
            else:
                cpu_usage = 40 + random.gauss(0, 8)

            cpu_usage = max(0.0, min(100.0, cpu_usage))

            if t % 5 == 0:
                self.current_replicas = self.calculate_desired_replicas(cpu_usage)

            cpu_history.append(cpu_usage)
            replica_history.append(self.current_replicas)

            if t % 10 == 0 or t == duration - 1:
                print(
                    f"  t={t:2d}s  CPU={cpu_usage:5.1f}%  "
                    f"副本数={self.current_replicas}"
                )

        return cpu_history, replica_history


def main():
    print("=== Kubernetes HPA 模拟 ===\n")
    hpa = HPASimulator(min_replicas=2, max_replicas=8, target_cpu=60.0)
    patterns = ["steady", "spike", "gradual_increase"]

    for pattern in patterns:
        print(f"\n--- {pattern.upper()} ---")
        hpa.current_replicas = hpa.min_replicas
        cpu_data, replica_data = hpa.simulate_load_pattern(pattern, duration=20)
        avg_cpu = sum(cpu_data) / len(cpu_data)
        print(
            f"  摘要: 平均 CPU={avg_cpu:.1f}%, "
            f"副本范围 {min(replica_data)}-{max(replica_data)}"
        )

    print("\n✅ HPA 模拟完成！")
    print("💡 观察: 副本数随 CPU 升高而增加，受 min/max 约束")


if __name__ == "__main__":
    main()
