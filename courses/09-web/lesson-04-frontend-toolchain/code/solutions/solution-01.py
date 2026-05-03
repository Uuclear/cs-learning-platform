#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案：模块打包器实现

这是 example-01-bundler-simulation.py 的完整解决方案，
包含了更健壮的模块解析和依赖处理逻辑。
"""

import os
import json
from typing import Dict, List, Set, Optional


class AdvancedModuleBundler:
    """高级模块打包器，支持循环依赖检测和更准确的导入解析"""

    def __init__(self):
        self.modules: Dict[str, str] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.resolved_modules: Set[str] = set()
        self.dependency_graph: Dict[str, Set[str]] = {}

    def add_module(self, file_path: str, content: str):
        """添加模块到打包器"""
        self.modules[file_path] = content
        self.dependencies[file_path] = self._parse_imports_advanced(content)
        self.dependency_graph[file_path] = set(self.dependencies[file_path])

    def _parse_imports_advanced(self, content: str) -> List[str]:
        """高级导入解析，支持多种 import 语法"""
        imports = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('#'):
                continue

            # 支持多种 import 语法
            if line.startswith('import '):
                if ' from ' in line:
                    # import {x} from 'module'
                    parts = line.split(' from ', 1)
                    if len(parts) == 2:
                        module_spec = parts[1].strip().strip("';\"")
                        resolved_path = self._resolve_module_path(module_spec)
                        if resolved_path:
                            imports.append(resolved_path)
                elif line.endswith(';'):
                    # import 'module'
                    module_spec = line[7:-1].strip().strip("';\"")
                    resolved_path = self._resolve_module_path(module_spec)
                    if resolved_path:
                        imports.append(resolved_path)

            elif line.startswith('const ') and ('require(' in line or 'import(' in line):
                # 动态导入：const x = require('module')
                # 简化处理
                pass

        return imports

    def _resolve_module_path(self, module_spec: str) -> Optional[str]:
        """解析模块路径"""
        if module_spec.startswith('.'):
            # 相对路径
            if module_spec.endswith('.js'):
                return module_spec
            else:
                return f"{module_spec}.js"
        else:
            # 绝对路径或 node_modules（简化处理）
            return f"./node_modules/{module_spec}.js"

    def detect_cycles(self) -> List[List[str]]:
        """检测循环依赖"""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node):
            if node not in self.dependency_graph:
                return
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.dependency_graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # 找到循环
                    cycle = list(rec_stack) + [neighbor]
                    cycles.append(cycle)
                    return True

            rec_stack.remove(node)
            return False

        for node in self.dependency_graph:
            if node not in visited:
                dfs(node)

        return cycles

    def bundle(self, entry_point: str) -> str:
        """打包入口模块及其所有依赖"""
        if entry_point not in self.modules:
            raise FileNotFoundError(f"入口模块未找到: {entry_point}")

        self.resolved_modules.clear()
        bundled_code = "// === 前端工具链课程 - 模块打包演示 ===\n"
        bundled_code += self._bundle_recursive(entry_point)
        return bundled_code

    def _bundle_recursive(self, module_path: str, depth: int = 0) -> str:
        """递归打包模块"""
        if module_path in self.resolved_modules:
            return f"\n// 模块已包含: {module_path}\n"

        if module_path not in self.modules:
            return f"\n// 警告: 未找到模块 {module_path}\n"

        self.resolved_modules.add(module_path)
        indent = "  " * depth
        content = self.modules[module_path]

        result = f"\n{indent}// === 开始模块: {module_path} ===\n"
        result += content
        result += f"\n{indent}// === 结束模块: {module_path} ===\n"

        # 递归处理依赖
        for dep in self.dependencies.get(module_path, []):
            result += self._bundle_recursive(dep, depth + 1)

        return result


def solution_main():
    """解决方案主函数"""
    bundler = AdvancedModuleBundler()

    # 测试数据
    test_modules = {
        './app.js': "import { init } from './main.js';\ninit();",
        './main.js': "import { utils } from './utils.js';\nexport function init() { utils.log('started'); }",
        './utils.js': "export const utils = { log: (msg) => console.log(msg) };"
    }

    for path, content in test_modules.items():
        bundler.add_module(path, content)

    result = bundler.bundle('./app.js')
    print("打包结果:")
    print(result)

    cycles = bundler.detect_cycles()
    if cycles:
        print(f"\n发现循环依赖: {cycles}")
    else:
        print("\n✓ 无循环依赖")


if __name__ == "__main__":
    solution_main()