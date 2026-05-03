#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：重构优先级计算器
基于代码复杂度、使用频率和变更历史计算重构优先级
"""

import ast
import os
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class CodeComplexityAnalyzer(ast.NodeVisitor):
    """代码复杂度分析器"""

    def __init__(self):
        self.complexity = 0
        self.nested_level = 0

    def visit_If(self, node):
        """处理if语句 - 增加复杂度"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """处理for循环 - 增加复杂度"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """处理while循环 - 增加复杂度"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        """处理try语句 - 增加复杂度"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """处理函数定义"""
        # 重置复杂度计数器用于单个函数分析
        old_complexity = self.complexity
        self.complexity = 0
        self.generic_visit(node)
        function_complexity = self.complexity
        self.complexity = old_complexity + function_complexity


def calculate_cyclomatic_complexity(file_path: str) -> float:
    """计算文件的圈复杂度"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        analyzer = CodeComplexityAnalyzer()
        analyzer.visit(tree)
        return float(analyzer.complexity)
    except Exception:
        return 0.0


def estimate_usage_frequency(file_path: str) -> float:
    """估算文件的使用频率（基于文件大小和修改时间的简单启发式）"""
    try:
        stat = os.stat(file_path)
        size_score = min(1.0, stat.st_size / 10000)  # 文件越大，使用可能越频繁
        # 简化的启发式：最近修改的文件可能更活跃
        import time
        days_since_modified = (time.time() - stat.st_mtime) / (24 * 3600)
        recency_score = max(0.1, 1.0 - (days_since_modified / 365))  # 一年内为1.0，逐年递减
        return (size_score + recency_score) / 2
    except Exception:
        return 0.5


def get_change_history_score(file_path: str) -> float:
    """获取变更历史分数（模拟值，实际项目中可集成git历史）"""
    # 在实际项目中，这里会分析git提交历史
    # 现在使用简单的启发式：假设频繁修改的文件需要更多关注
    filename = os.path.basename(file_path).lower()
    if 'service' in filename or 'model' in filename:
        return 0.8  # 核心业务文件
    elif 'util' in filename or 'helper' in filename:
        return 0.6  # 工具文件
    else:
        return 0.4  # 其他文件


def calculate_refactoring_priority(
    file_path: str,
    complexity_weight: float = 0.4,
    usage_weight: float = 0.3,
    change_weight: float = 0.3
) -> float:
    """
    计算重构优先级分数
    :param file_path: 文件路径
    :param complexity_weight: 复杂度权重
    :param usage_weight: 使用频率权重
    :param change_weight: 变更历史权重
    :return: 优先级分数 (0-10)
    """
    if not os.path.exists(file_path):
        return 0.0

    complexity = min(10.0, calculate_cyclomatic_complexity(file_path) / 5.0)
    usage = estimate_usage_frequency(file_path) * 10.0
    change_score = get_change_history_score(file_path) * 10.0

    priority = (
        complexity * complexity_weight +
        usage * usage_weight +
        change_score * change_weight
    )

    return min(10.0, priority)


def analyze_directory(directory: str) -> List[Tuple[str, float]]:
    """分析目录中所有Python文件的重构优先级"""
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                priority = calculate_refactoring_priority(file_path)
                if priority > 0:
                    results.append((file_path, priority))

    # 按优先级降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def main():
    """主函数"""
    import sys

    if len(sys.argv) != 2:
        print("用法: python example-03-refactoring-priority.py <directory_or_file>")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        # 分析单个文件
        priority = calculate_refactoring_priority(path)
        print(f"文件 {path} 的重构优先级: {priority:.2f}/10.0")
    elif os.path.isdir(path):
        # 分析整个目录
        results = analyze_directory(path)
        print(f"目录 {path} 中的重构优先级排名:")
        print("-" * 60)
        for i, (file_path, priority) in enumerate(results[:10], 1):  # 显示前10个
            print(f"{i:2d}. {os.path.basename(file_path):20s} - {priority:.2f}/10.0")
    else:
        print(f"路径 {path} 不存在")


if __name__ == "__main__":
    main()