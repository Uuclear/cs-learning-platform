#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: Terraform 资源创建模拟
模拟 Terraform 的依赖图和资源创建过程
"""

from typing import Dict, List, Set
import time


class Resource:
    """表示一个基础设施资源"""

    def __init__(self, name: str, resource_type: str, dependencies: List[str] = None):
        self.name = name
        self.resource_type = resource_type
        self.dependencies = dependencies or []
        self.created = False

    def create(self) -> bool:
        """模拟资源创建过程"""
        print(f"正在创建 {self.resource_type} 资源: {self.name}")
        time.sleep(0.5)  # 模拟创建时间
        self.created = True
        print(f"✓ 成功创建 {self.resource_type} 资源: {self.name}")
        return True


class TerraformSimulator:
    """Terraform 模拟器 - 处理资源依赖和创建顺序"""

    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        self.creation_order: List[str] = []

    def add_resource(self, resource: Resource):
        """添加资源到模拟器"""
        self.resources[resource.name] = resource

    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """构建依赖图"""
        graph = {}
        for name, resource in self.resources.items():
            graph[name] = set(resource.dependencies)
        return graph

    def _topological_sort(self, graph: Dict[str, Set[str]]) -> List[str]:
        """拓扑排序 - 确定资源创建顺序"""
        visited = set()
        temp_mark = set()
        result = []

        def visit(node: str):
            if node in temp_mark:
                raise ValueError(f"检测到循环依赖: {node}")
            if node not in visited:
                temp_mark.add(node)
                for dependency in graph.get(node, set()):
                    if dependency not in self.resources:
                        raise ValueError(f"未定义的依赖资源: {dependency}")
                    visit(dependency)
                temp_mark.remove(node)
                visited.add(node)
                result.append(node)

        for node in graph:
            if node not in visited:
                visit(node)

        return result

    def plan(self) -> List[str]:
        """生成执行计划"""
        print("=== Terraform 执行计划 ===")
        graph = self._build_dependency_graph()
        self.creation_order = self._topological_sort(graph)

        print("将按以下顺序创建资源:")
        for i, resource_name in enumerate(self.creation_order, 1):
            resource = self.resources[resource_name]
            deps = ", ".join(resource.dependencies) if resource.dependencies else "无依赖"
            print(f"{i}. {resource.resource_type} '{resource_name}' (依赖: {deps})")

        return self.creation_order

    def apply(self) -> bool:
        """应用计划并创建资源"""
        print("\n=== 开始应用变更 ===")
        for resource_name in self.creation_order:
            resource = self.resources[resource_name]
            # 验证所有依赖都已创建
            for dep_name in resource.dependencies:
                if not self.resources[dep_name].created:
                    raise RuntimeError(f"依赖资源 {dep_name} 尚未创建")
            resource.create()

        print("\n✓ 所有资源创建完成!")
        return True


def main():
    """主函数 - 演示 Terraform 模拟器"""
    print("🚀 欢迎使用 Terraform 模拟器!")
    print("本示例演示了 Terraform 如何处理资源依赖和创建顺序\n")

    # 创建模拟器实例
    tf = TerraformSimulator()

    # 添加资源 - 模拟 AWS 基础设施
    tf.add_resource(Resource("vpc", "aws_vpc", []))
    tf.add_resource(Resource("subnet_private", "aws_subnet", ["vpc"]))
    tf.add_resource(Resource("subnet_public", "aws_subnet", ["vpc"]))
    tf.add_resource(Resource("security_group", "aws_security_group", ["vpc"]))
    tf.add_resource(Resource("ec2_instance", "aws_instance", ["subnet_private", "security_group"]))
    tf.add_resource(Resource("rds_instance", "aws_db_instance", ["subnet_private", "security_group"]))

    try:
        # 生成计划
        tf.plan()

        # 应用变更
        tf.apply()

    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

    return True


if __name__ == "__main__":
    main()