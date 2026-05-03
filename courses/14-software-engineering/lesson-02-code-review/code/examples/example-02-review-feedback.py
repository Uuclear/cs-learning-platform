#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码审查反馈系统模拟器

这个脚本模拟代码审查反馈系统，包括：
- 不同严重级别的反馈分类
- 建设性反馈生成
- 反馈统计和分析
"""

from enum import Enum
from typing import List, Dict, Any
import json


class SeverityLevel(Enum):
    """严重级别枚举"""
    CRITICAL = "critical"      # 关键问题 - 必须修复
    HIGH = "high"             # 高优先级 - 强烈建议修复
    MEDIUM = "medium"         # 中等优先级 - 建议修复
    LOW = "low"               # 低优先级 - 可选改进


class ReviewFeedback:
    """代码审查反馈类"""

    def __init__(self, comment: str, severity: SeverityLevel, line_number: int = None):
        """初始化反馈

        Args:
            comment: 反馈内容
            severity: 严重级别
            line_number: 行号（可选）
        """
        self.comment = comment
        self.severity = severity
        self.line_number = line_number

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式

        Returns:
            包含反馈信息的字典
        """
        result = {
            "comment": self.comment,
            "severity": self.severity.value,
            "type": self._get_feedback_type()
        }
        if self.line_number:
            result["line"] = self.line_number
        return result

    def _get_feedback_type(self) -> str:
        """获取反馈类型

        Returns:
            反馈类型字符串
        """
        if "安全" in self.comment or "security" in self.comment.lower():
            return "security"
        elif "性能" in self.comment or "performance" in self.comment.lower():
            return "performance"
        elif "可读性" in self.comment or "readability" in self.comment.lower():
            return "readability"
        elif "正确性" in self.comment or "correctness" in self.comment.lower():
            return "correctness"
        else:
            return "general"


class FeedbackGenerator:
    """反馈生成器类"""

    def __init__(self):
        """初始化反馈生成器"""
        self.feedback_templates = {
            SeverityLevel.CRITICAL: [
                "存在安全漏洞：{issue} - 必须立即修复",
                "逻辑错误：{issue} - 会导致程序崩溃或数据损坏",
                "缺少必要的错误处理：{issue} - 可能导致未处理异常"
            ],
            SeverityLevel.HIGH: [
                "性能问题：{issue} - 建议优化以提高效率",
                "API设计问题：{issue} - 可能影响系统稳定性",
                "缺少关键测试：{issue} - 建议添加相关测试用例"
            ],
            SeverityLevel.MEDIUM: [
                "代码可读性：{issue} - 建议重构以提高可维护性",
                "命名不清晰：{issue} - 建议使用更具描述性的名称",
                "重复代码：{issue} - 考虑提取到公共函数中"
            ],
            SeverityLevel.LOW: [
                "格式问题：{issue} - 建议遵循团队代码风格指南",
                "注释可以更详细：{issue} - 帮助其他开发者理解",
                "可以考虑的改进：{issue} - 非必需但有益"
            ]
        }

    def generate_feedback(self, issue_description: str, severity: SeverityLevel,
                         line_number: int = None) -> ReviewFeedback:
        """生成反馈

        Args:
            issue_description: 问题描述
            severity: 严重级别
            line_number: 行号

        Returns:
            生成的反馈对象
        """
        template = self.feedback_templates[severity][0]  # 使用第一个模板
        comment = template.format(issue=issue_description)
        return ReviewFeedback(comment, severity, line_number)

    def categorize_feedback(self, feedback_list: List[ReviewFeedback]) -> Dict[str, int]:
        """对反馈进行分类统计

        Args:
            feedback_list: 反馈列表

        Returns:
            分类统计字典
        """
        stats = {"security": 0, "performance": 0, "readability": 0,
                "correctness": 0, "general": 0}

        for feedback in feedback_list:
            stats[feedback._get_feedback_type()] += 1

        return stats


def main():
    """主函数 - 演示代码审查反馈系统"""
    print("=== 代码审查反馈系统模拟器 ===\n")

    # 创建反馈生成器
    generator = FeedbackGenerator()

    # 模拟不同严重级别的反馈
    feedback_items = [
        ("SQL注入风险", SeverityLevel.CRITICAL, 45),
        ("数据库查询未索引优化", SeverityLevel.HIGH, 78),
        ("函数名不够描述性", SeverityLevel.MEDIUM, 123),
        ("缺少行尾空格", SeverityLevel.LOW, 201)
    ]

    feedback_list = []
    for issue, severity, line in feedback_items:
        feedback = generator.generate_feedback(issue, severity, line)
        feedback_list.append(feedback)

    # 显示所有反馈
    print("📋 代码审查反馈:")
    for i, feedback in enumerate(feedback_list, 1):
        emoji = {"critical": "🚨", "high": "⚠️", "medium": "📝", "low": "💡"}[feedback.severity.value]
        print(f"{emoji} [{feedback.severity.value.upper()}] {feedback.comment}")
        if feedback.line_number:
            print(f"   📍 行号: {feedback.line_number}")
        print()

    # 统计反馈类型
    stats = generator.categorize_feedback(feedback_list)
    print("📊 反馈类型统计:")
    for category, count in stats.items():
        if count > 0:
            print(f"   • {category}: {count}")

    # 显示JSON格式输出
    print("\n📄 JSON格式输出:")
    json_output = [fb.to_dict() for fb in feedback_list]
    print(json.dumps(json_output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()