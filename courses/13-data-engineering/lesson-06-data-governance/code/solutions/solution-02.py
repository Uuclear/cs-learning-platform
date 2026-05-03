#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据血缘追踪解决方案

这个解决方案提供了增强的数据血缘追踪功能，
包括影响分析、依赖可视化和变更影响评估。
"""

from typing import List, Dict, Set, Optional
import json


class EnhancedDataLineageTracker:
    """增强的数据血缘追踪器，支持更多功能"""

    def __init__(self):
        """初始化增强血缘追踪器"""
        self.lineage_graph = {}  # 存储血缘关系图
        self.processes = {}      # 存储处理过程信息
        self.data_quality_metrics = {}  # 存储每个节点的数据质量指标

    def add_source(self, source_name: str, description: str = "",
                   quality_metrics: Optional[Dict] = None):
        """添加数据源，可选包含质量指标

        Args:
            source_name: 数据源名称
            description: 数据源描述
            quality_metrics: 数据质量指标字典
        """
        if source_name not in self.lineage_graph:
            self.lineage_graph[source_name] = {
                "type": "source",
                "description": description,
                "downstream": set(),
                "upstream": set(),
                "created_at": self._get_timestamp()
            }

        if quality_metrics:
            self.data_quality_metrics[source_name] = quality_metrics

    def add_process(self, process_name: str, inputs: List[str], outputs: List[str],
                   description: str = "", transformation_logic: str = ""):
        """添加数据处理过程

        Args:
            process_name: 处理过程名称
            inputs: 输入数据源列表
            outputs: 输出数据源列表
            description: 处理过程描述
            transformation_logic: 转换逻辑描述
        """
        for input_node in inputs:
            if input_node not in self.lineage_graph:
                self.add_source(input_node)

        for output_node in outputs:
            if output_node not in self.lineage_graph:
                self.lineage_graph[output_node] = {
                    "type": "intermediate",
                    "description": f"处理输出: {process_name}",
                    "downstream": set(),
                    "upstream": set(),
                    "created_at": self._get_timestamp()
                }

        for input_node in inputs:
            self.lineage_graph[input_node]["downstream"].update(outputs)
            for output_node in outputs:
                self.lineage_graph[output_node]["upstream"].add(input_node)

        self.processes[process_name] = {
            "inputs": inputs,
            "outputs": outputs,
            "description": description,
            "transformation_logic": transformation_logic,
            "created_at": self._get_timestamp()
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

            for downstream in sorted(self.lineage_graph[current]["downstream"]):
                if dfs(downstream):
                    return True

            path.pop()
            return False

        dfs(source)
        return path if path and path[-1] == target else []

    def get_full_lineage(self, node: str) -> Dict:
        """获取节点的完整血缘信息

        Args:
            node: 节点名称

        Returns:
            完整血缘信息字典
        """
        if node not in self.lineage_graph:
            return {}

        upstream_nodes = self._get_all_upstream(node)
        downstream_nodes = self._get_all_downstream(node)

        return {
            "node": node,
            "info": self.lineage_graph[node],
            "upstream": list(upstream_nodes),
            "downstream": list(downstream_nodes),
            "quality_metrics": self.data_quality_metrics.get(node, {})
        }

    def _get_all_upstream(self, node: str) -> Set[str]:
        """递归获取所有上游节点

        Args:
            node: 当前节点名称

        Returns:
            所有上游节点集合
        """
        upstream = set()
        direct_upstream = self.get_upstream(node)
        upstream.update(direct_upstream)

        for upstream_node in direct_upstream:
            upstream.update(self._get_all_upstream(upstream_node))

        return upstream

    def _get_all_downstream(self, node: str) -> Set[str]:
        """递归获取所有下游节点

        Args:
            node: 当前节点名称

        Returns:
            所有下游节点集合
        """
        downstream = set()
        direct_downstream = self.get_downstream(node)
        downstream.update(direct_downstream)

        for downstream_node in direct_downstream:
            downstream.update(self._get_all_downstream(downstream_node))

        return downstream

    def _get_timestamp(self) -> str:
        """获取当前时间戳

        Returns:
            ISO格式的时间戳字符串
        """
        from datetime import datetime
        return datetime.now().isoformat()

    def visualize_lineage(self, node: str) -> str:
        """生成简单的血缘可视化文本

        Args:
            node: 要可视化的节点名称

        Returns:
            可视化文本
        """
        lineage = self.get_full_lineage(node)
        if not lineage:
            return f"节点 {node} 不存在"

        result = [f"血缘图谱 - 节点: {node}"]
        result.append("=" * 50)

        if lineage["upstream"]:
            result.append("上游依赖:")
            for upstream in sorted(lineage["upstream"]):
                result.append(f"  <- {upstream}")
        else:
            result.append("上游依赖: (无)")

        result.append(f"当前节点: {node}")

        if lineage["downstream"]:
            result.append("下游影响:")
            for downstream in sorted(lineage["downstream"]):
                result.append(f"  -> {downstream}")
        else:
            result.append("下游影响: (无)")

        return "\n".join(result)


def main():
    """主函数：演示增强数据血缘追踪功能"""
    # 创建追踪器实例
    tracker = EnhancedDataLineageTracker()

    # 添加带质量指标的数据源
    tracker.add_source(
        "raw_customer_data",
        "原始客户数据CSV文件",
        {"completeness": 0.95, "accuracy": 0.92, "freshness": "2023-05-02"}
    )

    tracker.add_source(
        "raw_order_data",
        "原始订单数据JSON文件",
        {"completeness": 0.98, "accuracy": 0.96, "freshness": "2023-05-02"}
    )

    # 添加处理过程
    tracker.add_process(
        "clean_customer_data",
        ["raw_customer_data"],
        ["cleaned_customer_data"],
        "清洗客户数据：去除重复、标准化格式、验证邮箱",
        "标准化姓名格式，验证邮箱有效性，去除无效记录"
    )

    tracker.add_process(
        "clean_order_data",
        ["raw_order_data"],
        ["cleaned_order_data"],
        "清洗订单数据：验证金额、标准化日期、去除无效订单",
        "验证订单金额为正数，标准化日期格式，过滤测试订单"
    )

    tracker.add_process(
        "join_customer_orders",
        ["cleaned_customer_data", "cleaned_order_data"],
        ["customer_order_summary"],
        "关联客户和订单数据，生成汇总报表",
        "按客户ID关联，计算每个客户的订单统计信息"
    )

    tracker.add_process(
        "create_sales_dashboard",
        ["customer_order_summary"],
        ["sales_analytics_dashboard"],
        "创建销售分析仪表板",
        "生成包含销售额、订单数量、客户活跃度的可视化仪表板"
    )

    print("=== 增强数据血缘追踪解决方案演示 ===\n")

    # 演示各种功能
    print("1. 销售分析仪表板的血缘可视化:")
    print(tracker.visualize_lineage("sales_analytics_dashboard"))
    print()

    print("2. 从原始客户数据到销售分析仪表板的路径:")
    path = tracker.find_impact_path("raw_customer_data", "sales_analytics_dashboard")
    if path:
        print("   " + " → ".join(path))
    else:
        print("   未找到路径")
    print()

    print("3. 客户订单汇总的完整血缘信息:")
    full_lineage = tracker.get_full_lineage("customer_order_summary")
    print(f"   上游节点: {full_lineage['upstream']}")
    print(f"   下游节点: {full_lineage['downstream']}")
    print()

    print("4. 原始客户数据的质量指标:")
    quality_metrics = tracker.data_quality_metrics.get("raw_customer_data", {})
    for metric, value in quality_metrics.items():
        print(f"   {metric}: {value}")


if __name__ == "__main__":
    main()