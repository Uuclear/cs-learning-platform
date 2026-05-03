#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 Tree Shaking（死代码消除）

这个脚本演示了前端构建工具中的 Tree Shaking 优化技术：
1. 分析代码中的实际使用情况
2. 识别未使用的导出函数/变量
3. 移除死代码以减小包体积

Tree Shaking 是现代打包工具（如 Webpack、Rollup）的重要优化功能。
"""

import ast
import json
from typing import Set, List, Dict


class TreeShaker:
    """Tree Shaking 模拟器"""

    def __init__(self):
        self.used_identifiers: Set[str] = set()
        self.exported_identifiers: Set[str] = set()
        self.unused_identifiers: Set[str] = set()

    def analyze_code(self, code: str) -> Dict[str, any]:
        """分析代码并执行 tree shaking"""
        try:
            tree = ast.parse(code)

            # 提取所有导出的标识符（简化版）
            self._extract_exports(tree)

            # 分析实际使用的标识符
            self._analyze_usage(tree)

            # 找出未使用的标识符
            self.unused_identifiers = self.exported_identifiers - self.used_identifiers

            return {
                'exported': list(self.exported_identifiers),
                'used': list(self.used_identifiers),
                'unused': list(self.unused_identifiers),
                'shaken_code': self._remove_unused_code(code)
            }
        except SyntaxError as e:
            return {'error': f'语法错误: {e}'}

    def _extract_exports(self, tree: ast.AST):
        """提取模块中导出的标识符（模拟 ES6 exports）"""
        # 在真实场景中，这会解析 export 语句
        # 这里我们假设所有顶层函数都是导出的
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.exported_identifiers.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.exported_identifiers.add(target.id)

    def _analyze_usage(self, tree: ast.AST):
        """分析代码中实际使用的标识符"""
        class UsageVisitor(ast.NodeVisitor):
            def __init__(self, used_set):
                self.used_set = used_set

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):  # 只记录被读取的标识符
                    self.used_set.add(node.id)

        visitor = UsageVisitor(self.used_identifiers)
        visitor.visit(tree)

    def _remove_unused_code(self, code: str) -> str:
        """移除未使用的代码（简化版）"""
        lines = code.split('\n')
        filtered_lines = []

        skip_next_function = False

        for line in lines:
            stripped = line.strip()

            # 跳过未使用的函数定义
            if stripped.startswith('def ') and any(unused in stripped for unused in self.unused_identifiers):
                skip_next_function = True
                continue

            # 跳过函数体（简单处理）
            if skip_next_function:
                if stripped == '':
                    skip_next_function = False
                    continue
                elif not stripped.startswith('    '):  # 不是以缩进开头，说明函数结束
                    skip_next_function = False

            if not skip_next_function:
                filtered_lines.append(line)

        return '\n'.join(filtered_lines)


def main():
    """主函数：演示 Tree Shaking 过程"""
    print("=== Tree Shaking (死代码消除) 模拟演示 ===\n")

    # 模拟的 JavaScript/TypeScript 代码（用 Python 语法表示以便 AST 解析）
    sample_code = '''
# 导出的实用函数
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

def multiply(x, y):
    return x * y

def unused_helper():
    """这个辅助函数从未被使用"""
    return "never called"

def format_date(date_str):
    """格式化日期"""
    return date_str.replace("-", "/")

# 全局变量（导出）
DEBUG_MODE = True
MAX_RETRY = 3

# 主要逻辑 - 只使用部分导出的函数
result = add(10, 20)
message = greet("开发者")
print(f"{message} 计算结果: {result}")

# 注意：multiply, unused_helper, format_date, DEBUG_MODE, MAX_RETRY 都未被使用
'''

    print("原始代码:")
    print(sample_code)
    print("\n" + "="*60 + "\n")

    # 执行 tree shaking 分析
    shaker = TreeShaker()
    result = shaker.analyze_code(sample_code)

    if 'error' in result:
        print(f"分析失败: {result['error']}")
        return

    print("分析结果:")
    print(f"✓ 导出的标识符: {result['exported']}")
    print(f"✓ 实际使用的标识符: {result['used']}")
    print(f"✗ 未使用的标识符: {result['unused']}")

    print(f"\n优化后节省的标识符数量: {len(result['unused'])}")
    print(f"Tree Shaking 效果: 移除了 {len(result['unused'])} 个未使用的导出项\n")

    print("优化后的代码:")
    print(result['shaken_code'])


if __name__ == "__main__":
    main()