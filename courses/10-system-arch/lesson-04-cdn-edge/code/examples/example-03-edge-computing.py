#!/usr/bin/env python3
"""
边缘计算模拟：对比边缘函数执行与源站服务器处理

这个示例演示了边缘计算的优势，通过比较在边缘节点
执行简单计算与回源到原始服务器的性能差异。
"""

import time
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Request:
    """请求数据结构"""
    user_id: str
    content: str
    geo_location: str  # 用户地理位置

class OriginServer:
    """模拟原始服务器（传统架构）"""

    def __init__(self):
        self.processing_delay = 0.2  # 源站处理延迟（秒）
        self.location = "us-east-1"  # 源站位置

    def process_request(self, request: Request) -> str:
        """
        处理请求（包含网络延迟 + 处理延迟）

        Args:
            request: 用户请求

        Returns:
            处理结果
        """
        # 模拟网络延迟（基于用户与源站的距离）
        network_delay = self._calculate_network_delay(request.geo_location)

        # 模拟处理时间
        time.sleep(network_delay + self.processing_delay)

        return f"Processed by origin server: {request.content}"

    def _calculate_network_delay(self, user_location: str) -> float:
        """根据用户位置计算网络延迟"""
        # 简化的延迟模型（秒）
        delay_map = {
            "us-east": 0.05,   # 美国东部用户
            "us-west": 0.08,   # 美国西部用户
            "eu-west": 0.12,   # 欧洲用户
            "ap-southeast": 0.20,  # 亚太用户
            "ap-northeast": 0.18,  # 日本/韩国用户
        }
        return delay_map.get(user_location, 0.15)

class EdgeFunction:
    """模拟边缘函数（边缘计算）"""

    def __init__(self):
        self.processing_delay = 0.05  # 边缘函数处理延迟（秒）

    def execute(self, request: Request) -> str:
        """
        在边缘节点执行函数

        Args:
            request: 用户请求

        Returns:
            执行结果
        """
        # 边缘函数延迟很低，因为靠近用户
        network_delay = 0.01  # 假设边缘节点就在用户附近

        time.sleep(network_delay + self.processing_delay)

        # 简单的边缘处理逻辑（例如：个性化内容、A/B测试、安全检查等）
        processed_content = self._process_content(request.content, request.user_id)
        return f"Processed by edge function: {processed_content}"

    def _process_content(self, content: str, user_id: str) -> str:
        """边缘函数的具体处理逻辑"""
        # 示例：基于用户ID的个性化处理
        if "welcome" in content.lower():
            return content + f" (个性化欢迎消息 for user {user_id})"
        elif "api" in content.lower():
            return f'{{"user": "{user_id}", "status": "active", "edge_processed": true}}'
        else:
            return content.upper()  # 简单转换

def simulate_edge_vs_origin():
    """模拟边缘计算与传统源站的对比"""
    print("=== 边缘计算 vs 源站服务器对比 ===\n")

    # 创建服务实例
    origin_server = OriginServer()
    edge_function = EdgeFunction()

    # 模拟不同地区的用户请求
    test_requests = [
        Request("user_001", "Welcome to our website!", "ap-southeast"),
        Request("user_002", "API call for user data", "eu-west"),
        Request("user_003", "Static content request", "us-west"),
        Request("user_004", "Dynamic page load", "ap-northeast"),
    ]

    print("传统源站架构:")
    origin_times = []
    for req in test_requests:
        start_time = time.time()
        result = origin_server.process_request(req)
        end_time = time.time()
        elapsed = end_time - start_time
        origin_times.append(elapsed)
        print(f"  {req.geo_location} → {result[:50]}... ({elapsed:.3f}s)")

    print(f"\n平均响应时间 (源站): {sum(origin_times)/len(origin_times):.3f}s")

    print("\n边缘计算架构:")
    edge_times = []
    for req in test_requests:
        start_time = time.time()
        result = edge_function.execute(req)
        end_time = time.time()
        elapsed = end_time - start_time
        edge_times.append(elapsed)
        print(f"  {req.geo_location} → {result[:50]}... ({elapsed:.3f}s)")

    print(f"\n平均响应时间 (边缘): {sum(edge_times)/len(edge_times):.3f}s")

    improvement = (sum(origin_times) - sum(edge_times)) / sum(origin_times) * 100
    print(f"\n性能提升: {improvement:.1f}%")

    print("\n边缘计算适用场景:")
    print("  ✓ 用户地理位置分散")
    print("  ✓ 需要低延迟响应")
    print("  ✓ 可以在边缘处理的逻辑（个性化、安全、缓存等）")
    print("  ✓ 减轻源站负载")

if __name__ == "__main__":
    simulate_edge_vs_origin()