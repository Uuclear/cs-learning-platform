#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：完整的Bundle分析器

这个解决方案提供了更详细的bundle分析，
包括依赖图可视化和优化建议。
"""

import json
from collections import defaultdict, deque


class AdvancedBundleAnalyzer:
    """高级Bundle分析器"""

    def __init__(self):
        self.modules = {}
        self.dependency_graph = defaultdict(set)
        self.reverse_graph = defaultdict(set)

    def load_from_json(self, bundle_data):
        """从JSON数据加载bundle信息"""
        for module_id, module_info in bundle_data.items():
            self.add_module(
                module_id,
                module_info['size'],
                module_info.get('dependencies', [])
            )

    def add_module(self, module_id, size, dependencies):
        """添加模块"""
        self.modules[module_id] = {'size': size, 'dependencies': dependencies}

        for dep in dependencies:
            self.dependency_graph[module_id].add(dep)
            self.reverse_graph[dep].add(module_id)

    def find_cycles(self):
        """检测依赖循环"""
        visited = set()
        recursion_stack = set()
        cycles = []

        def dfs(node, path):
            if node in recursion_stack:
                # 找到循环
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return

            if node in visited:
                return

            visited.add(node)
            recursion_stack.add(node)
            path.append(node)

            for neighbor in self.dependency_graph[node]:
                dfs(neighbor, path)

            path.pop()
            recursion_stack.remove(node)

        for node in self.modules:
            if node not in visited:
                dfs(node, [])

        return cycles

    def calculate_critical_path(self):
        """计算关键路径（影响初始加载的最长路径）"""
        entry_points = self.find_entry_points()
        if not entry_points:
            return []

        max_path = []
        max_size = 0

        def dfs(node, current_path, current_size):
            nonlocal max_path, max_size

            current_path.append(node)
            current_size += self.modules[node]['size']

            if current_size > max_size:
                max_size = current_size
                max_path = current_path.copy()

            for dep in self.dependency_graph[node]:
                dfs(dep, current_path, current_size)

            current_path.pop()

        for entry in entry_points:
            dfs(entry, [], 0)

        return max_path, max_size

    def find_entry_points(self):
        """找入口点"""
        all_modules = set(self.modules.keys())
        dependent_modules = set(self.reverse_graph.keys())
        return list(all_modules - dependent_modules)

    def generate_optimization_report(self):
        """生成优化报告"""
        cycles = self.find_cycles()
        critical_path, critical_size = self.calculate_critical_path()
        duplicates = self.find_duplicate_dependencies()

        report = {
            'total_size': sum(m['size'] for m in self.modules.values()),
            'module_count': len(self.modules),
            'cycles': cycles,
            'critical_path': critical_path,
            'critical_size': critical_size,
            'duplicates': duplicates,
            'optimization_suggestions': self._generate_suggestions()
        }

        return report

    def find_duplicate_dependencies(self):
        """找重复依赖"""
        duplicates = {}
        for dep, dependents in self.reverse_graph.items():
            if len(dependents) > 1 and dep in self.modules:
                duplicates[dep] = list(dependents)
        return duplicates

    def _generate_suggestions(self):
        """生成优化建议"""
        suggestions = []

        # 大型模块分割
        large_modules = [(mid, m['size']) for mid, m in self.modules.items() if m['size'] > 50000]
        large_modules.sort(key=lambda x: x[1], reverse=True)

        for module_id, size in large_modules[:3]:
            suggestions.append({
                'type': 'split_large_module',
                'target': module_id,
                'size': size,
                'recommendation': f'考虑将{module_id}分割成更小的chunk'
            })

        # 公共依赖提取
        duplicates = self.find_duplicate_dependencies()
        common_deps = [(dep, len(deps)) for dep, deps in duplicates.items() if len(deps) >= 2]
        common_deps.sort(key=lambda x: x[1], reverse=True)

        for dep, usage_count in common_deps[:3]:
            suggestions.append({
                'type': 'extract_common_dependency',
                'target': dep,
                'usage_count': usage_count,
                'recommendation': f'将{dep}提取到公共chunk，被{usage_count}个模块使用'
            })

        return suggestions


if __name__ == "__main__":
    # 示例bundle数据
    sample_bundle = {
        "main.js": {"size": 50000, "dependencies": ["react", "lodash", "utils"]},
        "admin.js": {"size": 35000, "dependencies": ["react", "lodash", "utils"]},
        "react": {"size": 120000, "dependencies": []},
        "lodash": {"size": 80000, "dependencies": []},
        "utils": {"size": 15000, "dependencies": []}
    }

    analyzer = AdvancedBundleAnalyzer()
    analyzer.load_from_json(sample_bundle)

    report = analyzer.generate_optimization_report()
    print("=== 优化报告 ===")
    print(f"总大小: {report['total_size']:,} 字节")
    print(f"模块数: {report['module_count']}")
    print(f"关键路径大小: {report['critical_size']:,} 字节")

    print("\n优化建议:")
    for suggestion in report['optimization_suggestions']:
        print(f"- {suggestion['recommendation']}")