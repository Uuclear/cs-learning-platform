#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据血缘追踪示例

这个示例演示了如何实现一个简单的数据血缘追踪系统，
用于记录数据从源头到最终消费的完整路径。
"""

from typing import List, Dict, Set


class DataLineageTracker:
    """数据血缘追踪器：记录数据从源到目标的转换过程"""

    def __init__(self):
        """初始化血缘追踪器"""
        self.lineage_graph = {}  # 存储血缘关系图
        self.processes = {}      # 存储处理过程信息

    def add_source(self, source_name: str, description: str = ""):
        """添加数据源

        Args:
            source_name: 数据源名称
            description: 数据源描述
        """
        if source_name not in self.lineage_graph:
            self.lineage_graph[source_name] = {
                "type": "source",
                "description": description,
                "downstream": set(),
                "upstream": set()
            }

    def add_process(self, process_name: str, inputs: List[str], outputs: List[str],
                   description: str = ""):
        """添加数据处理过程

        Args:
            process_name: 处理过程名称
            inputs: 输入数据源列表
            outputs: 输出数据源列表
            description: 处理过程描述
        """
        # 确保输入和输出都已注册
        for input_node in inputs:
            if input_node not in self.lineage_graph:
                self.add_source(input_node)

        for output_node in outputs:
            if output_node not in self.lineage_graph:
                self.lineage_graph[output_node] = {
                    "type": "intermediate",
                    "description": f"处理输出: {process_name}",
                    "downstream": set(),
                    "upstream": set()
                }

        # 建立血缘关系
        for input_node in inputs:
            self.lineage_graph[input_node]["downstream"].update(outputs)
            for output_node in outputs:
                self.lineage_graph[output_node]["upstream"].add(input_node)

        # 记录处理过程
        self.processes[process_name] = {
            "inputs": inputs,
            "outputs": outputs,
            "description": description
        }

    def get_upstream(self, node: str) -> Set[str]:
        """获取指定节点的所有上游依赖

        Args:
            node: 节点名称

        Returns:
            上游依赖集合
        """
        if node not in self.lineage_graph:
            return set()
        return self.lineage_graph[node]["upstream"].copy()

    def get_downstream(self, node: str) -> Set[str]:
        """获取指定节点的所有下游影响

        Args:
            node: 节点名称

        Returns:
            下游影响集合
        """
        if node not in self.lineage_graph:
            return set()
        return self.lineage_graph[node]["downstream"].copy()

    def find_impact_path(self, source: str, target: str) -> List[str]:
        """查找从源到目标的影响路径

        Args:
            source: 源节点名称
            target: 目标节点名称

        Returns:
            影响路径列表，如果不存在路径则返回空列表
        """
        if source not in self.lineage_graph or target not in self.lineage_graph:
            return []

        visited = set()
        path = []

        def dfs(current: str):
            """深度优先搜索查找路径"""
            if current == target:
                path.append(current)
                return True
            if current in visited:
                return False

            visited.add(current)
            path.append(current)

            for downstream in self.lineage_graph[current]["downstream"]:
                if dfs(downstream):
                    return True

            path.pop()
            return False

        dfs(source)
        return path if path and path[-1] == target else []


def main():
    """主函数：演示数据血缘追踪的使用"""
    # 创建血缘追踪器实例
    tracker = DataLineageTracker()

    # 添加数据源
    tracker.add_source("raw_customer_data", "原始客户数据CSV文件")
    tracker.add_source("raw_order_data", "原始订单数据JSON文件")
    tracker.add_source("raw_product_data", "原始产品数据数据库表")

    # 添加处理过程
    tracker.add_process(
        "clean_customer_data",
        ["raw_customer_data"],
        ["cleaned_customer_data"],
        "清洗客户数据：去除重复、标准化格式、验证邮箱"
    )

    tracker.add_process(
        "clean_order_data",
        ["raw_order_data"],
        ["cleaned_order_data"],
        "清洗订单数据：验证金额、标准化日期、去除无效订单"
    )

    tracker.add_process(
        "enrich_product_info",
        ["raw_product_data"],
        ["enriched_product_data"],
        "丰富产品信息：添加分类、品牌和供应商信息"
    )

    tracker.add_process(
        "join_customer_orders",
        ["cleaned_customer_data", "cleaned_order_data"],
        ["customer_order_summary"],
        "关联客户和订单数据，生成汇总报表"
    )

    tracker.add_process(
        "create_sales_dashboard",
        ["customer_order_summary", "enriched_product_data"],
        ["sales_analytics_dashboard"],
        "创建销售分析仪表板，包含客户、订单和产品维度"
    )

    # 查询血缘关系
    print("=== 数据血缘追踪演示 ===\n")

    print("1. 销售分析仪表板的上游依赖:")
    upstream = tracker.get_upstream("sales_analytics_dashboard")
    for dependency in sorted(upstream):
        print(f"   - {dependency}")

    print("\n2. 原始客户数据的下游影响:")
    downstream = tracker.get_downstream("raw_customer_data")
    for impact in sorted(downstream):
        print(f"   - {impact}")

    print("\n3. 从原始客户数据到销售分析仪表板的完整路径:")
    path = tracker.find_impact_path("raw_customer_data", "sales_analytics_dashboard")
    if path:
        print("   " + " → ".join(path))
    else:
        print("   未找到路径")

    print("\n4. 所有处理过程:")
    for process_name, process_info in tracker.processes.items():
        print(f"   {process_name}: {process_info['description']}")


if __name__ == "__main__":
    main()