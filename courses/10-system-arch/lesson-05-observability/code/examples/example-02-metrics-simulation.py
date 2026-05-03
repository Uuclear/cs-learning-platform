#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可观测性课程示例 2: 指标模拟

本示例演示如何模拟 Prometheus 风格的指标收集，
包括计数器、直方图和基于阈值的告警。
"""

import time
import random
from typing import Dict, List, Tuple
from collections import defaultdict


class MetricsCollector:
    """指标收集器类"""

    def __init__(self):
        """初始化指标收集器"""
        self.counters = defaultdict(int)
        self.histograms = defaultdict(list)
        self.gauges = {}

    def increment_counter(self, name: str, labels: Dict[str, str] = None, value: int = 1) -> None:
        """
        增加计数器

        Args:
            name: 指标名称
            labels: 标签字典
            value: 增加的值
        """
        key = self._get_metric_key(name, labels)
        self.counters[key] += value

    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """
        记录直方图观测值

        Args:
            name: 指标名称
            value: 观测值
            labels: 标签字典
        """
        key = self._get_metric_key(name, labels)
        self.histograms[key].append(value)

    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """
        设置仪表盘值

        Args:
            name: 指标名称
            value: 值
            labels: 标签字典
        """
        key = self._get_metric_key(name, labels)
        self.gauges[key] = value

    def _get_metric_key(self, name: str, labels: Dict[str, str] = None) -> str:
        """
        生成指标键

        Args:
            name: 指标名称
            labels: 标签字典

        Returns:
            指标键字符串
        """
        if not labels:
            return name
        label_str = ",".join([f"{k}=\"{v}\"" for k, v in sorted(labels.items())])
        return f"{name}{{{label_str}}}"

    def get_counter_value(self, name: str, labels: Dict[str, str] = None) -> int:
        """获取计数器值"""
        key = self._get_metric_key(name, labels)
        return self.counters.get(key, 0)

    def get_histogram_stats(self, name: str, labels: Dict[str, str] = None) -> Dict[str, float]:
        """获取直方图统计信息"""
        key = self._get_metric_key(name, labels)
        values = self.histograms.get(key, [])
        if not values:
            return {"count": 0, "sum": 0.0, "avg": 0.0, "p95": 0.0, "p99": 0.0}

        values_sorted = sorted(values)
        count = len(values)
        total = sum(values)
        avg = total / count
        p95_idx = min(int(0.95 * count), count - 1)
        p99_idx = min(int(0.99 * count), count - 1)

        return {
            "count": count,
            "sum": total,
            "avg": avg,
            "p95": values_sorted[p95_idx],
            "p99": values_sorted[p99_idx]
        }

    def get_gauge_value(self, name: str, labels: Dict[str, str] = None) -> float:
        """获取仪表盘值"""
        key = self._get_metric_key(name, labels)
        return self.gauges.get(key, 0.0)


class AlertManager:
    """告警管理器"""

    def __init__(self, metrics_collector: MetricsCollector):
        """
        初始化告警管理器

        Args:
            metrics_collector: 指标收集器实例
        """
        self.metrics = metrics_collector
        self.active_alerts = []

    def check_http_error_rate(self, threshold: float = 0.05) -> bool:
        """
        检查 HTTP 错误率是否超过阈值

        Args:
            threshold: 错误率阈值 (默认 5%)

        Returns:
            是否触发告警
        """
        total_requests = self.metrics.get_counter_value("http_requests_total")
        error_requests = (
            self.metrics.get_counter_value("http_requests_total", {"status": "5xx"}) +
            self.metrics.get_counter_value("http_requests_total", {"status": "4xx"})
        )

        if total_requests == 0:
            return False

        error_rate = error_requests / total_requests
        if error_rate > threshold:
            alert_msg = f"HTTP 错误率过高: {error_rate:.2%} > {threshold:.2%}"
            self.active_alerts.append(alert_msg)
            print(f"🚨 告警触发: {alert_msg}")
            return True
        return False

    def check_latency_p99(self, threshold_ms: float = 1000.0) -> bool:
        """
        检查 P99 延迟是否超过阈值

        Args:
            threshold_ms: 延迟阈值（毫秒）

        Returns:
            是否触发告警
        """
        latency_stats = self.metrics.get_histogram_stats("http_request_duration_seconds")
        p99_ms = latency_stats["p99"] * 1000  # 转换为毫秒

        if p99_ms > threshold_ms:
            alert_msg = f"P99 延迟过高: {p99_ms:.2f}ms > {threshold_ms}ms"
            self.active_alerts.append(alert_msg)
            print(f"🚨 告警触发: {alert_msg}")
            return True
        return False

    def check_memory_usage(self, threshold_percent: float = 80.0) -> bool:
        """
        检查内存使用率是否超过阈值

        Args:
            threshold_percent: 内存使用率阈值（百分比）

        Returns:
            是否触发告警
        """
        memory_usage = self.metrics.get_gauge_value("process_memory_usage_percent")
        if memory_usage > threshold_percent:
            alert_msg = f"内存使用率过高: {memory_usage:.1f}% > {threshold_percent}%"
            self.active_alerts.append(alert_msg)
            print(f"🚨 告警触发: {alert_msg}")
            return True
        return False


def simulate_metrics_and_alerts():
    """模拟指标收集和告警"""
    collector = MetricsCollector()
    alert_manager = AlertManager(collector)

    print("=== 开始模拟指标收集 ===")

    # 模拟 HTTP 请求
    endpoints = ["/api/users", "/api/products", "/api/orders", "/health"]
    statuses = ["2xx", "2xx", "2xx", "2xx", "2xx", "4xx", "5xx"]  # 大部分成功，少量错误

    for i in range(100):
        endpoint = random.choice(endpoints)
        status = random.choice(statuses)

        # 记录请求计数
        collector.increment_counter(
            "http_requests_total",
            {"endpoint": endpoint, "method": "GET", "status": status}
        )

        # 记录请求延迟（大部分正常，偶尔慢）
        if random.random() < 0.95:
            latency = random.uniform(0.05, 0.3)  # 50-300ms
        else:
            latency = random.uniform(0.5, 2.0)   # 500ms-2s

        collector.observe_histogram(
            "http_request_duration_seconds",
            latency,
            {"endpoint": endpoint}
        )

        time.sleep(0.01)  # 模拟时间流逝

    # 设置内存使用率（模拟高内存使用）
    memory_usage = 85.5  # 85.5% 使用率
    collector.set_gauge("process_memory_usage_percent", memory_usage)

    print(f"\n=== 指标收集完成 ===")
    print(f"总请求数: {collector.get_counter_value('http_requests_total')}")
    print(f"内存使用率: {collector.get_gauge_value('process_memory_usage_percent'):.1f}%")

    latency_stats = collector.get_histogram_stats("http_request_duration_seconds")
    print(f"P99 延迟: {latency_stats['p99'] * 1000:.2f}ms")

    print(f"\n=== 开始告警检查 ===")
    # 检查各种告警条件
    alert_manager.check_http_error_rate(threshold=0.03)  # 3% 阈值
    alert_manager.check_latency_p99(threshold_ms=500.0)  # 500ms 阈值
    alert_manager.check_memory_usage(threshold_percent=80.0)  # 80% 阈值

    print(f"\n=== 活跃告警数量: {len(alert_manager.active_alerts)} ===")


def main():
    """主函数"""
    print("=== 可观测性课程：指标模拟示例 ===\n")
    simulate_metrics_and_alerts()
    print("\n=== 指标示例结束 ===")


if __name__ == "__main__":
    main()