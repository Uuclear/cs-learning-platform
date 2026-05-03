#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：分布式追踪上下文实现
模拟分布式追踪系统中的跨度创建、父子关系和上下文传播
"""

import uuid
import time
import threading
from typing import Dict, Optional, Any, List
from contextlib import contextmanager


class Span:
    """追踪跨度，代表一个操作的执行"""

    def __init__(self, name: str, trace_id: str, parent_span_id: Optional[str] = None):
        """
        初始化跨度

        Args:
            name: 跨度名称
            trace_id: 追踪ID
            parent_span_id: 父跨度ID（可选）
        """
        self.span_id = str(uuid.uuid4())
        self.trace_id = trace_id
        self.parent_span_id = parent_span_id
        self.name = name
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.tags: Dict[str, Any] = {}
        self.logs: List[Dict[str, Any]] = []

    def set_tag(self, key: str, value: Any) -> 'Span':
        """
        设置跨度标签

        Args:
            key: 标签键
            value: 标签值

        Returns:
            Span: 当前跨度实例（支持链式调用）
        """
        self.tags[key] = value
        return self

    def log(self, message: str, **kwargs) -> 'Span':
        """
        记录跨度日志

        Args:
            message: 日志消息
            **kwargs: 额外的日志字段

        Returns:
            Span: 当前跨度实例（支持链式调用）
        """
        self.logs.append({
            'timestamp': time.time(),
            'message': message,
            **kwargs
        })
        return self

    def finish(self) -> None:
        """结束跨度"""
        self.end_time = time.time()

    def duration(self) -> float:
        """
        获取跨度持续时间（秒）

        Returns:
            float: 持续时间
        """
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式

        Returns:
            Dict: 跨度数据字典
        """
        return {
            'span_id': self.span_id,
            'trace_id': self.trace_id,
            'parent_span_id': self.parent_span_id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration(),
            'tags': self.tags,
            'logs': self.logs
        }


class Tracer:
    """追踪器，用于创建和管理跨度"""

    def __init__(self, service_name: str):
        """
        初始化追踪器

        Args:
            service_name: 服务名称
        """
        self.service_name = service_name
        self._local = threading.local()

    def _get_active_span(self) -> Optional[Span]:
        """获取当前活跃的跨度"""
        return getattr(self._local, 'current_span', None)

    def _set_active_span(self, span: Optional[Span]) -> None:
        """设置当前活跃的跨度"""
        self._local.current_span = span

    def start_span(self, name: str, parent_span: Optional[Span] = None) -> Span:
        """
        开始一个新的跨度

        Args:
            name: 跨度名称
            parent_span: 父跨度（可选）

        Returns:
            Span: 新创建的跨度
        """
        # 如果没有指定父跨度，使用当前活跃的跨度
        if parent_span is None:
            parent_span = self._get_active_span()

        # 如果有父跨度，使用相同的trace_id
        if parent_span is not None:
            trace_id = parent_span.trace_id
            parent_span_id = parent_span.span_id
        else:
            # 创建新的trace_id
            trace_id = str(uuid.uuid4())
            parent_span_id = None

        span = Span(name, trace_id, parent_span_id)
        span.set_tag('service.name', self.service_name)

        # 设置为当前活跃跨度
        self._set_active_span(span)
        return span

    @contextmanager
    def span(self, name: str):
        """
        跨度上下文管理器

        Args:
            name: 跨度名称
        """
        span = self.start_span(name)
        try:
            yield span
        finally:
            span.finish()
            # 恢复父跨度为当前活跃跨度
            parent_span_id = span.parent_span_id
            if parent_span_id:
                # 在真实场景中，我们会从存储中查找父跨度
                # 这里简化处理，直接清除当前跨度
                pass
            self._set_active_span(None)

    def inject_context(self, span: Span) -> Dict[str, str]:
        """
        注入追踪上下文到载体中（用于跨服务传播）

        Args:
            span: 要注入上下文的跨度

        Returns:
            Dict[str, str]: 包含追踪上下文的字典
        """
        return {
            'trace-id': span.trace_id,
            'span-id': span.span_id,
            'parent-span-id': span.parent_span_id or '',
            'sampled': '1'
        }

    def extract_context(self, carrier: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        从载体中提取追踪上下文

        Args:
            carrier: 包含追踪上下文的载体

        Returns:
            Optional[Dict]: 提取的上下文信息
        """
        trace_id = carrier.get('trace-id')
        span_id = carrier.get('span-id')
        parent_span_id = carrier.get('parent-span-id') or None

        if not trace_id or not span_id:
            return None

        return {
            'trace_id': trace_id,
            'parent_span_id': parent_span_id if parent_span_id else None
        }


def simulate_http_request(tracer: Tracer, request_id: str) -> None:
    """
    模拟HTTP请求处理，包含多个子操作

    Args:
        tracer: 追踪器实例
        request_id: 请求ID
    """
    with tracer.span('http.request') as root_span:
        root_span.set_tag('http.method', 'GET')
        root_span.set_tag('http.url', '/api/users/profile')
        root_span.set_tag('request.id', request_id)

        # 模拟认证
        with tracer.span('auth.validate') as auth_span:
            auth_span.log('验证用户令牌', token_type='JWT')
            time.sleep(0.01)  # 模拟处理时间

        # 模拟数据库查询
        with tracer.span('db.query') as db_span:
            db_span.set_tag('db.statement', 'SELECT * FROM users WHERE id = ?')
            db_span.set_tag('db.system', 'postgresql')
            db_span.log('执行查询', user_id='user-123')
            time.sleep(0.02)

        # 模拟外部API调用
        with tracer.span('external.api.call') as api_span:
            api_span.set_tag('http.url', 'https://payment-api.example.com/validate')
            api_span.set_tag('peer.service', 'payment-service')

            # 模拟上下文传播到外部服务
            context = tracer.inject_context(api_span)
            print(f"  传播到外部服务的上下文: {context}")

            time.sleep(0.03)


def main():
    """主函数，演示分布式追踪的使用"""
    print("=== 分布式追踪上下文演示 ===")

    # 创建追踪器
    tracer = Tracer('user-service')

    # 模拟处理多个请求
    for i in range(2):
        request_id = f'req-{i+1:04d}'
        print(f"\n处理请求: {request_id}")
        simulate_http_request(tracer, request_id)

    print("\n=== 分布式追踪演示完成 ===")


if __name__ == '__main__':
    main()