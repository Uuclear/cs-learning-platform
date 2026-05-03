#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：高级重构优先级计算器
集成多种指标和权重配置，支持自定义规则
"""

import ast
import os
import subprocess
from typing import Dict, List, Tuple, Optional, Callable
from collections import defaultdict


class AdvancedCodeComplexityAnalyzer(ast.NodeVisitor):
    """高级代码复杂度分析器"""

    def __init__(self):
        self.complexity = 0
        self.function_complexities = {}
        self.current_function = None
        self.nesting_depth = 0

    def visit_FunctionDef(self, node):
        """处理函数定义"""
        old_function = self.current_function
        old_complexity = self.complexity
        old_nesting = self.nesting_depth

        self.current_function = node.name
        self.complexity = 0
        self.nesting_depth = 0

        self.generic_visit(node)

        # 保存函数复杂度
        self.function_complexities[node.name] = self.complexity

        # 恢复状态
        self.current_function = old_function
        self.complexity = old_complexity + self.complexity
        self.nesting_depth = old_nesting

    def visit_If(self, node):
        """处理if语句"""
        self.complexity += 1
        self.nesting_depth += 1
        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_For(self, node):
        """处理for循环"""
        self.complexity += 1
        self.nesting_depth += 1
        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_While(self, node):
        """处理while循环"""
        self.complexity += 1
        self.nesting_depth += 1
        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_Try(self, node):
        """处理try语句"""
        self.complexity += 1
        self.nesting_depth += 1
        self.generic_visit(node)
        self.nesting_depth -= 1

    def visit_BoolOp(self, node):
        """处理布尔操作（and/or）"""
        self.complexity += len(node.values) - 1
        self.generic_visit(node)


def calculate_cyclomatic_complexity(file_path: str) -> float:
    """计算圈复杂度"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        analyzer = AdvancedCodeComplexityAnalyzer()
        analyzer.visit(tree)
        return float(analyzer.complexity)
    except Exception:
        return 0.0


def calculate_maintainability_index(file_path: str) -> float:
    """计算可维护性指数（简化版）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        blank_lines = sum(1 for line in lines if not line.strip())
        code_lines = total_lines - blank_lines

        if code_lines == 0:
            return 100.0

        comment_ratio = comment_lines / code_lines
        complexity = calculate_cyclomatic_complexity(file_path)

        # 简化的可维护性指数公式
        maintainability = 171 - 5.2 * (complexity / code_lines) - 0.23 * (code_lines) - 16.2 * comment_ratio
        return max(0.0, min(100.0, maintainability))

    except Exception:
        return 50.0


def get_git_change_frequency(file_path: str) -> float:
    """获取git变更频率（如果在git仓库中）"""
    try:
        # 检查是否在git仓库中
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                              capture_output=True, text=True, cwd=os.path.dirname(file_path))
        if result.returncode != 0:
            return 0.5  # 不在git仓库中，返回默认值

        # 获取文件的提交历史
        result = subprocess.run(['git', 'log', '--oneline', '--follow', '--', os.path.basename(file_path)],
                              capture_output=True, text=True, cwd=os.path.dirname(file_path))
        if result.returncode == 0:
            commit_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            # 转换为0-1范围的分数
            return min(1.0, commit_count / 50.0)  # 假设50次提交是高频率
        else:
            return 0.3  # git命令失败，返回较低分数

    except Exception:
        return 0.3


def estimate_usage_frequency(file_path: str) -> float:
    """估算使用频率"""
    try:
        stat = os.stat(file_path)
        size_score = min(1.0, stat.st_size / 10000)  # 文件越大，使用可能越频繁

        # 结合git变更频率
        git_score = get_git_change_frequency(file_path)

        return (size_score * 0.6 + git_score * 0.4)
    except Exception:
        return 0.5


def get_code_quality_metrics(file_path: str) -> Dict[str, float]:
    """获取代码质量指标"""
    if not os.path.exists(file_path):
        return {'complexity': 0.0, 'maintainability': 0.0, 'usage_frequency': 0.0}

    complexity = calculate_cyclomatic_complexity(file_path)
    maintainability = calculate_maintainability_index(file_path)
    usage_frequency = estimate_usage_frequency(file_path)

    return {
        'complexity': min(10.0, complexity / 5.0),  # 归一化到0-10
        'maintainability': maintainability / 10.0,  # 归一化到0-10
        'usage_frequency': usage_frequency * 10.0   # 归一化到0-10
    }


class RefactoringPriorityCalculator:
    """重构优先级计算器"""

    def __init__(self,
                 complexity_weight: float = 0.4,
                 maintainability_weight: float = 0.3,
                 usage_weight: float = 0.3):
        self.weights = {
            'complexity': complexity_weight,
            'maintainability': maintainability_weight,
            'usage_frequency': usage_weight
        }

    def calculate_priority(self, file_path: str) -> float:
        """计算重构优先级"""
        metrics = get_code_quality_metrics(file_path)

        # 可维护性越低，优先级越高（所以用10 - maintainability）
        priority = (
            metrics['complexity'] * self.weights['complexity'] +
            (10.0 - metrics['maintainability']) * self.weights['maintainability'] +
            metrics['usage_frequency'] * self.weights['usage_frequency']
        )

        return min(10.0, priority)

    def analyze_directory(self, directory: str,
                         min_priority: float = 3.0) -> List[Tuple[str, float, Dict[str, float]]]:
        """分析目录中的所有Python文件"""
        results = []

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    priority = self.calculate_priority(file_path)
                    if priority >= min_priority:
                        metrics = get_code_quality_metrics(file_path)
                        results.append((file_path, priority, metrics))

        # 按优先级降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def generate_detailed_report(self, directory: str) -> str:
        """生成详细报告"""
        results = self.analyze_directory(directory)
        if not results:
            return f"目录 {directory} 中没有发现需要重构的文件。"

        report_lines = [f"重构优先级分析报告 - 目录: {directory}", "=" * 60]

        for i, (file_path, priority, metrics) in enumerate(results[:15], 1):  # 显示前15个
            rel_path = os.path.relpath(file_path, directory)
            report_lines.append(f"\n{i:2d}. {rel_path}")
            report_lines.append(f"    重构优先级: {priority:.2f}/10.0")
            report_lines.append(f"    圈复杂度:   {metrics['complexity']:.2f}/10.0")
            report_lines.append(f"    可维护性:   {metrics['maintainability']:.2f}/10.0")
            report_lines.append(f"    使用频率:   {metrics['usage_frequency']:.2f}/10.0")

        return "\n".join(report_lines)


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python solution-03.py <directory_or_file> [min_priority]")
        sys.exit(1)

    path = sys.argv[1]
    min_priority = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0

    calculator = RefactoringPriorityCalculator()

    if os.path.isfile(path):
        priority = calculator.calculate_priority(path)
        metrics = get_code_quality_metrics(path)
        print(f"文件 {path} 的重构优先级分析:")
        print(f"  重构优先级: {priority:.2f}/10.0")
        print(f"  圈复杂度:   {metrics['complexity']:.2f}/10.0")
        print(f"  可维护性:   {metrics['maintainability']:.2f}/10.0")
        print(f"  使用频率:   {metrics['usage_frequency']:.2f}/10.0")
    elif os.path.isdir(path):
        print(calculator.generate_detailed_report(path))
    else:
        print(f"路径 {path} 不存在")


if __name__ == "__main__":
    main()