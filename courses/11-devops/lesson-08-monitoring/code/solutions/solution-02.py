#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：指标收集器
完整的指标收集器实现，支持计数器、仪表盘和直方图
"""

import threading
from typing import Dict, List, Optional, Union
from collections import defaultdict


class MetricCollector:
    def __init__(self):
        self._metrics: Dict[str, 'Metric'] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, description: str = '') -> 'Counter':
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Counter(name, description)
            return self._metrics[name]

    def gauge(self, name: str, description: str = '') -> 'Gauge':
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Gauge(name, description)
            return self._metrics[name]

    def histogram(self, name: str, description: str = '',
                  buckets: Optional[List[float]] = None) -> 'Histogram':
        with self._lock:
            if name not in self._metrics:
                if buckets is None:
                    buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
                self._metrics[name] = Histogram(name, description, buckets)
            return self._metrics[name]

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        with self._lock:
            result = []
            for metric in self._metrics.values():
                result.extend(metric.collect())
            return result

    def export_prometheus(self) -> str:
        lines = []
        with self._lock:
            for metric in self._metrics.values():
                lines.extend(metric.export_prometheus())
        return '\n'.join(lines)


class Metric:
    def __init__(self, name: str, description: str = ''):
        self.name = name
        self.description = description

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        raise NotImplementedError

    def export_prometheus(self) -> List[str]:
        raise NotImplementedError


class Counter(Metric):
    def __init__(self, name: str, description: str = ''):
        super().__init__(name, description)
        self._value = 0.0
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0) -> None:
        if amount < 0:
            raise ValueError("计数器只能增加正数")
        with self._lock:
            self._value += amount

    def get(self) -> float:
        with self._lock:
            return self._value

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        return [{
            'name': self.name,
            'type': 'counter',
            'value': self.get(),
            'description': self.description
        }]

    def export_prometheus(self) -> List[str]:
        lines = []
        if self.description:
            lines.append(f'# HELP {self.name} {self.description}')
        lines.append(f'# TYPE {self.name} counter')
        lines.append(f'{self.name} {self.get()}')
        return lines


class Gauge(Metric):
    def __init__(self, name: str, description: str = ''):
        super().__init__(name, description)
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        with self._lock:
            self._value = value

    def inc(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value -= amount

    def get(self) -> float:
        with self._lock:
            return self._value

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        return [{
            'name': self.name,
            'type': 'gauge',
            'value': self.get(),
            'description': self.description
        }]

    def export_prometheus(self) -> List[str]:
        lines = []
        if self.description:
            lines.append(f'# HELP {self.name} {self.description}')
        lines.append(f'# TYPE {self.name} gauge')
        lines.append(f'{self.name} {self.get()}')
        return lines


class Histogram(Metric):
    def __init__(self, name: str, description: str = '', buckets: List[float] = None):
        super().__init__(name, description)
        if buckets is None:
            buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]

        self.buckets = sorted(buckets) + [float('inf')]
        self._bucket_counts = [0] * len(self.buckets)
        self._sum = 0.0
        self._count = 0
        self._lock = threading.Lock()

    def observe(self, value: float) -> None:
        with self._lock:
            self._sum += value
            self._count += 1

            for i, bucket_upper in enumerate(self.buckets):
                if value <= bucket_upper:
                    self._bucket_counts[i] += 1
                    break

    def collect(self) -> List[Dict[str, Union[str, float, Dict]]]:
        with self._lock:
            result = []

            result.append({
                'name': f'{self.name}_sum',
                'type': 'counter',
                'value': self._sum,
                'description': f'{self.description} sum'
            })

            result.append({
                'name': f'{self.name}_count',
                'type': 'counter',
                'value': self._count,
                'description': f'{self.description} count'
            })

            cumulative_count = 0
            for i, bucket_upper in enumerate(self.buckets[:-1]):
                cumulative_count += self._bucket_counts[i]
                result.append({
                    'name': f'{self.name}_bucket',
                    'type': 'counter',
                    'value': cumulative_count,
                    'description': f'{self.description} bucket le {bucket_upper}',
                    'labels': {'le': str(bucket_upper)}
                })

            result.append({
                'name': f'{self.name}_bucket',
                'type': 'counter',
                'value': self._count,
                'description': f'{self.description} bucket le +Inf',
                'labels': {'le': '+Inf'}
            })

            return result

    def export_prometheus(self) -> List[str]:
        lines = []
        if self.description:
            lines.append(f'# HELP {self.name} {self.description}')
        lines.append(f'# TYPE {self.name} histogram')

        with self._lock:
            lines.append(f'{self.name}_sum {self._sum}')
            lines.append(f'{self.name}_count {self._count}')
            cumulative_count = 0
            for i, bucket_upper in enumerate(self.buckets[:-1]):
                cumulative_count += self._bucket_counts[i]
                lines.append(f'{self.name}_bucket{{le="{bucket_upper}"}} {cumulative_count}')
            lines.append(f'{self.name}_bucket{{le="+Inf"}} {self._count}')

        return lines


# 测试代码
if __name__ == '__main__':
    collector = MetricCollector()

    # 测试计数器
    requests = collector.counter('http_requests_total', 'HTTP请求总数')
    requests.inc(5)

    # 测试仪表盘
    users = collector.gauge('active_users', '活跃用户数')
    users.set(100)

    # 测试直方图
    duration = collector.histogram('request_duration', '请求持续时间')
    duration.observe(0.5)
    duration.observe(1.2)

    print(collector.export_prometheus())