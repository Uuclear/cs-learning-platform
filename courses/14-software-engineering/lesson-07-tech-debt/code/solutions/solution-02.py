#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：增强的技术债务追踪器
支持债务分类、状态跟踪和报告生成
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class DebtCategory(Enum):
    """技术债务类别"""
    CODE = "代码债务"
    ARCHITECTURE = "架构债务"
    TESTING = "测试债务"
    DOCUMENTATION = "文档债务"
    INFRASTRUCTURE = "基础设施债务"


class DebtStatus(Enum):
    """技术债务状态"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    WONT_FIX = "wont_fix"


class EnhancedTechDebtItem:
    """增强的技术债务项"""

    def __init__(self,
                 description: str,
                 category: DebtCategory,
                 risk_score: int,
                 impact_score: int,
                 location: str = "",
                 created_date: str = None,
                 due_date: str = None,
                 assigned_to: str = "",
                 status: DebtStatus = DebtStatus.OPEN,
                 notes: str = ""):
        self.description = description
        self.category = category
        self.risk_score = min(10, max(1, risk_score))  # 1-10范围
        self.impact_score = min(10, max(1, impact_score))
        self.location = location
        self.created_date = created_date or datetime.now().strftime("%Y-%m-%d")
        self.due_date = due_date or ""
        self.assigned_to = assigned_to
        self.status = status
        self.notes = notes
        self.priority_score = self._calculate_priority()

    def _calculate_priority(self) -> float:
        """计算优先级分数"""
        base_score = self.risk_score * 0.6 + self.impact_score * 0.4

        # 根据类别调整权重
        category_multipliers = {
            DebtCategory.CODE: 1.0,
            DebtCategory.ARCHITECTURE: 1.5,  # 架构问题通常更严重
            DebtCategory.TESTING: 1.2,      # 测试缺失影响质量
            DebtCategory.DOCUMENTATION: 0.8, # 文档问题相对轻微
            DebtCategory.INFRASTRUCTURE: 1.3  # 基础设施问题可能影响部署
        }

        multiplier = category_multipliers.get(self.category, 1.0)
        return base_score * multiplier

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'description': self.description,
            'category': self.category.value,
            'risk_score': self.risk_score,
            'impact_score': self.impact_score,
            'location': self.location,
            'created_date': self.created_date,
            'due_date': self.due_date,
            'assigned_to': self.assigned_to,
            'status': self.status.value,
            'notes': self.notes,
            'priority_score': self.priority_score
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedTechDebtItem':
        """从字典创建实例"""
        category_map = {v.value: v for v in DebtCategory}
        status_map = {v.value: v for v in DebtStatus}

        return cls(
            description=data['description'],
            category=category_map[data['category']],
            risk_score=data['risk_score'],
            impact_score=data['impact_score'],
            location=data.get('location', ''),
            created_date=data.get('created_date'),
            due_date=data.get('due_date', ''),
            assigned_to=data.get('assigned_to', ''),
            status=status_map[data['status']],
            notes=data.get('notes', '')
        )


class EnhancedTechDebtTracker:
    """增强的技术债务追踪器"""

    def __init__(self):
        self.debt_items: List[EnhancedTechDebtItem] = []

    def add_debt_item(self, item: EnhancedTechDebtItem):
        """添加技术债务项"""
        self.debt_items.append(item)

    def get_items_by_status(self, status: DebtStatus) -> List[EnhancedTechDebtItem]:
        """按状态获取项目"""
        return [item for item in self.debt_items if item.status == status]

    def get_items_by_category(self, category: DebtCategory) -> List[EnhancedTechDebtItem]:
        """按类别获取项目"""
        return [item for item in self.debt_items if item.category == category]

    def get_high_priority_items(self, threshold: float = 50.0) -> List[EnhancedTechDebtItem]:
        """获取高优先级项目"""
        return [item for item in self.debt_items
                if item.priority_score >= threshold and item.status != DebtStatus.RESOLVED]

    def get_overdue_items(self) -> List[EnhancedTechDebtItem]:
        """获取超期项目"""
        today = datetime.now().date()
        overdue_items = []
        for item in self.debt_items:
            if item.due_date and item.status not in [DebtStatus.RESOLVED, DebtStatus.WONT_FIX]:
                try:
                    due_date = datetime.strptime(item.due_date, "%Y-%m-%d").date()
                    if due_date < today:
                        overdue_items.append(item)
                except ValueError:
                    pass  # 处理无效日期格式
        return overdue_items

    def get_sorted_by_priority(self) -> List[EnhancedTechDebtItem]:
        """按优先级排序（降序）"""
        return sorted([item for item in self.debt_items if item.status != DebtStatus.RESOLVED],
                     key=lambda x: x.priority_score, reverse=True)

    def generate_report(self, include_resolved=False) -> str:
        """生成报告字符串"""
        report_lines = []
        if not self.debt_items:
            return "没有找到技术债务项。"

        # 统计信息
        total_count = len(self.debt_items)
        resolved_count = len(self.get_items_by_status(DebtStatus.RESOLVED))
        active_count = total_count - resolved_count

        report_lines.append(f"技术债务报告 - 总共 {total_count} 个项目，{active_count} 个活跃，{resolved_count} 个已解决\n")

        # 按类别统计
        category_counts = {}
        for category in DebtCategory:
            count = len(self.get_items_by_category(category))
            category_counts[category.value] = count
        report_lines.append("按类别统计:")
        for category_name, count in category_counts.items():
            if count > 0:
                report_lines.append(f"  {category_name}: {count} 个")
        report_lines.append("")

        # 超期项目
        overdue_items = self.get_overdue_items()
        if overdue_items:
            report_lines.append(f"⚠️ 超期项目 ({len(overdue_items)}):")
            for item in overdue_items:
                report_lines.append(f"  [{item.priority_score:.1f}] {item.description}")
                report_lines.append(f"      截止日期: {item.due_date}, 负责人: {item.assigned_to or '未分配'}")
            report_lines.append("")

        # 高优先级项目
        high_priority = self.get_high_priority_items(threshold=60.0)
        if high_priority:
            report_lines.append(f"🔥 高优先级项目 ({len(high_priority)}):")
            for item in high_priority:
                report_lines.append(f"  [{item.priority_score:.1f}] {item.description}")
                report_lines.append(f"      类别: {item.category.value}")
                report_lines.append(f"      风险: {item.risk_score}/10, 影响: {item.impact_score}/10")
                report_lines.append(f"      位置: {item.location}")
                report_lines.append(f"      状态: {item.status.value}, 负责人: {item.assigned_to or '未分配'}")
                if item.due_date:
                    report_lines.append(f"      截止日期: {item.due_date}")
                report_lines.append("")

        return "\n".join(report_lines)

    def save_to_file(self, filename: str):
        """保存到JSON文件"""
        data = [item.to_dict() for item in self.debt_items]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str):
        """从JSON文件加载"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.debt_items = [EnhancedTechDebtItem.from_dict(item) for item in data]
        except FileNotFoundError:
            print(f"文件 {filename} 不存在，创建新的债务追踪器")
            self.debt_items = []


