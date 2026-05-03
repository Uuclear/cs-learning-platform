#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：指标收集器实现
实现计数器、仪表盘和直方图三种基本指标类型，并支持导出功能
"""

import time
import threading
from typing import Dict, List, Optional, Union
from collections import defaultdict


class MetricCollector:
    """指标收集器，支持多种指标类型"""

    def __init__(self):
        """初始化指标收集器"""
        self._metrics: Dict[str, 'Metric'] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, description: str = '') -> 'Counter':
        """
        创建或获取计数器指标

        Args:
            name: 指标名称
            description: 指标描述

        Returns:
            Counter: 计数器实例
        """
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Counter(name, description)
            return self._metrics[name]

    def gauge(self, name: str, description: str = '') -> 'Gauge':
        """
        创建或获取仪表盘指标

        Args:
            name: 指标名称
            description: 指标描述

        Returns:
            Gauge: 仪表盘实例
        """
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Gauge(name, description)
            return self._metrics[name]

    def histogram(self, name: str, description: str = '',
                  buckets: Optional[List[float]] = None) -> 'Histogram':
        """
        创建或获取直方图指标

        Args:
            name: 指标名称
            description: 指标描述
            buckets: 直方图桶边界，默认为[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]

        Returns:
            Histogram: 直方图实例
        """
        with self._lock:
            if name not in self._metrics:
                if buckets is None:
                    buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
                self._metrics[name] = Histogram(name, description, buckets)
            return self._metrics[name]

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        """
        收集所有指标数据

        Returns:
            List[Dict]: 指标数据列表
        """
        with self._lock:
            result = []
            for metric in self._metrics.values():
                result.extend(metric.collect())
            return result

    def export_prometheus(self) -> str:
        """
        导出Prometheus格式的指标数据

        Returns:
            str: Prometheus格式的指标字符串
        """
        lines = []
        with self._lock:
            for metric in self._metrics.values():
                lines.extend(metric.export_prometheus())
        return '\n'.join(lines)


class Metric:
    """指标基类"""

    def __init__(self, name: str, description: str = ''):
        """
        初始化指标

        Args:
            name: 指标名称
            description: 指标描述
        """
        self.name = name
        self.description = description

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        """
        收集指标数据

        Returns:
            List[Dict]: 指标数据列表
        """
        raise NotImplementedError

    def export_prometheus(self) -> List[str]:
        """
        导出Prometheus格式

        Returns:
            List[str]: Prometheus格式行列表
        """
        raise NotImplementedError


class Counter(Metric):
    """计数器指标 - 只能递增的累计值"""

    def __init__(self, name: str, description: str = ''):
        """
        初始化计数器

        Args:
            name: 指标名称
            description: 指标描述
        """
        super().__init__(name, description)
        self._value = 0.0
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0) -> None:
        """
        增加计数器值

        Args:
            amount: 增加的数量，默认为1.0
        """
        if amount < 0:
            raise ValueError("计数器只能增加正数")
        with self._lock:
            self._value += amount

    def get(self) -> float:
        """
        获取当前计数器值

        Returns:
            float: 当前值
        """
        with self._lock:
            return self._value

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        """收集计数器数据"""
        return [{
            'name': self.name,
            'type': 'counter',
            'value': self.get(),
            'description': self.description
        }]

    def export_prometheus(self) -> List[str]:
        """导出Prometheus格式"""
        lines = []
        if self.description:
            lines.append(f'# HELP {self.name} {self.description}')
        lines.append(f'# TYPE {self.name} counter')
        lines.append(f'{self.name} {self.get()}')
        return lines


class Gauge(Metric):
    """仪表盘指标 - 可以上下波动的瞬时值"""

    def __init__(self, name: str, description: str = ''):
        """
        初始化仪表盘

        Args:
            name: 指标名称
            description: 指标描述
        """
        super().__init__(name, description)
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        """
        设置仪表盘值

        Args:
            value: 新的值
        """
        with self._lock:
            self._value = value

    def inc(self, amount: float = 1.0) -> None:
        """
        增加仪表盘值

        Args:
            amount: 增加的数量
        """
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0) -> None:
        """
        减少仪表盘值

        Args:
            amount: 减少的数量
        """
        with self._lock:
            self._value -= amount

    def get(self) -> float:
        """
        获取当前仪表盘值

        Returns:
            float: 当前值
        """
        with self._lock:
            return self._value

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        """收集仪表盘数据"""
        return [{
            'name': self.name,
            'type': 'gauge',
            'value': self.get(),
            'description': self.description
        }]

    def export_prometheus(self) -> List[str]:
        """导出Prometheus格式"""
        lines = []
        if self.description:
            lines.append(f'# HELP {self.name} {self.description}')
        lines.append(f'# TYPE {self.name} gauge')
        lines.append(f'{self.name} {self.get()}')
        return lines


class Histogram(Metric):
    """直方图指标 - 记录观测值的分布情况"""

    def __init__(self, name: str, description: str = '', buckets: List[float] = None):
        """
        初始化直方图

        Args:
            name: 指标名称
            description: 指标描述
            buckets: 桶边界列表
        """
        super().__init__(name, description)
        if buckets is None:
            buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]

        # 确保桶是升序的并以+Inf结尾
        self.buckets = sorted(buckets) + [float('inf')]
        self._bucket_counts = [0] * len(self.buckets)
        self._sum = 0.0
        self._count = 0
        self._lock = threading.Lock()

    def observe(self, value: float) -> None:
        """
        记录一个观测值

        Args:
            value: 观测值
        """
        with self._lock:
            self._sum += value
            self._count += 1

            # 找到对应的桶并增加计数
            for i, bucket_upper in enumerate(self.buckets):
                if value <= bucket_upper:
                    self._bucket_counts[i] += 1
                    break

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        """收集直方图数据"""
        with self._lock:
            result = []

            # 添加总和指标
            result.append({
                'name': f'{self.name}_sum',
                'type': 'counter',
                'value': self._sum,
                'description': f'{self.description} sum'
            })

            # 添加计数指标
            result.append({
                'name': f'{self.name}_count',
                'type': 'counter',
                'value': self._count,
                'description': f'{self.description} count'
            })

            # 添加各个桶的指标
            cumulative_count = 0
            for i, bucket_upper in enumerate(self.buckets[:-1]):  # 排除+Inf
                cumulative_count += self._bucket_counts[i]
                bucket_label = f'le="{bucket_upper}"'
                result.append({
                    'name': f'{self.name}_bucket',
                    'type': 'counter',
                    'value': cumulative_count,
                    'description': f'{self.description} bucket le {bucket_upper}',
                    'labels': {'le': str(bucket_upper)}
                })

            # 添加+Inf桶
            result.append({
                'name': f'{self.name}_bucket',
                'type': 'counter',
                'value': self._count,
                'description': f'{self.description} bucket le +Inf',
                'labels': {'le': '+Inf'}
            })

            return result

    def export_prometheus(self) -> List[str]:
        """导出Prometheus格式"""
        lines = []
        if self.description:
            lines.append(f'# HELP {self.name} {self.description}')
        lines.append(f'# TYPE {self.name} histogram')

        with self._lock:
            # 总和
            lines.append(f'{self.name}_sum {self._sum}')
            # 计数
            lines.append(f'{self.name}_count {self._count}')
            # 各个桶
            cumulative_count = 0
            for i, bucket_upper in enumerate(self.buckets[:-1]):
                cumulative_count += self._bucket_counts[i]
                lines.append(f'{self.name}_bucket{{le="{bucket_upper}"}} {cumulative_count}')
            # +Inf桶
            lines.append(f'{self.name}_bucket{{le="+Inf"}} {self._count}')

        return lines


def main():
    """主函数，演示指标收集器的使用"""
    collector = MetricCollector()

    # 创建各种指标
    http_requests_total = collector.counter(
        'http_requests_total',
        'HTTP请求总数'
    )

    active_users = collector.gauge(
        'active_users',
        '当前活跃用户数'
    )

    request_duration_seconds = collector.histogram(
        'request_duration_seconds',
        'HTTP请求持续时间（秒）',
        buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
    )

    # 模拟应用行为
    print("=== 指标收集器演示 ===")

    # 记录一些HTTP请求
    for i in range(5):
        http_requests_total.inc()
        duration = 0.1 + i * 0.2  # 模拟不同的请求时间
        request_duration_seconds.observe(duration)
        time.sleep(0.01)

    # 设置活跃用户数
    active_users.set(1250)

    # 显示收集的数据
    print("\n收集的指标数据:")
    metrics_data = collector.collect()
    for metric in metrics_data[:3]:  # 只显示前几个
        print(f"  {metric['name']}: {metric['value']} ({metric['type']})")

    # 显示Prometheus格式
    print("\nPrometheus格式输出:")
    prometheus_output = collector.export_prometheus()
    print(prometheus_output)

    print("\n=== 指标收集器演示完成 ===")


if __name__ == '__main__':
    main()