#!/usr/bin/env python3
"""
解决方案3: 边缘计算优化

这个解决方案展示了如何在边缘计算中实现
复杂的业务逻辑，同时保持低延迟。
"""

import time
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class EdgeRequest:
    user_id: str
    content: str
    geo_location: str
    device_type: str
    headers: Dict[str, str]

class OptimizedEdgeFunction:
    def __init__(self):
        self.processing_delay = 0.02  # 优化后的处理延迟

    def execute(self, request: EdgeRequest) -> Dict[str, Any]:
        start_time = time.time()

        # 1. 安全检查（在边缘执行）
        if not self._security_check(request):
            return {"error": "Security check failed", "status": 403}

        # 2. 个性化处理
        personalized_content = self._personalize_content(request)

        # 3. A/B测试路由
        ab_test_group = self._get_ab_test_group(request.user_id)

        # 4. 缓存决策
        should_cache = self._should_cache(request)

        processing_time = time.time() - start_time

        return {
            "content": personalized_content,
            "ab_test_group": ab_test_group,
            "should_cache": should_cache,
            "edge_processing_time": processing_time,
            "geo_location": request.geo_location,
            "device_type": request.device_type
        }

    def _security_check(self, request: EdgeRequest) -> bool:
        """边缘安全检查"""
        # 检查基本的请求头
        user_agent = request.headers.get("user-agent", "")
        if "bot" in user_agent.lower() and "google" not in user_agent.lower():
            return False

        # 检查请求频率（简单实现）
        ip_hash = hash(request.user_id) % 1000
        if ip_hash < 50:  # 模拟5%的恶意请求
            return False

        return True

    def _personalize_content(self, request: EdgeRequest) -> str:
        """基于用户和设备的个性化内容"""
        base_content = request.content

        # 移动设备优化
        if request.device_type == "mobile":
            base_content += " [Mobile Optimized]"

        # 地理位置个性化
        region_map = {
            "ap-southeast": "欢迎来自东南亚的用户！",
            "eu-west": "Welcome from Europe!",
            "us-east": "Welcome from the East Coast!",
        }
        region_message = region_map.get(request.geo_location, "Welcome!")
        base_content += f" {region_message}"

        return base_content

    def _get_ab_test_group(self, user_id: str) -> str:
        """A/B测试分组"""
        # 基于用户ID的确定性分组
        group_hash = hash(user_id) % 100
        if group_hash < 33:
            return "A"
        elif group_hash < 66:
            return "B"
        else:
            return "C"

    def _should_cache(self, request: EdgeRequest) -> bool:
        """智能缓存决策"""
        # 动态内容不缓存
        if "api" in request.content.lower() or "dynamic" in request.content.lower():
            return False

        # 移动设备请求可能需要不同缓存策略
        if request.device_type == "mobile":
            return True  # 移动设备更需要缓存

        # 默认缓存静态内容
        return True

def main():
    edge_function = OptimizedEdgeFunction()

    # 测试请求
    test_requests = [
        EdgeRequest(
            user_id="user_123",
            content="Welcome to our site!",
            geo_location="ap-southeast",
            device_type="mobile",
            headers={"user-agent": "iPhone Safari"}
        ),
        EdgeRequest(
            user_id="user_456",
            content="API call for dashboard",
            geo_location="us-east",
            device_type="desktop",
            headers={"user-agent": "Chrome Desktop"}
        )
    ]

    for req in test_requests:
        result = edge_function.execute(req)
        print(f"请求处理结果:")
        print(f"  内容: {result['content'][:50]}...")
        print(f"  A/B测试组: {result['ab_test_group']}")
        print(f"  是否缓存: {result['should_cache']}")
        print(f"  处理时间: {result['edge_processing_time']:.4f}s")
        print()

if __name__ == "__main__":
    main()