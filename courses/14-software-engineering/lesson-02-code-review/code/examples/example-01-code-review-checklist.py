#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码审查检查清单模拟器

这个脚本模拟自动化代码审查检查，包括：
- 代码复杂度分析
- 命名规范检查
- 文档字符串验证
"""

import ast
import sys
from typing import List, Dict, Any


class CodeReviewChecker:
    """代码审查检查器类"""

    def __init__(self):
        """初始化检查器"""
        self.issues = []
        self.max_complexity = 10
        self.required_docstring_ratio = 0.8

    def check_naming_convention(self, node: ast.AST) -> None:
        """检查命名规范

        Args:
            node: AST节点
        """
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.islower() and '_' in node.name:
                self.issues.append(f"函数命名不规范: {node.name} - 应使用snake_case")

        elif isinstance(node, ast.ClassDef):
            if not node.name[0].isupper():
                self.issues.append(f"类命名不规范: {node.name} - 应使用PascalCase")

        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if not node.id.islower() and '_' in node.id:
                self.issues.append(f"变量命名不规范: {node.id} - 应使用snake_case")

    def calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """计算圈复杂度

        Args:
            node: AST节点

        Returns:
            复杂度数值
        """
        complexity = 1

        # 统计控制流语句
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

        # 重置问题列表
        self.issues = []

        # 检查命名规范
        for node in ast.walk(tree):
            self.check_naming_convention(node)

        # 检查复杂度
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self.calculate_cyclomatic_complexity(node)
                if complexity > self.max_complexity:
                    self.issues.append(f"函数 {node.name} 复杂度过高: {complexity} (最大允许: {self.max_complexity})")

        # 检查文档字符串
        docstring_ratio = self.check_docstrings(tree)
        if docstring_ratio < self.required_docstring_ratio:
            self.issues.append(f"文档字符串覆盖率不足: {docstring_ratio:.2%} (要求: {self.required_docstring_ratio:.2%})")

        return {
            "issues": self.issues,
            "total_issues": len(self.issues),
            "docstring_coverage": docstring_ratio
        }


def main():
    """主函数 - 演示代码审查检查清单"""
    print("=== 代码审查检查清单模拟器 ===\n")

    # 示例代码
    sample_code = '''
def calculate_user_score(user_data):
    """计算用户评分"""
    score = 0
    if user_data.get("active", False):
        score += 10
    if user_data.get("premium", False):
        score += 20

    for activity in user_data.get("activities", []):
        if activity["type"] == "login":
            score += 1
        elif activity["type"] == "purchase":
            score += 5
        elif activity["type"] == "review":
            score += 3

    return score

class userDataProcessor:
    def process(self, data):
        UserScore = calculate_user_score(data)
        return {"score": UserScore}
'''

    checker = CodeReviewChecker()
    result = checker.review_code(sample_code)

    print("审查结果:")
    if result.get("error"):
        print(f"❌ {result['error']}")
    elif result["total_issues"] == 0:
        print("✅ 代码通过所有检查!")
    else:
        print(f"⚠️  发现 {result['total_issues']} 个问题:")
        for issue in result["issues"]:
            print(f"  • {issue}")
        print(f"📊 文档字符串覆盖率: {result['docstring_coverage']:.2%}")


if __name__ == "__main__":
    main()