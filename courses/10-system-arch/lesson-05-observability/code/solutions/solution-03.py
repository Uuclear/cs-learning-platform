#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可观测性课程解决方案 3: 分布式追踪上下文

此解决方案展示了更健壮的分布式追踪上下文实现，
包括 W3C Trace Context 标准兼容性和更好的错误处理。
"""

import uuid
import re
from typing import Optional, Dict, Tuple


class W3CTraceContext:
    """
    W3C Trace Context 标准兼容的追踪上下文实现

    参考: https://www.w3.org/TR/trace-context/
    """

    # Trace ID 格式: 32个十六进制字符
    TRACE_ID_PATTERN = re.compile(r'^[0-9a-f]{32}$')

    # Span ID 格式: 16个十六进制字符
    SPAN_ID_PATTERN = re.compile(r'^[0-9a-f]{16}$')

    def __init__(self, trace_id: str, span_id: str, trace_flags: str = "01"):
        """
        初始化追踪上下文

        Args:
            trace_id: 32字符的十六进制 trace ID
            span_id: 16字符的十六进制 span ID
            trace_flags: 2字符的十六进制 trace flags (默认采样)
        """
        if not self.TRACE_ID_PATTERN.match(trace_id):
            raise ValueError("Invalid trace_id format. Must be 32 hex characters.")

        if not self.SPAN_ID_PATTERN.match(span_id):
            raise ValueError("Invalid span_id format. Must be 16 hex characters.")

        if not re.match(r'^[0-9a-f]{2}$', trace_flags):
            raise ValueError("Invalid trace_flags format. Must be 2 hex characters.")

        self.trace_id = trace_id
        self.span_id = span_id
        self.trace_flags = trace_flags

    @classmethod
    def generate(cls) -> 'W3CTraceContext':
        """生成新的追踪上下文"""
        trace_id = uuid.uuid4().hex  # 32字符
        span_id = uuid.uuid4().hex[:16]  # 16字符
        return cls(trace_id, span_id)

    def is_sampled(self) -> bool:
        """检查是否启用采样"""
        return self.trace_flags[-1] == '1'

    def to_traceparent_header(self) -> str:
        """
        转换为 traceparent HTTP 头部值

        格式: 00-{trace-id}-{span-id}-{trace-flags}
        """
        return f"00-{self.trace_id}-{self.span_id}-{self.trace_flags}"

    @classmethod
    def from_traceparent_header(cls, header_value: str) -> Optional['W3CTraceContext']:
        """
        从 traceparent HTTP 头部值创建追踪上下文

        Args:
            header_value: traceparent 头部值

        Returns:
            W3CTraceContext 实例或 None（如果无效）
        """
        try:
            parts = header_value.strip().split('-')
            if len(parts) < 4:
                return None

            version = parts[0]
            if version != "00":
                # 不支持的版本
                return None

            trace_id = parts[1]
            span_id = parts[2]
            trace_flags = parts[3][:2]  # 只取前2个字符

            return cls(trace_id, span_id, trace_flags)

        except (IndexError, ValueError):
            return None

    def create_child_context(self) -> 'W3CTraceContext':
        """创建子 span 上下文"""
        child_span_id = uuid.uuid4().hex[:16]
        return W3CTraceContext(self.trace_id, child_span_id, self.trace_flags)

    def __str__(self) -> str:
        return f"W3CTraceContext(trace_id={self.trace_id[:8]}..., span_id={self.span_id[:8]}..., sampled={self.is_sampled()})"

    def __repr__(self) -> str:
        return self.__str__()


def demonstrate_w3c_trace_context():
    """演示 W3C Trace Context 使用"""
    print("=== W3C Trace Context 演示 ===\n")

    # 1. 生成新的追踪上下文
    root_context = W3CTraceContext.generate()
    print(f"根上下文: {root_context}")
    print(f"Traceparent 头部: {root_context.to_traceparent_header()}")
    print()

    # 2. 创建子上下文
    child_context = root_context.create_child_context()
    print(f"子上下文: {child_context}")
    print(f"相同的 Trace ID: {root_context.trace_id == child_context.trace_id}")
    print()

    # 3. 从头部重建上下文
    traceparent_header = child_context.to_traceparent_header()
    reconstructed = W3CTraceContext.from_traceparent_header(traceparent_header)
    print(f"从头部重建: {reconstructed}")
    print(f"重建成功: {reconstructed is not None}")
    if reconstructed:
        print(f"Trace ID 匹配: {child_context.trace_id == reconstructed.trace_id}")
        print(f"Span ID 匹配: {child_context.span_id == reconstructed.span_id}")
    print()

    # 4. 测试无效输入
    invalid_cases = [
        "00-invalid-trace-id-span-id-01",  # 无效的 trace ID
        "01-1234567890abcdef1234567890abcdef-1234567890abcdef-01",  # 不支持的版本
        "00-1234567890abcdef1234567890abcdef-1234567890ab-01",  # 无效的 span ID
    ]

    print("无效输入测试:")
    for case in invalid_cases:
        result = W3CTraceContext.from_traceparent_header(case)
        print(f"  {case[:50]}... -> {result is None}")


class TraceContextPropagator:
    """追踪上下文传播器"""

    @staticmethod
    def extract(headers: Dict[str, str]) -> Optional[W3CTraceContext]:
        """从 HTTP 头部提取追踪上下文"""
        traceparent = headers.get("traceparent")
        if traceparent:
            return W3CTraceContext.from_traceparent_header(traceparent)
        return None

    @staticmethod
    def inject(context: W3CTraceContext, headers: Dict[str, str]) -> None:
        """将追踪上下文注入 HTTP 头部"""
        headers["traceparent"] = context.to_traceparent_header()


def simulate_service_chain():
    """模拟服务链调用"""
    print("=== 服务链调用模拟 ===\n")

    propagator = TraceContextPropagator()

    # 客户端发起请求
    client_context = W3CTraceContext.generate()
    http_headers = {}
    propagator.inject(client_context, http_headers)

    print(f"客户端上下文: {client_context}")
    print(f"传递的头部: {http_headers}")
    print()

    # API 网关接收请求
    gateway_extracted = propagator.extract(http_headers)
    print(f"API 网关提取: {gateway_extracted}")

    if gateway_extracted:
        # API 网关创建子 span
        gateway_child = gateway_extracted.create_child_context()
        gateway_headers = {}
        propagator.inject(gateway_child, gateway_headers)
        print(f"API 网关子上下文: {gateway_child}")
        print()

        # 用户服务接收请求
        user_service_extracted = propagator.extract(gateway_headers)
        print(f"用户服务提取: {user_service_extracted}")

        if user_service_extracted:
            print(f"完整链路 Trace ID: {user_service_extracted.trace_id}")


def main():
    """主函数"""
    demonstrate_w3c_trace_context()
    print()
    simulate_service_chain()


if __name__ == "__main__":
    main()