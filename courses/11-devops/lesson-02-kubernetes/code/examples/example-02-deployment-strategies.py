#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2：部署策略模拟

这个脚本演示滚动更新（Rolling Update）和重新创建（Recreate）
两种部署策略的区别，以及它们对应用可用性的影响。
"""

import time
import random
from typing import List, Dict


class Pod:
    """Pod 类表示一个 Kubernetes Pod"""
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.status = "Running"
        self.ready = True

    def __str__(self):
        return f"Pod({self.name}, v{self.version}, {self.status})"


class DeploymentSimulator:
    """Deployment 模拟器"""
    def __init__(self, app_name: str, initial_version: str, replicas: int = 3):
        self.app_name = app_name
        self.replicas = replicas
        self.pods: List[Pod] = []
        self.current_version = initial_version
        self._create_initial_pods()

    def _create_initial_pods(self):
        """创建初始 Pod"""
        self.pods = [
            Pod(f"{self.app_name}-pod-{i}", self.current_version)
            for i in range(self.replicas)
        ]

    def get_available_pods(self) -> int:
        """获取可用的 Pod 数量"""
        return sum(1 for pod in self.pods if pod.status == "Running" and pod.ready)

    def display_status(self, strategy: str = ""):
        """显示当前状态"""
        available = self.get_available_pods()
        total = len(self.pods)
        versions = [pod.version for pod in self.pods]
        unique_versions = list(set(versions))

        print(f"状态: {available}/{total} 个 Pod 可用")
        print(f"版本分布: {', '.join(unique_versions)}")
        if strategy:
            print(f"部署策略: {strategy}")
        print(f"Pod 列表: {[str(pod) for pod in self.pods]}")
        print()

    def rolling_update(self, new_version: str, max_unavailable: int = 1, max_surge: int = 1):
        """模拟滚动更新策略"""
        print("🔄 开始滚动更新...")
        print(f"从版本 {self.current_version} 更新到 {new_version}")
        print(f"参数: maxUnavailable={max_unavailable}, maxSurge={max_surge}")
        print("-" * 50)

        # 滚动更新过程
        pods_to_update = len(self.pods)
        updated = 0

        while updated < pods_to_update:
            # 计算可以同时更新的 Pod 数量
            current_available = self.get_available_pods()
            can_update = min(
                max_unavailable,
                pods_to_update - updated,
                current_available  # 确保不会让可用 Pod 降到 0
            )

            if can_update <= 0:
                can_update = 1  # 至少更新一个

            # 创建新的 Pod（surge）
            surge_pods = min(max_surge, pods_to_update - updated)
            for i in range(surge_pods):
                if len(self.pods) < pods_to_update + max_surge:
                    new_pod = Pod(f"{self.app_name}-pod-new-{updated+i}", new_version)
                    new_pod.ready = False  # 新 Pod 需要时间准备
                    self.pods.append(new_pod)

            # 更新现有 Pod
            pods_updated_this_round = 0
            for pod in self.pods[:]:
                if pod.version == self.current_version and pods_updated_this_round < can_update:
                    # 删除旧 Pod
                    self.pods.remove(pod)
                    # 创建新 Pod 替代
                    pod_suffix = int(pod.name.split('-')[-1])
                    new_pod = Pod(f"{self.app_name}-pod-{updated + pod_suffix}", new_version)
                    new_pod.ready = False
                    self.pods.append(new_pod)
                    updated += 1
                    pods_updated_this_round += 1

            # 模拟新 Pod 准备就绪
            for pod in self.pods:
                if pod.version == new_version and not pod.ready:
                    if random.random() > 0.3:  # 70% 概率准备就绪
                        pod.ready = True

            self.display_status("滚动更新")
            time.sleep(1)

        self.current_version = new_version
        print("✅ 滚动更新完成！")

    def recreate_deployment(self, new_version: str):
        """模拟重新创建策略"""
        print("🔄 开始重新创建部署...")
        print(f"从版本 {self.current_version} 更新到 {new_version}")
        print("-" * 50)

        # 第一阶段：删除所有旧 Pod
        print("阶段 1: 删除所有旧 Pod...")
        old_pods = self.pods[:]
        self.pods = []
        self.display_status("重新创建 - 删除阶段")
        time.sleep(2)

        # 第二阶段：创建所有新 Pod
        print("阶段 2: 创建所有新 Pod...")
        self.pods = [
            Pod(f"{self.app_name}-pod-{i}", new_version)
            for i in range(self.replicas)
        ]

        # 模拟 Pod 逐步准备就绪
        ready_count = 0
        while ready_count < len(self.pods):
            for pod in self.pods[ready_count:]:
                if random.random() > 0.4:  # 60% 概率准备就绪
                    pod.ready = True
                    ready_count += 1
            self.display_status("重新创建 - 创建阶段")
            time.sleep(1)

        self.current_version = new_version
        print("✅ 重新创建部署完成！")


def main():
    """主函数：演示两种部署策略"""
    print("=== Kubernetes 部署策略模拟 ===\n")

    # 演示滚动更新
    print("📊 场景 1: 滚动更新 (推荐用于生产环境)")
    simulator1 = DeploymentSimulator("web-app", "1.0", replicas=4)
    simulator1.display_status()
    simulator1.rolling_update("2.0")
    print("\n" + "="*60 + "\n")

    # 演示重新创建
    print("📊 场景 2: 重新创建 (适用于非关键应用)")
    simulator2 = DeploymentSimulator("batch-job", "1.0", replicas=3)
    simulator2.display_status()
    simulator2.recreate_deployment("2.0")


if __name__ == "__main__":
    main()