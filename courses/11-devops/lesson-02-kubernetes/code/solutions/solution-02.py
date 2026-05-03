#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2：Kubernetes Pod 调度模拟器

实现一个简单的 Pod 调度模拟器，根据资源约束将 Pods 分配到节点。
模拟 Kubernetes 调度器的过滤和评分阶段。
"""

import random
from typing import List, Dict, Tuple, Optional


class Node:
    """节点类表示 Kubernetes 节点"""
    def __init__(self, name: str, cpu_capacity: int, memory_capacity: int):
        self.name = name
        self.cpu_capacity = cpu_capacity  # CPU 容量（毫核）
        self.memory_capacity = memory_capacity  # 内存容量（MiB）
        self.allocated_cpu = 0
        self.allocated_memory = 0
        self.pods = []

    def available_cpu(self) -> int:
        """可用 CPU 资源"""
        return self.cpu_capacity - self.allocated_cpu

    def available_memory(self) -> int:
        """可用内存资源"""
        return self.memory_capacity - self.allocated_memory

    def can_fit_pod(self, pod_cpu: int, pod_memory: int) -> bool:
        """检查是否能容纳指定资源需求的 Pod"""
        return (self.available_cpu() >= pod_cpu and
                self.available_memory() >= pod_memory)

    def allocate_pod(self, pod_name: str, pod_cpu: int, pod_memory: int):
        """分配 Pod 到此节点"""
        if not self.can_fit_pod(pod_cpu, pod_memory):
            raise ValueError(f"节点 {self.name} 无法容纳 Pod {pod_name}")

        self.allocated_cpu += pod_cpu
        self.allocated_memory += pod_memory
        self.pods.append({
            "name": pod_name,
            "cpu": pod_cpu,
            "memory": pod_memory
        })

    def get_utilization_score(self) -> float:
        """计算资源利用率评分（越高越好）"""
        cpu_util = self.allocated_cpu / self.cpu_capacity
        memory_util = self.allocated_memory / self.memory_capacity
        return (cpu_util + memory_util) / 2

    def __str__(self):
        return (f"Node({self.name}): "
                f"CPU={self.allocated_cpu}/{self.cpu_capacity}m, "
                f"Memory={self.allocated_memory}/{self.memory_capacity}Mi")


class Pod:
    """Pod 类表示要调度的 Pod"""
    def __init__(self, name: str, cpu_request: int, memory_request: int,
                 node_selector: Optional[Dict[str, str]] = None):
        self.name = name
        self.cpu_request = cpu_request
        self.memory_request = memory_request
        self.node_selector = node_selector or {}

    def matches_node_labels(self, node_labels: Dict[str, str]) -> bool:
        """检查 Pod 的节点选择器是否匹配节点标签"""
        if not self.node_selector:
            return True
        return all(node_labels.get(k) == v for k, v in self.node_selector.items())

    def __str__(self):
        return f"Pod({self.name}, CPU={self.cpu_request}m, Memory={self.memory_request}Mi)"


class SchedulerSimulator:
    """调度器模拟器"""
    def __init__(self):
        self.nodes: List[Node] = []
        self.node_labels: Dict[str, Dict[str, str]] = {}  # 节点标签

    def add_node(self, name: str, cpu_capacity: int, memory_capacity: int,
                 labels: Optional[Dict[str, str]] = None):
        """添加节点"""
        node = Node(name, cpu_capacity, memory_capacity)
        self.nodes.append(node)
        self.node_labels[name] = labels or {}

    def schedule_pod(self, pod: Pod) -> Optional[str]:
        """调度单个 Pod"""
        print(f"🎯 调度 Pod: {pod}")

        # 第一阶段：过滤（Filtering）
        feasible_nodes = []
        for node in self.nodes:
            node_labels = self.node_labels[node.name]
            if (node.can_fit_pod(pod.cpu_request, pod.memory_request) and
                pod.matches_node_labels(node_labels)):
                feasible_nodes.append(node)

        if not feasible_nodes:
            print(f"❌ 无法找到合适的节点来调度 Pod {pod.name}")
            return None

        # 第二阶段：评分（Scoring）
        # 使用资源利用率作为评分标准（更高的利用率更好）
        best_node = max(feasible_nodes, key=lambda n: n.get_utilization_score())

        # 分配 Pod 到最佳节点
        best_node.allocate_pod(pod.name, pod.cpu_request, pod.memory_request)
        print(f"✅ Pod {pod.name} 已调度到节点 {best_node.name}")
        return best_node.name

    def schedule_pods(self, pods: List[Pod]) -> Dict[str, Optional[str]]:
        """批量调度 Pods"""
        results = {}
        for pod in pods:
            results[pod.name] = self.schedule_pod(pod)
        return results

    def display_cluster_state(self):
        """显示集群状态"""
        print("\n📊 集群状态:")
        print("-" * 60)
        for node in self.nodes:
            labels_str = ", ".join(f"{k}={v}" for k, v in self.node_labels[node.name].items())
            label_info = f" [{labels_str}]" if labels_str else ""
            print(f"{node}{label_info}")
            if node.pods:
                for pod in node.pods:
                    print(f"  └─ {pod['name']} (CPU={pod['cpu']}m, Memory={pod['memory']}Mi)")
            else:
                print("  └─ (空闲)")
        print("-" * 60)


def main():
    """主函数：演示调度模拟器"""
    print("=== Kubernetes Pod 调度模拟器 ===\n")

    # 创建调度器
    scheduler = SchedulerSimulator()

    # 添加节点
    scheduler.add_node("node-1", cpu_capacity=2000, memory_capacity=4096,
                      labels={"zone": "us-east-1a", "gpu": "false"})
    scheduler.add_node("node-2", cpu_capacity=4000, memory_capacity=8192,
                      labels={"zone": "us-east-1b", "gpu": "true"})
    scheduler.add_node("node-3", cpu_capacity=1000, memory_capacity=2048,
                      labels={"zone": "us-east-1a", "gpu": "false"})

    # 创建 Pods
    pods = [
        Pod("web-app-1", cpu_request=500, memory_request=512),
        Pod("web-app-2", cpu_request=300, memory_request=256),
        Pod("database", cpu_request=1000, memory_request=2048,
            node_selector={"zone": "us-east-1b"}),  # 必须在 zone b
        Pod("ml-job", cpu_request=2000, memory_request=4096,
            node_selector={"gpu": "true"}),  # 需要 GPU 节点
        Pod("cache", cpu_request=200, memory_request=128),
        Pod("monitoring", cpu_request=100, memory_request=64)
    ]

    # 调度 Pods
    print("开始调度 Pods...\n")
    results = scheduler.schedule_pods(pods)

    # 显示结果
    scheduler.display_cluster_state()

    # 统计信息
    scheduled_count = sum(1 for result in results.values() if result is not None)
    print(f"\n📈 调度统计: {scheduled_count}/{len(pods)} 个 Pods 成功调度")

    # 测试资源不足的情况
    print("\n--- 测试资源不足情况 ---")
    large_pod = Pod("large-app", cpu_request=5000, memory_request=10240)
    scheduler.schedule_pod(large_pod)


if __name__ == "__main__":
    main()