#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: Terraform 资源依赖图模拟
这是 example-01-terraform-simulation.py 的简化解决方案
"""

from typing import Dict, List
from collections import defaultdict, deque


class Resource:
    """表示一个基础设施资源"""

    def __init__(self, name: str, resource_type: str, dependencies: List[str] = None):
        self.name = name
        self.resource_type = resource_type
        self.dependencies = dependencies or []


class TerraformSimulator:
    """简化的 Terraform 模拟器"""

    def __init__(self):
        self.resources: Dict[str, Resource] = {}

    def add_resource(self, resource: Resource):
        """添加资源"""
        self.resources[resource.name] = resource

    def get_execution_order(self) -> List[str]:
        """获取执行顺序（拓扑排序）"""
        # 构建依赖图
        graph = defaultdict(list)
        in_degree = {}

        for name in self.resources:
            in_degree[name] = 0

        for resource in self.resources.values():
            for dep in resource.dependencies:
                graph[dep].append(resource.name)
                in_degree[resource.name] = in_degree.get(resource.name, 0) + 1

        # Kahn算法
        queue = deque([name for name, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result


def main():
    """主函数"""
    tf_sim = TerraformSimulator()

    # 添加资源
    tf_sim.add_resource(Resource("vpc", "aws_vpc", []))
    tf_sim.add_resource(Resource("subnet", "aws_subnet", ["vpc"]))
    tf_sim.add_resource(Resource("security_group", "aws_security_group", ["vpc"]))
    tf_sim.add_resource(Resource("instance", "aws_instance", ["subnet", "security_group"]))

    # 获取执行顺序
    order = tf_sim.get_execution_order()
    print("执行顺序:", order)


if __name__ == "__main__":
    main()