#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：代码异味检测器
检测Python代码中的常见代码异味（code smells）
包括：过长函数、参数过多、嵌套过深等问题
"""

import ast
import sys
from typing import List, Dict, Any


class CodeSmellDetector(ast.NodeVisitor):
    """代码异味检测器类"""

    def __init__(self):
        self.issues = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        """访问函数定义节点"""
        self.current_function = node.name

        # 检测过长函数（超过50行）
        function_lines = node.end_lineno - node.lineno + 1
        if function_lines > 50:
            self.issues.append({
                'type': 'long_function',
                'message': f'函数 {node.name} 过长 ({function_lines} 行)，建议拆分',
                'line': node.lineno
            })

        # 检测参数过多（超过5个）
        arg_count = len(node.args.args)
        if arg_count > 5:
            self.issues.append({
                'type': 'too_many_parameters',
                'message': f'函数 {node.name} 参数过多 ({arg_count} 个)，建议重构',
                'line': node.lineno
            })

        # 继续遍历函数体
        self.generic_visit(node)
        self.current_function = None

    def visit_If(self, node):
        """访问if语句节点，检测嵌套过深"""
        self._check_nesting_depth(node, 'if')
        self.generic_visit(node)

    def visit_For(self, node):
        """访问for循环节点，检测嵌套过深"""
        self._check_nesting_depth(node, 'for')
        self.generic_visit(node)

    def visit_While(self, node):
        """访问while循环节点，检测嵌套过深"""
        self._check_nesting_depth(node, 'while')
        self.generic_visit(node)

    def _check_nesting_depth(self, node, statement_type):
        """检查嵌套深度"""
        depth = self._calculate_nesting_depth(node)
        if depth > 4:  # 超过4层嵌套
            self.issues.append({
                'type': 'deep_nesting',
                'message': f'{statement_type} 语句嵌套过深 ({depth} 层)，建议提取方法',
                'line': node.lineno
            })

    def _calculate_nesting_depth(self, node):
        """计算当前节点的嵌套深度"""
        depth = 0
        current = node
        while hasattr(current, 'parent') and current.parent:
            if isinstance(current.parent, (ast.If, ast.For, ast.While)):
                depth += 1
            current = current.parent
        return depth


def add_parent_pointers(node, parent=None):
    """为AST节点添加父指针，便于计算嵌套深度"""
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        add_parent_pointers(child, node)


def analyze_file(file_path: str) -> List[Dict[str, Any]]:
    """分析指定文件的代码异味"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        tree = ast.parse(source_code, filename=file_path)
        add_parent_pointers(tree)

        detector = CodeSmellDetector()
        detector.visit(tree)

        return detector.issues

    except Exception as e:
        print(f"分析文件 {file_path} 时出错: {e}")
        return []


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python example-01-code-smell-detector.py <python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    issues = analyze_file(file_path)

    if issues:
        print(f"在文件 {file_path} 中发现 {len(issues)} 个代码异味:")
        for issue in issues:
            print(f"  行 {issue['line']}: {issue['message']}")
    else:
        print(f"文件 {file_path} 中未发现明显的代码异味")


if __name__ == "__main__":
    main()