#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：技术债务追踪器
使用风险vs影响评分模型来跟踪和优先处理技术债务项
"""

import json
from typing import List, Dict, Any
from datetime import datetime


class TechDebtItem:
    """技术债务项类"""

    def __init__(self, description: str, risk_score: int, impact_score: int,
                 location: str = "", created_date: str = None):
        """
        初始化技术债务项
        :param description: 债务描述
        :param risk_score: 风险评分 (1-10)
        :param impact_score: 影响评分 (1-10)
        :param location: 代码位置
        :param created_date: 创建日期
        """
        self.description = description
        self.risk_score = min(10, max(1, risk_score))  # 限制在1-10范围内
        self.impact_score = min(10, max(1, impact_score))
        self.location = location
        self.created_date = created_date or datetime.now().strftime("%Y-%m-%d")
        self.priority_score = self._calculate_priority()

    def _calculate_priority(self) -> float:
        """计算优先级分数 = 风险分数 × 影响分数"""
        return self.risk_score * self.impact_score

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'description': self.description,
            'risk_score': self.risk_score,
            'impact_score': self.impact_score,
            'location': self.location,
            'created_date': self.created_date,
            'priority_score': self.priority_score
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TechDebtItem':
        """从字典创建实例"""
        return cls(
            description=data['description'],
            risk_score=data['risk_score'],
            impact_score=data['impact_score'],
            location=data.get('location', ''),
            created_date=data.get('created_date')
        )


class TechDebtTracker:
    """技术债务追踪器"""

    def __init__(self):
        self.debt_items: List[TechDebtItem] = []

    def add_debt_item(self, item: TechDebtItem):
        """添加技术债务项"""
        self.debt_items.append(item)

    def get_high_priority_items(self, threshold: float = 50.0) -> List[TechDebtItem]:
        """获取高优先级的技术债务项"""
        return [item for item in self.debt_items
                if item.priority_score >= threshold]

    def get_sorted_by_priority(self) -> List[TechDebtItem]:
        """按优先级排序（降序）"""
        return sorted(self.debt_items, key=lambda x: x.priority_score, reverse=True)

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
            self.debt_items = [TechDebtItem.from_dict(item) for item in data]
        except FileNotFoundError:
            print(f"文件 {filename} 不存在，创建新的债务追踪器")
            self.debt_items = []


def main():
    """主函数 - 演示技术债务追踪器的使用"""
    tracker = TechDebtTracker()

    # 添加一些示例技术债务项
    debt_items = [
        TechDebtItem(
            description="认证模块使用硬编码密码，存在安全风险",
            risk_score=9,
            impact_score=8,
            location="auth/auth_service.py"
        ),
        TechDebtItem(
            description="数据库查询没有索引优化，性能缓慢",
            risk_score=6,
            impact_score=7,
            location="models/user_model.py"
        ),
        TechDebtItem(
            description="缺少单元测试覆盖核心业务逻辑",
            risk_score=5,
            impact_score=8,
            location="services/order_service.py"
        ),
        TechDebtItem(
            description="API文档过时，与实际实现不符",
            risk_score=3,
            impact_score=6,
            location="api/v1/endpoints.py"
        )
    ]

    for item in debt_items:
        tracker.add_debt_item(item)

    # 显示高优先级项
    high_priority = tracker.get_high_priority_items(threshold=50.0)
    print("高优先级技术债务项 (优先级 >= 50):")
    for item in high_priority:
        print(f"  [{item.priority_score:.1f}] {item.description}")
        print(f"      风险: {item.risk_score}, 影响: {item.impact_score}")
        print(f"      位置: {item.location}")
        print()

    # 保存到文件
    tracker.save_to_file("tech_debt_example.json")
    print("技术债务数据已保存到 tech_debt_example.json")


if __name__ == "__main__":
    main()