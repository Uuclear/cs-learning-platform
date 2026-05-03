#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：Bundle分析器

这个脚本解析简单的模块依赖树，计算总bundle大小，
并识别重复的依赖项（可以帮助进行代码分割优化）。
"""

import json
from collections import defaultdict, deque


class BundleAnalyzer:
    """Bundle分析器类"""

    def __init__(self):
        """初始化分析器"""
        self.modules = {}  # {module_id: {'size': size, 'dependencies': [deps]}}
        self.dependency_graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)

    def add_module(self, module_id, size, dependencies=None):
        """
        添加模块到分析器

        :param module_id: 模块ID
        :param size: 模块大小（字节）
        :param dependencies: 依赖列表
        """
        if dependencies is None:
            dependencies = []

        self.modules[module_id] = {
            'size': size,
            'dependencies': dependencies.copy()
        }

        # 构建依赖图
        for dep in dependencies:
            self.dependency_graph[module_id].append(dep)
            self.reverse_graph[dep].append(module_id)

    def calculate_total_size(self):
        """
        计算总bundle大小（包含重复依赖）

        :return: 总大小（字节）
        """
        return sum(module['size'] for module in self.modules.values())

    def find_duplicate_dependencies(self):
        """
        找出被多个模块依赖的重复依赖项

        :return: 重复依赖字典 {dependency: [dependents]}
        """
        duplicates = {}
        for dep, dependents in self.reverse_graph.items():
            if len(dependents) > 1 and dep in self.modules:
                duplicates[dep] = dependents.copy()
        return duplicates

    def calculate_unique_size(self):
        """
        计算去重后的实际bundle大小

        :return: 唯一大小（字节）
        """
        return sum(module['size'] for module in self.modules.values())

    def find_entry_points(self):
        """
        找出入口点（没有被其他模块依赖的模块）

        :return: 入口点列表
        """
        all_modules = set(self.modules.keys())
        dependent_modules = set(self.reverse_graph.keys())
        entry_points = all_modules - dependent_modules
        return list(entry_points)

    def calculate_module_impact(self, module_id):
        """
        计算模块的影响范围（直接影响的模块数量）

        :param module_id: 模块ID
        :return: 影响的模块数量
        """
        if module_id not in self.modules:
            return 0

        visited = set()
        queue = deque([module_id])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            # 添加所有依赖此模块的模块
            for dependent in self.reverse_graph.get(current, []):
                if dependent not in visited:
                    queue.append(dependent)

        return len(visited) - 1  # 减去自身

    def suggest_code_splitting(self, min_impact=2, min_size=10000):
        """
        建议代码分割点

        :param min_impact: 最小影响模块数
        :param min_size: 最小模块大小（字节）
        :return: 分割建议列表
        """
        suggestions = []
        duplicates = self.find_duplicate_dependencies()

        for module_id, module_info in self.modules.items():
            impact = self.calculate_module_impact(module_id)
            size = module_info['size']

            # 大型且被多个模块使用的模块适合分割
            if impact >= min_impact and size >= min_size:
                suggestions.append({
                    'module': module_id,
                    'size': size,
                    'impact': impact,
                    'reason': f'大型模块({size}字节)，影响{impact}个模块'
                })

            # 被重复使用的依赖也适合提取到公共chunk
            if module_id in duplicates and len(duplicates[module_id]) >= min_impact:
                suggestions.append({
                    'module': module_id,
                    'size': size,
                    'impact': len(duplicates[module_id]),
                    'reason': f'被{len(duplicates[module_id])}个模块重复使用'
                })

        # 按影响和大小排序
        suggestions.sort(key=lambda x: (x['impact'], x['size']), reverse=True)
        return suggestions

    def generate_report(self):
        """
        生成完整的bundle分析报告

        :return: 报告字符串
        """
        total_size = self.calculate_total_size()
        unique_size = self.calculate_unique_size()
        duplicates = self.find_duplicate_dependencies()
        entry_points = self.find_entry_points()
        suggestions = self.suggest_code_splitting()

        report = []
        report.append("=== Bundle分析报告 ===\n")

        report.append(f"总模块数: {len(self.modules)}")
        report.append(f"总bundle大小: {total_size:,} 字节 ({total_size / 1024:.1f} KB)")
        report.append(f"唯一内容大小: {unique_size:,} 字节 ({unique_size / 1024:.1f} KB)")
        report.append(f"重复内容节省: {total_size - unique_size:,} 字节 ({(total_size - unique_size) / 1024:.1f} KB)\n")

        report.append(f"入口点数量: {len(entry_points)}")
        if entry_points:
            report.append(f"入口点: {', '.join(entry_points[:5])}")
            if len(entry_points) > 5:
                report.append(f"... 还有 {len(entry_points) - 5} 个入口点\n")

        report.append(f"\n重复依赖项: {len(duplicates)}")
        for dep, dependents in list(duplicates.items())[:5]:
            report.append(f"  {dep}: 被 {len(dependents)} 个模块使用 ({', '.join(dependents[:3])})")
        if len(duplicates) > 5:
            report.append(f"  ... 还有 {len(duplicates) - 5} 个重复依赖项\n")

        report.append(f"\n代码分割建议: {len(suggestions)}")
        for i, suggestion in enumerate(suggestions[:3], 1):
            report.append(f"  {i}. {suggestion['module']}")
            report.append(f"     大小: {suggestion['size']:,} 字节")
            report.append(f"     影响: {suggestion['impact']} 个模块")
            report.append(f"     原因: {suggestion['reason']}")
        if len(suggestions) > 3:
            report.append(f"  ... 还有 {len(suggestions) - 3} 个建议\n")

        return "\n".join(report)


def create_sample_bundle():
    """创建示例bundle数据"""
    analyzer = BundleAnalyzer()

    # 添加模块（模拟真实应用的模块结构）
    modules_data = {
        'main.js': {'size': 50000, 'dependencies': ['react', 'lodash', 'utils', 'components']},
        'admin.js': {'size': 35000, 'dependencies': ['react', 'lodash', 'utils', 'admin-components']},
        'user-profile.js': {'size': 25000, 'dependencies': ['react', 'utils', 'profile-components']},
        'react': {'size': 120000, 'dependencies': []},
        'lodash': {'size': 80000, 'dependencies': []},
        'utils': {'size': 15000, 'dependencies': []},
        'components': {'size': 45000, 'dependencies': ['utils']},
        'admin-components': {'size': 30000, 'dependencies': ['utils']},
        'profile-components': {'size': 20000, 'dependencies': ['utils']},
        'analytics.js': {'size': 10000, 'dependencies': ['utils']}
    }

    for module_id, data in modules_data.items():
        analyzer.add_module(module_id, data['size'], data['dependencies'])

    return analyzer


def main():
    """主函数：运行bundle分析"""
    print("=== JavaScript Bundle分析器 ===\n")

    # 创建示例bundle
    analyzer = create_sample_bundle()

    # 生成并显示报告
    report = analyzer.generate_report()
    print(report)

    print("=== 优化建议 ===")
    print("1. 将React和Lodash提取到vendor chunk")
    print("2. 将Utils模块提取到common chunk")
    print("3. 考虑按路由进行代码分割")
    print("4. 使用动态导入减少初始bundle大小")


if __name__ == "__main__":
    main()