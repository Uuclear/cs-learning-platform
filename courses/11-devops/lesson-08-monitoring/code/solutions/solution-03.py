#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：分布式追踪上下文
完整的分布式追踪实现，包含跨度管理和上下文传播
"""

import uuid
import time
import threading
from typing import Dict, Optional, Any, List
from contextlib import contextmanager


class Span:
    def __init__(self, name: str, trace_id: str, parent_span_id: Optional[str] = None):
        self.span_id = str(uuid.uuid4())
        self.trace_id = trace_id
        self.parent_span_id = parent_span_id
        self.name = name
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.tags: Dict[str, Any] = {}
        self.logs: List[Dict[str, Any]] = []

    def set_tag(self, key: str, value: Any) -> 'Span':
        self.tags[key] = value
        return self

    def log(self, message: str, **kwargs) -> 'Span':
        self.logs.append({
            'timestamp': time.time(),
            'message': message,
            **kwargs
        })
        return self

    def finish(self) -> None:
        self.end_time = time.time()

    def duration(self) -> float:
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
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
    def __init__(self, service_name: str):
        self.service_name = service_name
        self._local = threading.local()

    def _get_active_span(self) -> Optional[Span]:
        return getattr(self._local, 'current_span', None)

    def _set_active_span(self, span: Optional[Span]) -> None:
        self._local.current_span = span

    def start_span(self, name: str, parent_span: Optional[Span] = None) -> Span:
        if parent_span is None:
            parent_span = self._get_active_span()

        if parent_span is not None:
            trace_id = parent_span.trace_id
            parent_span_id = parent_span.span_id
        else:
            trace_id = str(uuid.uuid4())
            parent_span_id = None

        span = Span(name, trace_id, parent_span_id)
        span.set_tag('service.name', self.service_name)
        self._set_active_span(span)
        return span

    @contextmanager
    def span(self, name: str):
        span = self.start_span(name)
        try:
            yield span
        finally:
            span.finish()
            self._set_active_span(None)

    def inject_context(self, span: Span) -> Dict[str, str]:
        return {
            'trace-id': span.trace_id,
            'span-id': span.span_id,
            'parent-span-id': span.parent_span_id or '',
            'sampled': '1'
        }

    def extract_context(self, carrier: Dict[str, str]) -> Optional[Dict[str, str]]:
        trace_id = carrier.get('trace-id')
        span_id = carrier.get('span-id')
        parent_span_id = carrier.get('parent-span-id') or None

        if not trace_id or not span_id:
            return None

        return {
            'trace_id': trace_id,
            'parent_span_id': parent_span_id if parent_span_id else None
        }


# 测试代码
if __name__ == '__main__':
    tracer = Tracer('test-service')

    with tracer.span('test-operation') as span:
        span.set_tag('test', 'solution-03')
        span.log('测试日志消息', test_id='solution-03')

    print("分布式追踪解决方案测试完成")