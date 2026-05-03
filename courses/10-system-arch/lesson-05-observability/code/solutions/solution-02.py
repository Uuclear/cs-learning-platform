#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可观测性课程解决方案 2: 指标收集和告警

此解决方案展示了更完整的指标收集实现，
包括 Prometheus 兼容的指标格式和灵活的告警规则。
"""

import time
import threading
from typing import Dict, List, Callable, Optional
from collections import defaultdict
import math


class Metric:
    """基础指标类"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def collect(self) -> str:
        """收集指标数据（子类实现）"""
        raise NotImplementedError


class Counter(Metric):
    """计数器指标"""

    def __init__(self, name: str, description: str = ""):
        super().__init__(name, description)
        self._value = 0
        self._lock = threading.Lock()

    def inc(self, value: float = 1.0) -> None:
        """增加计数器值"""
        with self._lock:
            self._value += value

    def set(self, value: float) -> None:
        """设置计数器值"""
        with self._lock:
            self._value = value

    def get(self) -> float:
        """获取计数器值"""
        with self._lock:
            return self._value

    def collect(self) -> str:
        """收集计数器指标"""
        lines = []
        if self.description:
            lines.append(f"# HELP {self.name} {self.description}")
            lines.append(f"# TYPE {self.name} counter")
        lines.append(f"{self.name} {self.get()}")
        return "\n".join(lines)


class Gauge(Metric):
    """仪表盘指标"""

    def __init__(self, name: str, description: str = ""):
        super().__init__(name, description)
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        """设置仪表盘值"""
        with self._lock:
            self._value = value

    def inc(self, value: float = 1.0) -> None:
        """增加仪表盘值"""
        with self._lock:
            self._value += value

    def dec(self, value: float = 1.0) -> None:
        """减少仪表盘值"""
        with self._lock:
            self._value -= value

    def get(self) -> float:
        """获取仪表盘值"""
        with self._lock:
            return self._value

    def collect(self) -> str:
        """收集仪表盘指标"""
        lines = []
        if self.description:
            lines.append(f"# HELP {self.name} {self.description}")
            lines.append(f"# TYPE {self.name} gauge")
        lines.append(f"{self.name} {self.get()}")
        return "\n".join(lines)


class Histogram(Metric):
    """直方图指标"""

    def __init__(self, name: str, buckets: List[float] = None, description: str = ""):
        super().__init__(name, description)
        if buckets is None:
            # 默认桶：5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s
            buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        self.buckets = sorted(buckets)
        self.buckets.append(float('inf'))  # 添加无穷大桶
        self._bucket_counts = defaultdict(int)
        self._count = 0
        self._sum = 0.0
        self._lock = threading.Lock()

    def observe(self, value: float) -> None:
        """记录观测值"""
        with self._lock:
            self._count += 1
            self._sum += value

            # 找到合适的桶
            for bucket in self.buckets:
                if value <= bucket:
                    self._bucket_counts[bucket] += 1
                    break

    def collect(self) -> str:
        """收集直方图指标"""
        lines = []
        if self.description:
            lines.append(f"# HELP {self.name} {self.description}")
            lines.append(f"# TYPE {self.name} histogram")

        with self._lock:
            # 记录累计桶计数
            cumulative_count = 0
            for bucket in self.buckets:
                if bucket == float('inf'):
                    bucket_label = 'inf'
                else:
                    bucket_label = str(bucket)
                cumulative_count += self._bucket_counts[bucket]
                lines.append(f'{self.name}_bucket{{le="{bucket_label}"}} {cumulative_count}')

            lines.append(f"{self.name}_count {self._count}")
            lines.append(f"{self.name}_sum {self._sum}")

        return "\n".join(lines)


class AlertRule:
    """告警规则"""

    def __init__(self, name: str, condition: Callable[[], bool], description: str = ""):
        self.name = name
        self.condition = condition
        self.description = description
        self.active = False

    def evaluate(self) -> bool:
        """评估告警条件"""
        try:
            result = self.condition()
            if result and not self.active:
                self.active = True
                print(f"🚨 告警触发: {self.name}")
                if self.description:
                    print(f"   描述: {self.description}")
            elif not result and self.active:
                self.active = False
                print(f"✅ 告警恢复: {self.name}")
            return result
        except Exception as e:
            print(f"⚠️  告警规则评估错误 {self.name}: {e}")
            return False


class MetricsRegistry:
    """指标注册表"""

    def __init__(self):
        self.metrics: Dict[str, Metric] = {}
        self.alert_rules: List[AlertRule] = []

    def register(self, metric: Metric) -> Metric:
        """注册指标"""
        self.metrics[metric.name] = metric
        return metric

    def add_alert_rule(self, rule: AlertRule) -> None:
        """添加告警规则"""
        self.alert_rules.append(rule)

    def collect_all(self) -> str:
        """收集所有指标"""
        return "\n".join(metric.collect() for metric in self.metrics.values())

    def evaluate_alerts(self) -> None:
        """评估所有告警规则"""
        for rule in self.alert_rules:
            rule.evaluate()


def create_sample_metrics():
    """创建示例指标"""
    registry = MetricsRegistry()

    # 创建各种指标
    http_requests = registry.register(
        Counter("http_requests_total", "HTTP 请求总数")
    )

    request_duration = registry.register(
        Histogram("http_request_duration_seconds", description="HTTP 请求持续时间")
    )

    memory_usage = registry.register(
        Gauge("process_memory_usage_bytes", "进程内存使用量（字节）")
    )

    active_connections = registry.register(
        Gauge("active_connections", "活跃连接数")
    )

    # 添加一些数据
    for _ in range(100):
        http_requests.inc()
        request_duration.observe(random.uniform(0.01, 0.5))

    memory_usage.set(1024 * 1024 * 256)  # 256MB
    active_connections.set(42)

    # 添加告警规则
    def high_error_rate():
        total = http_requests.get()
        # 这里简化，实际应该有单独的错误计数器
        error_rate = 0.1 if total > 50 else 0.0
        return error_rate > 0.05

    registry.add_alert_rule(
        AlertRule(
            "high_http_error_rate",
            high_error_rate,
            "HTTP 错误率超过 5%"
        )
    )

    def high_memory_usage():
        return memory_usage.get() > (1024 * 1024 * 200)  # 超过 200MB

    registry.add_alert_rule(
        AlertRule(
            "high_memory_usage",
            high_memory_usage,
            "内存使用量超过 200MB"
        )
    )

    return registry


def main():
    """主函数"""
    print("=== 指标解决方案演示 ===\n")

    registry = create_sample_metrics()

    # 显示收集的指标
    print("收集的指标:")
    print(registry.collect_all())
    print()

    # 评估告警
    print("告警评估:")
    registry.evaluate_alerts()


if __name__ == "__main__":
    import random
    main()