#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可观测性课程示例 3: 分布式链路追踪

本示例演示如何模拟分布式追踪中的上下文传播，
包括 trace ID、span ID 和跨服务调用的上下文传递。
"""

import uuid
import time
import random
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class TraceContext:
    """追踪上下文数据类"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    sampled: bool = True

    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式（用于 HTTP 头部传递）"""
        result = {
            "trace-id": self.trace_id,
            "span-id": self.span_id,
            "sampled": str(self.sampled).lower()
        }
        if self.parent_span_id:
            result["parent-span-id"] = self.parent_span_id
        return result

    @classmethod
    def from_dict(cls, headers: Dict[str, str]) -> Optional['TraceContext']:
        """从字典格式创建追踪上下文"""
        if "trace-id" not in headers or "span-id" not in headers:
            return None

        return cls(
            trace_id=headers["trace-id"],
            span_id=headers["span-id"],
            parent_span_id=headers.get("parent-span-id"),
            sampled=headers.get("sampled", "true").lower() == "true"
        )


class Tracer:
    """追踪器类"""

    def __init__(self, service_name: str):
        """
        初始化追踪器

        Args:
            service_name: 服务名称
        """
        self.service_name = service_name
        self.active_spans = []

    def start_span(self, operation_name: str, parent_context: Optional[TraceContext] = None) -> TraceContext:
        """
        开始一个新的 span

        Args:
            operation_name: 操作名称
            parent_context: 父上下文

        Returns:
            新的追踪上下文
        """
        trace_id = parent_context.trace_id if parent_context else str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        parent_span_id = parent_context.span_id if parent_context else None

        context = TraceContext(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            sampled=True  # 简化示例，总是采样
        )

        print(f"🔍 [{self.service_name}] 开始 span: {operation_name}")
        print(f"   Trace ID: {trace_id[:8]}...")
        print(f"   Span ID: {span_id[:8]}...")
        if parent_span_id:
            print(f"   Parent Span ID: {parent_span_id[:8]}...")

        self.active_spans.append({
            "context": context,
            "operation": operation_name,
            "start_time": time.time()
        })

        return context

    def end_span(self, context: TraceContext) -> None:
        """
        结束一个 span

        Args:
            context: 要结束的上下文
        """
        for i, span_data in enumerate(self.active_spans):
            if span_data["context"].span_id == context.span_id:
                duration = time.time() - span_data["start_time"]
                operation = span_data["operation"]

                print(f"✅ [{self.service_name}] 结束 span: {operation} ({duration:.3f}s)")
                print(f"   Trace ID: {context.trace_id[:8]}...")

                self.active_spans.pop(i)
                break


def simulate_service_call(
    service_name: str,
    operation: str,
    incoming_context: Optional[TraceContext] = None,
    simulate_work: bool = True
) -> TraceContext:
    """
    模拟服务调用

    Args:
        service_name: 服务名称
        operation: 操作名称
        incoming_context: 传入的追踪上下文
        simulate_work: 是否模拟工作耗时

    Returns:
        当前 span 的追踪上下文
    """
    tracer = Tracer(service_name)
    context = tracer.start_span(operation, incoming_context)

    if simulate_work:
        # 模拟处理时间
        work_time = random.uniform(0.05, 0.2)
        time.sleep(work_time)

        # 模拟可能的子服务调用
        if random.random() < 0.3 and service_name != "database":
            child_services = ["auth-service", "cache-service", "database"]
            child_service = random.choice(child_services)
            child_operation = f"query_{child_service.replace('-', '_')}"
            simulate_service_call(child_service, child_operation, context, simulate_work=False)

    tracer.end_span(context)
    return context


def simulate_distributed_trace():
    """模拟分布式追踪场景"""
    print("=== 分布式追踪模拟开始 ===\n")

    # 用户发起请求
    user_request_context = simulate_service_call(
        "api-gateway",
        "handle_user_request"
    )

    # API 网关调用用户服务
    user_service_context = simulate_service_call(
        "user-service",
        "get_user_profile",
        user_request_context
    )

    # 用户服务调用订单服务
    order_service_context = simulate_service_call(
        "order-service",
        "get_user_orders",
        user_service_context
    )

    print(f"\n=== 分布式追踪完成 ===")
    print(f"完整追踪 ID: {user_request_context.trace_id}")
    print(f"总 span 数量: 3 (加上可能的子服务调用)")


def demonstrate_context_propagation():
    """演示上下文传播"""
    print("\n=== 上下文传播演示 ===")

    # 创建初始上下文
    original_context = TraceContext(
        trace_id="trace-123456789",
        span_id="span-abcdef123",
        sampled=True
    )

    print("原始上下文:")
    print(f"  {original_context.to_dict()}")

    # 模拟通过 HTTP 头部传递
    http_headers = original_context.to_dict()
    print("\n通过 HTTP 头部传递后:")
    print(f"  {http_headers}")

    # 在下游服务中重建上下文
    reconstructed_context = TraceContext.from_dict(http_headers)
    print("\n下游服务重建的上下文:")
    if reconstructed_context:
        print(f"  {reconstructed_context.to_dict()}")
        print(f"  Trace ID 匹配: {original_context.trace_id == reconstructed_context.trace_id}")
        print(f"  Parent Span ID: {reconstructed_context.parent_span_id}")


def main():
    """主函数"""
    print("=== 可观测性课程：分布式链路追踪示例 ===\n")
    simulate_distributed_trace()
    demonstrate_context_propagation()
    print("\n=== 链路追踪示例结束 ===")


if __name__ == "__main__":
    main()