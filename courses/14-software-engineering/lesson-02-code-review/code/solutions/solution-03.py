#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：改进的代码审查指标系统

改进点：
- 添加了更多指标维度
- 改进了效率分数计算
- 增加了趋势分析功能
- 提供了更实用的建议
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import statistics


class ReviewMetrics:
    """代码审查指标类"""

    def __init__(self):
        """初始化指标收集器"""
        self.reviews: List[Dict[str, Any]] = []
        self.defect_detection_rates: List[float] = []

    def add_review(self, review_data: Dict[str, Any]) -> None:
        """添加审查数据

        Args:
            review_data: 包含审查信息的字典
        """
        required_fields = ["review_time_hours", "lines_of_code", "comments_count",
                          "defects_found", "total_defects"]
        if not all(field in review_data for field in required_fields):
            raise ValueError("缺少必要的审查数据字段")

        review_data["comments_per_loc"] = (
            review_data["comments_count"] / review_data["lines_of_code"]
            if review_data["lines_of_code"] > 0 else 0
        )
        review_data["defect_detection_rate"] = (
            review_data["defects_found"] / review_data["total_defects"]
            if review_data["total_defects"] > 0 else 0
        )

        self.reviews.append(review_data)
        self.defect_detection_rates.append(review_data["defect_detection_rate"])

    def calculate_average_review_time(self) -> float:
        """计算平均审查时间

        Returns:
            平均审查时间（小时）
        """
        if not self.reviews:
            return 0.0
        return statistics.mean([r["review_time_hours"] for r in self.reviews])

    def calculate_average_comments_per_loc(self) -> float:
        """计算平均每行代码评论数

        Returns:
            平均每行代码评论数
        """
        if not self.reviews:
            return 0.0
        return statistics.mean([r["comments_per_loc"] for r in self.reviews])

    def calculate_defect_detection_rate(self) -> float:
        """计算整体缺陷检测率

        Returns:
            整体缺陷检测率
        """
        if not self.defect_detection_rates:
            return 0.0
        return statistics.mean(self.defect_detection_rates)

    def get_efficiency_score(self) -> float:
        """计算审查效率分数

        Returns:
            效率分数（0-100）
        """
        if not self.reviews:
            return 0.0

        # 缺陷检测率分数 (0-50分)
        defect_score = min(self.calculate_defect_detection_rate() * 100, 50)

        # 评论质量分数 (0-30分)
        avg_comments_per_loc = self.calculate_average_comments_per_loc()
        if 0.05 <= avg_comments_per_loc <= 0.2:
            comment_score = 30
        elif avg_comments_per_loc < 0.05:
            comment_score = min(avg_comments_per_loc / 0.05 * 15, 15)
        else:
            comment_score = max(0, 30 - (avg_comments_per_loc - 0.2) * 50)

        # 审查速度分数 (0-20分)
        avg_time = self.calculate_average_review_time()
        if avg_time <= 2:
            time_score = 20
        elif avg_time <= 4:
            time_score = 15
        elif avg_time <= 8:
            time_score = 10
        else:
            time_score = max(0, 20 - (avg_time - 8) * 2)

        return defect_score + comment_score + time_score

    def analyze_trends(self) -> Dict[str, str]:
        """分析指标趋势

        Returns:
            趋势分析结果
        """
        if len(self.reviews) < 2:
            return {"message": "需要至少2次审查才能分析趋势"}

        # 分析最近两次审查的变化
        recent = self.reviews[-1]
        previous = self.reviews[-2]

        trends = {}

        # 审查时间趋势
        time_change = recent["review_time_hours"] - previous["review_time_hours"]
        if abs(time_change) < 0.1:
            trends["review_time"] = "稳定"
        elif time_change < 0:
            trends["review_time"] = "改善" if abs(time_change) > 0.5 else "轻微改善"
        else:
            trends["review_time"] = "恶化" if time_change > 0.5 else "轻微恶化"

        # 缺陷检测率趋势
        rate_change = recent["defect_detection_rate"] - previous["defect_detection_rate"]
        if abs(rate_change) < 0.05:
            trends["defect_detection"] = "稳定"
        elif rate_change > 0:
            trends["defect_detection"] = "改善"
        else:
            trends["defect_detection"] = "恶化"

        return trends

    def generate_report(self) -> Dict[str, Any]:
        """生成审查指标报告

        Returns:
            包含所有指标的报告字典
        """
        report = {
            "total_reviews": len(self.reviews),
            "average_review_time_hours": round(self.calculate_average_review_time(), 2),
            "average_comments_per_loc": round(self.calculate_average_comments_per_loc(), 4),
            "overall_defect_detection_rate": round(self.calculate_defect_detection_rate(), 4),
            "efficiency_score": round(self.get_efficiency_score(), 1),
            "trends": self.analyze_trends(),
            "recommendations": self._get_recommendations()
        }
        return report

    def _get_recommendations(self) -> List[str]:
        """获取改进建议

        Returns:
            建议列表
        """
        recommendations = []

        avg_time = self.calculate_average_review_time()
        if avg_time > 4:
            recommendations.append("审查时间过长，考虑拆分大型PR或增加审查人员")

        avg_comments = self.calculate_average_comments_per_loc()
        if avg_comments < 0.03:
            recommendations.append("评论密度较低，建议更详细地审查代码")
        elif avg_comments > 0.3:
            recommendations.append("评论密度过高，考虑聚焦关键问题而非风格偏好")

        defect_rate = self.calculate_defect_detection_rate()
        if defect_rate < 0.6:
            recommendations.append("缺陷检测率偏低，建议加强测试覆盖和静态分析")

        efficiency = self.get_efficiency_score()
        if efficiency < 70:
            recommendations.append("整体审查效率有待提高")

        if not recommendations:
            recommendations.append("当前审查流程表现良好！继续保持。")

        return recommendations


def main() -> None:
    """主函数"""
    print("改进后的指标系统提供趋势分析和更精准的建议!")


if __name__ == "__main__":
    main()