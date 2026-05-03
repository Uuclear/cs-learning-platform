#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：改进的代码异味检测器
添加了更多检测规则和更好的错误处理
"""

import ast
import sys
from typing import List, Dict, Any


class EnhancedCodeSmellDetector(ast.NodeVisitor):
    """增强的代码异味检测器"""

    def __init__(self):
        self.issues = []
        self.current_function = None
        self.function_stack = []

    def visit_FunctionDef(self, node):
        """访问函数定义节点"""
        self.function_stack.append(node.name)
        self.current_function = node.name

        # 检测过长函数（超过40行更严格）
        function_lines = node.end_lineno - node.lineno + 1
        if function_lines > 40:
            self.issues.append({
                'type': 'long_function',
                'message': f'函数 {node.name} 过长 ({function_lines} 行)，建议拆分为更小的函数',
                'line': node.lineno,
                'severity': 'high' if function_lines > 60 else 'medium'
            })

        # 检测参数过多（超过4个更严格）
        total_args = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            total_args += 1
        if node.args.kwarg:
            total_args += 1

        if total_args > 4:
            self.issues.append({
                'type': 'too_many_parameters',
                'message': f'函数 {node.name} 参数过多 ({total_args} 个)，考虑使用参数对象',
                'line': node.lineno,
                'severity': 'high' if total_args > 6 else 'medium'
            })

        # 检测函数中变量过多
        var_count = self._count_local_variables(node)
        if var_count > 10:
            self.issues.append({
                'type': 'too_many_variables',
                'message': f'函数 {node.name} 局部变量过多 ({var_count} 个)，建议提取方法',
                'line': node.lineno,
                'severity': 'medium'
            })

        self.generic_visit(node)
        self.function_stack.pop()
        self.current_function = self.function_stack[-1] if self.function_stack else None

    def _count_local_variables(self, func_node):
        """统计函数中的局部变量数量"""
        var_names = set()
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_names.add(target.id)
        return len(var_names)

    def visit_ClassDef(self, node):
        """访问类定义节点"""
        # 检测大类（方法过多）
        method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
        if method_count > 15:
            self.issues.append({
                'type': 'large_class',
                'message': f'类 {node.name} 方法过多 ({method_count} 个)，考虑拆分类',
                'line': node.lineno,
                'severity': 'high' if method_count > 20 else 'medium'
            })
        self.generic_visit(node)

    def visit_If(self, node):
        """访问if语句，检测嵌套和复杂条件"""
        self._check_nesting_depth(node, 'if')
        self._check_complex_condition(node)
        self.generic_visit(node)

    def _check_complex_condition(self, node):
        """检查复杂条件表达式"""
        if hasattr(node, 'test'):
            condition_complexity = self._calculate_condition_complexity(node.test)
            if condition_complexity > 3:
                self.issues.append({
                    'type': 'complex_condition',
                    'message': f'复杂条件表达式 (复杂度 {condition_complexity})，建议提取为命名变量',
                    'line': node.lineno,
                    'severity': 'medium'
                })

    def _calculate_condition_complexity(self, node):
        """计算条件表达式的复杂度"""
        if isinstance(node, (ast.BoolOp, ast.Compare)):
            complexity = 1
            if isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
                for value in node.values:
                    complexity += self._calculate_condition_complexity(value)
            elif isinstance(node, ast.Compare):
                complexity += len(node.ops)
            return complexity
        return 0

    def visit_For(self, node):
        """访问for循环"""
        self._check_nesting_depth(node, 'for')
        self.generic_visit(node)

    def visit_While(self, node):
        """访问while循环"""
        self._check_nesting_depth(node, 'while')
        self.generic_visit(node)

    def _check_nesting_depth(self, node, statement_type):
        """检查嵌套深度"""
        depth = self._calculate_nesting_depth(node)
        if depth > 3:  # 更严格的阈值
            self.issues.append({
                'type': 'deep_nesting',
                'message': f'{statement_type} 语句嵌套过深 ({depth} 层)，严重影响可读性',
                'line': node.lineno,
                'severity': 'high' if depth > 5 else 'medium'
            })

    def _calculate_nesting_depth(self, node):
        """计算嵌套深度"""
        depth = 0
        current = getattr(node, 'parent', None)
        while current:
            if isinstance(current, (ast.If, ast.For, ast.While, ast.Try)):
                depth += 1
            current = getattr(current, 'parent', None)
        return depth


def add_parent_pointers(node, parent=None):
    """为AST节点添加父指针"""
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        add_parent_pointers(child, node)


def analyze_file(file_path: str) -> List[Dict[str, Any]]:
    """分析文件并返回所有问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        tree = ast.parse(source_code, filename=file_path)
        add_parent_pointers(tree)

        detector = EnhancedCodeSmellDetector()
        detector.visit(tree)

        return detector.issues

    except SyntaxError as e:
        return [{
            'type': 'syntax_error',
            'message': f'语法错误: {e}',
            'line': e.lineno if e.lineno else 1,
            'severity': 'critical'
        }]
    except Exception as e:
        return [{
            'type': 'analysis_error',
            'message': f'分析错误: {e}',
            'line': 1,
            'severity': 'error'
        }]


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python solution-01.py <python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    issues = analyze_file(file_path)

    if issues:
        print(f"在文件 {file_path} 中发现 {len(issues)} 个问题:")
        severity_order = {'critical': 0, 'error': 1, 'high': 2, 'medium': 3, 'low': 4}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.get('severity', 'low'), 999))

        for issue in sorted_issues:
            severity = issue.get('severity', 'info')
            print(f"  [{severity.upper()}] 行 {issue['line']}: {issue['message']}")
    else:
        print(f"文件 {file_path} 分析完成，未发现问题")


if __name__ == "__main__":
    main()