#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3：健康检查监控器

实现一个简单的健康检查监控器，模拟 Kubernetes 的 readiness 和 liveness 探针行为。
"""

import time
import random
import threading
from typing import Dict, List, Optional, Callable
from enum import Enum


class ProbeType(Enum):
    """探针类型"""
    LIVENESS = "liveness"
    READINESS = "readiness"


class PodStatus(Enum):
    """Pod 状态"""
    RUNNING = "Running"
    NOT_READY = "NotReady"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"


class HealthCheckResult:
    """健康检查结果"""
    def __init__(self, success: bool, message: str = "", response_time: float = 0.0):
        self.success = success
        self.message = message
        self.response_time = response_time


class PodSimulator:
    """Pod 模拟器"""
    def __init__(self, name: str):
        self.name = name
        self.status = PodStatus.RUNNING
        self.ready = True
        self.health_check_count = 0
        self.liveness_failures = 0
        self.readiness_failures = 0

    def liveness_probe(self) -> HealthCheckResult:
        """模拟 liveness 探针"""
        self.health_check_count += 1

        # 模拟不同的健康状况
        if self.status == PodStatus.FAILED:
            return HealthCheckResult(False, "Pod 已失败", 0.1)

        # 随机故障（模拟真实世界的不稳定性）
        if random.random() < 0.05:  # 5% 故障率
            self.liveness_failures += 1
            return HealthCheckResult(False, "应用无响应", 2.0)

        # 正常响应
        response_time = random.uniform(0.05, 0.3)
        return HealthCheckResult(True, "OK", response_time)

    def readiness_probe(self) -> HealthCheckResult:
        """模拟 readiness 探针"""
        if not self.ready:
            return HealthCheckResult(False, "应用未准备好", 0.1)

        if self.status in [PodStatus.FAILED, PodStatus.SUCCEEDED]:
            return HealthCheckResult(False, f"Pod 状态为 {self.status.value}", 0.1)

        # 随机就绪故障
        if random.random() < 0.03:  # 3% 就绪故障率
            self.readiness_failures += 1
            return HealthCheckResult(False, "依赖服务不可用", 1.5)

        response_time = random.uniform(0.02, 0.2)
        return HealthCheckResult(True, "Ready", response_time)

    def simulate_workload(self):
        """模拟工作负载"""
        # 随机改变状态来测试健康检查
        if random.random() < 0.01:  # 1% 概率进入失败状态
            self.status = PodStatus.FAILED
        elif random.random() < 0.02:  # 2% 概率暂时不可用
            self.ready = False
            threading.Timer(10, lambda: setattr(self, 'ready', True)).start()

    def __str__(self):
        return f"Pod({self.name}, {self.status.value}, ready={self.ready})"


class HealthCheckMonitor:
    """健康检查监控器"""
    def __init__(self):
        self.pods: Dict[str, PodSimulator] = {}
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

    def add_pod(self, pod: PodSimulator):
        """添加 Pod 到监控"""
        self.pods[pod.name] = pod

    def remove_pod(self, pod_name: str):
        """从监控中移除 Pod"""
        if pod_name in self.pods:
            del self.pods[pod_name]

    def check_pod_health(self, pod_name: str) -> Dict[str, HealthCheckResult]:
        """检查单个 Pod 的健康状况"""
        pod = self.pods.get(pod_name)
        if not pod:
            return {}

        return {
            "liveness": pod.liveness_probe(),
            "readiness": pod.readiness_probe()
        }

    def get_pod_status(self, pod_name: str) -> Optional[PodStatus]:
        """获取 Pod 状态"""
        pod = self.pods.get(pod_name)
        return pod.status if pod else None

    def monitor_loop(self, interval: float = 5.0):
        """监控循环"""
        while self.monitoring:
            print(f"\n{'='*60}")
            print(f"🕒 健康检查时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")

            for pod_name, pod in self.pods.items():
                # 模拟工作负载
                pod.simulate_workload()

                # 执行健康检查
                results = self.check_pod_health(pod_name)

                # 处理 liveness 检查结果
                liveness_result = results["liveness"]
                if not liveness_result.success:
                    print(f"💀 {pod_name} - Liveness 检查失败: {liveness_result.message}")
                    # 在真实 Kubernetes 中，这会导致容器重启
                    if pod.liveness_failures >= 3:  # 连续失败 3 次后重置
                        print(f"🔄 {pod_name} - 触发重启 (模拟)")
                        pod.status = PodStatus.RUNNING
                        pod.ready = False
                        pod.liveness_failures = 0
                        # 模拟启动时间
                        threading.Timer(5, lambda p=pod: setattr(p, 'ready', True)).start()
                else:
                    print(f"✅ {pod_name} - Liveness: OK ({liveness_result.response_time:.2f}s)")

                # 处理 readiness 检查结果
                readiness_result = results["readiness"]
                if not readiness_result.success:
                    print(f"⚠️  {pod_name} - Readiness 检查失败: {readiness_result.message}")
                    # 在真实 Kubernetes 中，这会将 Pod 从 Service 负载均衡中移除
                else:
                    print(f"✅ {pod_name} - Readiness: Ready ({readiness_result.response_time:.2f}s)")

                print(f"📊 {pod}")

            time.sleep(interval)

    def start_monitoring(self, interval: float = 5.0):
        """开始监控"""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print(f"🚀 开始监控 {len(self.pods)} 个 Pods...")

    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        print("⏹️  监控已停止")


def main():
    """主函数：演示健康检查监控器"""
    print("=== Kubernetes 健康检查监控器 ===\n")

    # 创建监控器
    monitor = HealthCheckMonitor()

    # 添加 Pods
    pods = [
        PodSimulator("web-app-1"),
        PodSimulator("web-app-2"),
        PodSimulator("database"),
        PodSimulator("cache")
    ]

    for pod in pods:
        monitor.add_pod(pod)

    # 开始监控
    try:
        monitor.start_monitoring(interval=3.0)
        print("\n💡 监控说明:")
        print("   - Liveness 探针失败会导致 Pod 重启")
        print("   - Readiness 探针失败会使 Pod 从服务中移除")
        print("   - 按 Ctrl+C 停止监控\n")

        # 运行 60 秒
        time.sleep(60)

    except KeyboardInterrupt:
        print("\n🛑 收到中断信号...")
    finally:
        monitor.stop_monitoring()

    # 显示最终统计
    print("\n📈 最终统计:")
    print("-" * 40)
    for pod in pods:
        total_checks = pod.health_check_count
        liveness_fails = pod.liveness_failures
        readiness_fails = pod.readiness_failures
        print(f"{pod.name}:")
        print(f"  总检查次数: {total_checks}")
        print(f"  Liveness 失败: {liveness_fails}")
        print(f"  Readiness 失败: {readiness_fails}")


if __name__ == "__main__":
    main()