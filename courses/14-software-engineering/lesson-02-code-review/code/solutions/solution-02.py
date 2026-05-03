#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：改进的代码审查反馈系统

改进点：
- 使用更具体的反馈模板
- 添加了建设性建议
- 改进了反馈分类逻辑
- 增强了JSON输出格式
"""

from enum import Enum
from typing import List, Dict, Any, Optional
import json


class SeverityLevel(Enum):
    """严重级别枚举"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReviewFeedback:
    """代码审查反馈类"""

    def __init__(self, comment: str, severity: SeverityLevel,
                 line_number: Optional[int] = None,
                 suggestion: Optional[str] = None):
        """初始化反馈

        Args:
            comment: 反馈内容
            severity: 严重级别
            line_number: 行号（可选）
            suggestion: 改进建议（可选）
        """
        self.comment = comment
        self.severity = severity
        self.line_number = line_number
        self.suggestion = suggestion

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式

        Returns:
            包含反馈信息的字典
        """
        result = {
            "comment": self.comment,
            "severity": self.severity.value,
            "category": self._get_feedback_category(),
            "impact": self._get_impact_level()
        }
        if self.line_number:
            result["line"] = self.line_number
        if self.suggestion:
            result["suggestion"] = self.suggestion
        return result

    def _get_feedback_category(self) -> str:
        """获取反馈类别

        Returns:
            反馈类别字符串
        """
        comment_lower = self.comment.lower()
        if any(keyword in comment_lower for keyword in ["安全", "security", "漏洞", "injection"]):
            return "security"
        elif any(keyword in comment_lower for keyword in ["性能", "performance", "效率", "slow"]):
            return "performance"
        elif any(keyword in comment_lower for keyword in ["可读性", "readability", "命名", "name"]):
            return "readability"
        elif any(keyword in comment_lower for keyword in ["正确性", "correctness", "错误", "bug"]):
            return "correctness"
        else:
            return "maintainability"

    def _get_impact_level(self) -> str:
        """获取影响级别

        Returns:
            影响级别字符串
        """
        if self.severity == SeverityLevel.CRITICAL:
            return "high"
        elif self.severity == SeverityLevel.HIGH:
            return "medium"
        else:
            return "low"


class FeedbackGenerator:
    """反馈生成器类"""

    def __init__(self):
        """初始化反馈生成器"""
        self.feedback_templates = {
            SeverityLevel.CRITICAL: [
                {
                    "comment": "存在安全漏洞：{issue} - 必须立即修复",
                    "suggestion": "建议使用参数化查询或输入验证来防止此类漏洞"
                },
                {
                    "comment": "逻辑错误：{issue} - 会导致程序崩溃或数据损坏",
                    "suggestion": "添加适当的错误处理和边界条件检查"
                }
            ],
            SeverityLevel.HIGH: [
                {
                    "comment": "性能问题：{issue} - 建议优化以提高效率",
                    "suggestion": "考虑使用更高效的数据结构或算法"
                },
                {
                    "comment": "缺少关键测试：{issue} - 建议添加相关测试用例",
                    "suggestion": "为这个功能编写单元测试和集成测试"
                }
            ],
            SeverityLevel.MEDIUM: [
                {
                    "comment": "代码可读性：{issue} - 建议重构以提高可维护性",
                    "suggestion": "提取复杂逻辑到独立的函数中"
                },
                {
                    "comment": "命名不清晰：{issue} - 建议使用更具描述性的名称",
                    "suggestion": "使用能清楚表达意图的变量和函数名"
                }
            ],
            SeverityLevel.LOW: [
                {
                    "comment": "格式问题：{issue} - 建议遵循团队代码风格指南",
                    "suggestion": "使用自动格式化工具保持一致性"
                },
                {
                    "comment": "注释可以更详细：{issue} - 帮助其他开发者理解",
                    "suggestion": "添加关于为什么这样实现的上下文信息"
                }
            ]
        }

    def generate_feedback(self, issue_description: str, severity: SeverityLevel,
                         line_number: Optional[int] = None) -> ReviewFeedback:
        """生成反馈

        Args:
            issue_description: 问题描述
            severity: 严重级别
            line_number: 行号

        Returns:
            生成的反馈对象
        """
        template = self.feedback_templates[severity][0]
        comment = template["comment"].format(issue=issue_description)
        suggestion = template["suggestion"]
        return ReviewFeedback(comment, severity, line_number, suggestion)

    def categorize_feedback(self, feedback_list: List[ReviewFeedback]) -> Dict[str, int]:
        """对反馈进行分类统计

        Args:
            feedback_list: 反馈列表

        Returns:
            分类统计字典
        """
        stats = {"security": 0, "performance": 0, "readability": 0,
                "correctness": 0, "maintainability": 0}

        for feedback in feedback_list:
            category = feedback._get_feedback_category()
            stats[category] += 1

        return stats


def main() -> None:
    """主函数"""
    print("改进后的反馈系统提供更具体的建议!")


if __name__ == "__main__":
    main()