def main():
    """主函数 - 演示增强版技术债务追踪器的使用"""
    tracker = EnhancedTechDebtTracker()

    # 添加一些示例技术债务项
    debt_items = [
        EnhancedTechDebtItem(
            description="认证模块使用硬编码密码，存在安全风险",
            category=DebtCategory.CODE,
            risk_score=9,
            impact_score=8,
            location="auth/auth_service.py",
            due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            assigned_to="security-team"
        ),
        EnhancedTechDebtItem(
            description="数据库查询没有索引优化，性能缓慢",
            category=DebtCategory.CODE,
            risk_score=6,
            impact_score=7,
            location="models/user_model.py",
            due_date=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            assigned_to="database-team"
        ),
        EnhancedTechDebtItem(
            description="缺少单元测试覆盖核心业务逻辑",
            category=DebtCategory.TESTING,
            risk_score=5,
            impact_score=8,
            location="services/order_service.py",
            due_date=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            assigned_to="backend-team"
        ),
        EnhancedTechDebtItem(
            description="API文档过时，与实际实现不符",
            category=DebtCategory.DOCUMENTATION,
            risk_score=3,
            impact_score=6,
            location="api/v1/endpoints.py",
            due_date=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            assigned_to="api-team"
        )
    ]

    for item in debt_items:
        tracker.add_debt_item(item)

    # 显示完整报告
    print(tracker.generate_report())

    # 保存到文件
    tracker.save_to_file("enhanced_tech_debt_example.json")
    print("增强版技术债务数据已保存到 enhanced_tech_debt_example.json")


if __name__ == "__main__":
    main()