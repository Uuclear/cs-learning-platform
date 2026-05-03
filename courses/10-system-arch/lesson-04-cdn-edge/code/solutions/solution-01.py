#!/usr/bin/env python3
"""
解决方案1: CDN路由优化

这个解决方案实现了更智能的CDN路由策略，
考虑了网络状况、节点负载和地理位置。
"""

import math
import random
from typing import List, Tuple, Dict, Optional

class EdgeNode:
    def __init__(self, name: str, latitude: float, longitude: float,
                 load: float = 0.0, network_quality: float = 1.0):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.load = load  # 节点负载 (0.0 - 1.0)
        self.network_quality = network_quality  # 网络质量 (0.0 - 1.0)

    def distance_to(self, user_lat: float, user_lon: float) -> float:
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(user_lat)
        lon2 = math.radians(user_lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371

        return c * r

class AdvancedCDNRouter:
    def __init__(self):
        self.edge_nodes: List[EdgeNode] = [
            EdgeNode("北京边缘节点", 39.9042, 116.4074, 0.3, 0.95),
            EdgeNode("上海边缘节点", 31.2304, 121.4737, 0.4, 0.92),
            EdgeNode("东京边缘节点", 35.6762, 139.6503, 0.2, 0.98),
            EdgeNode("新加坡边缘节点", 1.3521, 103.8198, 0.5, 0.90),
            EdgeNode("硅谷边缘节点", 37.7749, -122.4194, 0.6, 0.96),
            EdgeNode("纽约边缘节点", 40.7128, -74.0060, 0.4, 0.94),
            EdgeNode("伦敦边缘节点", 51.5074, -0.1278, 0.3, 0.93),
            EdgeNode("法兰克福边缘节点", 50.1109, 8.6821, 0.2, 0.97),
        ]

    def find_best_edge_node(self, user_lat: float, user_lon: float) -> Tuple[EdgeNode, float]:
        best_node = None
        min_score = float('inf')

        for node in self.edge_nodes:
            distance = node.distance_to(user_lat, user_lon)

            # 综合评分：距离 + 负载 + 网络质量
            # 距离越近越好，负载越低越好，网络质量越高越好
            distance_score = distance / 1000  # 归一化距离分数
            load_penalty = node.load * 50  # 负载惩罚
            quality_bonus = (1 - node.network_quality) * 20  # 网络质量奖励

            total_score = distance_score + load_penalty + quality_bonus

            if total_score < min_score:
                min_score = total_score
                best_node = node

        distance = best_node.distance_to(user_lat, user_lon)
        return best_node, distance

def main():
    router = AdvancedCDNRouter()

    # 测试用例
    test_users = [
        ("悉尼用户", -33.8688, 151.2093),
        ("莫斯科用户", 55.7558, 37.6173),
    ]

    for user_name, lat, lon in test_users:
        best_node, distance = router.find_best_edge_node(lat, lon)
        print(f"{user_name} → {best_node.name} ({distance:.2f} km)")

if __name__ == "__main__":
    main()