#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案：Tree Shaking 实现

这是 example-02-tree-shaking.py 的完整解决方案，
包含了更精确的代码使用分析和死代码移除逻辑。
"""

import ast
import json
from typing import Set, List, Dict, Optional


class AdvancedTreeShaker:
    """高级 Tree Shaking 实现"""

    def __init__(self):
        self.exported_symbols: Set[str] = set()
        self.used_symbols: Set[str] = set()
        self.symbol_definitions: Dict[str, ast.AST] = {}
        self.import_mappings: Dict[str, str] = {}

    def analyze_module(self, code: str) -> Dict[str, any]:
        """分析模块并执行 tree shaking"""
        try:
            tree = ast.parse(code)

            # 提取导出符号
            self._extract_exports(tree)

            # 提取导入映射
            self._extract_imports(tree)

            # 分析使用情况
            self._analyze_usage(tree)

            # 执行优化
            optimized_code = self._generate_optimized_code(tree)

            unused_exports = self.exported_symbols - self.used_symbols

            return {
                'exported_symbols': list(self.exported_symbols),
                'used_symbols': list(self.used_symbols),
                'unused_exports': list(unused_exports),
                'optimized_code': optimized_code,
                'bytes_saved': len(code) - len(optimized_code)
            }

        except SyntaxError as e:
            return {'error': f'语法错误: {e}'}

    def _extract_exports(self, tree: ast.AST):
        """提取所有导出的符号"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.exported_symbols.add(node.name)
                self.symbol_definitions[node.name] = node
            elif isinstance(node, ast.ClassDef):
                self.exported_symbols.add(node.name)
                self.symbol_definitions[node.name] = node
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.exported_symbols.add(target.id)
                        self.symbol_definitions[target.id] = node

    def _extract_imports(self, tree: ast.AST):
        """提取导入语句的映射"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_name = alias.asname if alias.asname else alias.name
                    module_name = node.module if node.module else ''
                    self.import_mappings[imported_name] = f"{module_name}.{alias.name}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported_name = alias.asname if alias.asname else alias.name
                    self.import_mappings[imported_name] = alias.name

    def _analyze_usage(self, tree: ast.AST):
        """分析符号使用情况"""
        class UsageVisitor(ast.NodeVisitor):
            def __init__(self, used_set, import_mappings):
                self.used_set = used_set
                self.import_mappings = import_mappings

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    name = node.id
                    # 检查是否是导入的符号
                    if name in self.import_mappings:
                        # 导入的符号不算作当前模块的导出使用
                        pass
                    else:
                        self.used_set.add(name)

        visitor = UsageVisitor(self.used_symbols, self.import_mappings)
        visitor.visit(tree)

    def _generate_optimized_code(self, tree: ast.AST) -> str:
        """生成优化后的代码"""
        unused_nodes = []

        # 收集未使用的节点
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if node.name not in self.used_symbols and node.name in self.exported_symbols:
                    unused_nodes.append(node)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if (target.id not in self.used_symbols and
                            target.id in self.exported_symbols):
                            unused_nodes.append(node)

        # 简单的代码生成（实际工具会更复杂）
        lines = []
        current_line = 1

        for node in ast.iter_child_nodes(tree):
            if node not in unused_nodes:
                # 这里简化处理，实际需要更精确的源码映射
                lines.append(ast.unparse(node) if hasattr(ast, 'unparse') else '# Optimized code')

        return '\n'.join(lines) if lines else '# All code was shaken away!'


def solution_main():
    """解决方案主函数"""
    code = '''
def used_function():
    return "This is used"

def unused_function():
    return "This is unused"

class UsedClass:
    def method(self):
        return "Used method"

class UnusedClass:
    def method(self):
        return "Unused method"

CONSTANT_USED = 42
CONSTANT_UNUSED = 100

result = used_function()
obj = UsedClass()
print(result, obj.method(), CONSTANT_USED)
'''

    shaker = AdvancedTreeShaker()
    result = shaker.analyze_module(code)

    if 'error' in result:
        print(f"错误: {result['error']}")
        return

    print("Tree Shaking 分析结果:")
    print(f"导出符号: {result['exported_symbols']}")
    print(f"使用符号: {result['used_symbols']}")
    print(f"未使用导出: {result['unused_exports']}")
    print(f"节省字节数: {result['bytes_saved']}")
    print("\n优化后代码:")
    print(result['optimized_code'])


if __name__ == "__main__":
    solution_main()