#!/usr/bin/env python3
"""
CDN路由模拟：基于地理位置选择最优边缘节点

这个示例演示了CDN如何根据用户地理位置选择最近的边缘节点，
从而减少延迟并提高访问速度。
"""

import math
import random
from typing import List, Tuple, Dict

class EdgeNode:
    """边缘节点类，代表CDN的一个边缘服务器"""

    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude  # 纬度
        self.longitude = longitude  # 经度

    def distance_to(self, user_lat: float, user_lon: float) -> float:
        """
        计算边缘节点到用户的距离（使用Haversine公式）

        Args:
            user_lat: 用户纬度
            user_lon: 用户经度

        Returns:
            距离（公里）
        """
        # 将角度转换为弧度
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(user_lat)
        lon2 = math.radians(user_lon)

        # Haversine公式计算两点间距离
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # 地球半径（公里）

        return c * r

class CDNRouter:
    """CDN路由器，负责为用户选择最优边缘节点"""

    def __init__(self):
        # 模拟全球分布的边缘节点
        self.edge_nodes: List[EdgeNode] = [
            EdgeNode("北京边缘节点", 39.9042, 116.4074),
            EdgeNode("上海边缘节点", 31.2304, 121.4737),
            EdgeNode("东京边缘节点", 35.6762, 139.6503),
            EdgeNode("新加坡边缘节点", 1.3521, 103.8198),
            EdgeNode("硅谷边缘节点", 37.7749, -122.4194),
            EdgeNode("纽约边缘节点", 40.7128, -74.0060),
            EdgeNode("伦敦边缘节点", 51.5074, -0.1278),
            EdgeNode("法兰克福边缘节点", 50.1109, 8.6821),
        ]

    def find_best_edge_node(self, user_lat: float, user_lon: float) -> Tuple[EdgeNode, float]:
        """
        为用户找到最近的边缘节点

        Args:
            user_lat: 用户纬度
            user_lon: 用户经度

        Returns:
            (最优边缘节点, 距离)
        """
        best_node = None
        min_distance = float('inf')

        for node in self.edge_nodes:
            distance = node.distance_to(user_lat, user_lon)
            if distance < min_distance:
                min_distance = distance
                best_node = node

        return best_node, min_distance

def simulate_user_requests():
    """模拟不同地区用户的请求"""
    print("=== CDN边缘节点路由模拟 ===\n")

    # 模拟不同地区的用户
    users = [
        ("北京用户", 39.9042, 116.4074),
        ("悉尼用户", -33.8688, 151.2093),
        ("巴黎用户", 48.8566, 2.3522),
        ("孟买用户", 19.0760, 72.8777),
    ]

    router = CDNRouter()

    for user_name, lat, lon in users:
        best_node, distance = router.find_best_edge_node(lat, lon)
        print(f"{user_name}:")
        print(f"  最近边缘节点: {best_node.name}")
        print(f"  距离: {distance:.2f} 公里")
        print(f"  预估延迟: {distance * 0.005:.2f} 毫秒\n")  # 假设光速传播，实际会有更多延迟

if __name__ == "__main__":
    simulate_user_requests()