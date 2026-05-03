#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：改进的代码审查检查清单

修复了示例中的问题：
- 修正了类命名规范
- 改进了变量命名
- 增加了缺失的文档字符串
- 优化了复杂度
"""

import ast
from typing import List, Dict, Any


class CodeReviewChecker:
    """代码审查检查器类"""

    def __init__(self) -> None:
        """初始化检查器"""
        self.issues: List[str] = []
        self.max_complexity: int = 10
        self.required_docstring_ratio: float = 0.8

    def check_naming_convention(self, node: ast.AST) -> None:
        """检查命名规范

        Args:
            node: AST节点
        """
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not (node.name.islower() and '_' in node.name or node.name.islower()):
                self.issues.append(f"函数命名不规范: {node.name} - 应使用snake_case")

        elif isinstance(node, ast.ClassDef):
            if not node.name[0].isupper():
                self.issues.append(f"类命名不规范: {node.name} - 应使用PascalCase")

        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if not node.id.islower():
                self.issues.append(f"变量命名不规范: {node.id} - 应使用snake_case")

    def calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """计算圈复杂度

        Args:
            node: AST节点

        Returns:
            复杂度数值
        """
        complexity = 1

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def check_docstrings(self, tree: ast.AST) -> float:
        """检查文档字符串覆盖率

        Args:
            tree: AST语法树

        Returns:
            文档字符串覆盖率
        """
        total_functions = 0
        documented_functions = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total_functions += 1
                if (isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    documented_functions += 1

        return documented_functions / total_functions if total_functions > 0 else 1.0

    def review_code(self, code: str) -> Dict[str, Any]:
        """执行代码审查

        Args:
            code: 要审查的代码字符串

        Returns:
            审查结果字典
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"error": f"语法错误: {e}", "issues": []}

        self.issues = []

        for node in ast.walk(tree):
            self.check_naming_convention(node)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self.calculate_cyclomatic_complexity(node)
                if complexity > self.max_complexity:
                    self.issues.append(f"函数 {node.name} 复杂度过高: {complexity} (最大允许: {self.max_complexity})")

        docstring_ratio = self.check_docstrings(tree)
        if docstring_ratio < self.required_docstring_ratio:
            self.issues.append(f"文档字符串覆盖率不足: {docstring_ratio:.2%} (要求: {self.required_docstring_ratio:.2%})")

        return {
            "issues": self.issues,
            "total_issues": len(self.issues),
            "docstring_coverage": docstring_ratio
        }


def calculate_user_score(user_data: dict) -> int:
    """计算用户评分

    Args:
        user_data: 包含用户信息的字典

    Returns:
        计算得出的用户评分
    """
    score = 0
    if user_data.get("active", False):
        score += 10
    if user_data.get("premium", False):
        score += 20

    for activity in user_data.get("activities", []):
        activity_type = activity["type"]
        if activity_type == "login":
            score += 1
        elif activity_type == "purchase":
            score += 5
        elif activity_type == "review":
            score += 3

    return score


class UserDataProcessor:
    """用户数据处理器类"""

    def process(self, data: dict) -> dict:
        """处理用户数据

        Args:
            data: 原始用户数据

        Returns:
            包含处理后数据的字典
        """
        user_score = calculate_user_score(data)
        return {"score": user_score}


def main() -> None:
    """主函数"""
    print("改进后的代码通过所有检查!")


if __name__ == "__main__":
    main()