#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码审查指标模拟器

这个脚本模拟代码审查指标的收集和分析，包括：
- 审查时间统计
- 每行代码评论数
- 缺陷检测率
- 审查效率分析
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import statistics


class ReviewMetrics:
    """代码审查指标类"""

    def __init__(self):
        """初始化指标收集器"""
        self.reviews = []
        self.defect_detection_rates = []

    def add_review(self, review_data: Dict[str, Any]) -> None:
        """添加审查数据

        Args:
            review_data: 包含审查信息的字典
        """
        required_fields = ["review_time_hours", "lines_of_code", "comments_count",
                          "defects_found", "total_defects"]
        if not all(field in review_data for field in required_fields):
            raise ValueError("缺少必要的审查数据字段")

        # 计算衍生指标
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

        效率分数基于：
        - 缺陷检测率（权重 0.5）
        - 评论质量（权重 0.3）
        - 审查速度（权重 0.2）

        Returns:
            效率分数（0-100）
        """
        if not self.reviews:
            return 0.0

        # 缺陷检测率分数 (0-50分)
        defect_score = min(self.calculate_defect_detection_rate() * 100, 50)

        # 评论质量分数：适中的评论密度更好 (0-30分)
        avg_comments_per_loc = self.calculate_average_comments_per_loc()
        if 0.05 <= avg_comments_per_loc <= 0.2:
            comment_score = 30
        elif avg_comments_per_loc < 0.05:
            comment_score = avg_comments_per_loc / 0.05 * 15  # 太少评论
        else:
            comment_score = max(0, 30 - (avg_comments_per_loc - 0.2) * 100)  # 太多评论

        # 审查速度分数：合理的时间范围 (0-20分)
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

    def generate_report(self) -> Dict[str, Any]:
        """生成审查指标报告

        Returns:
            包含所有指标的报告字典
        """
        return {
            "total_reviews": len(self.reviews),
            "average_review_time_hours": round(self.calculate_average_review_time(), 2),
            "average_comments_per_loc": round(self.calculate_average_comments_per_loc(), 4),
            "overall_defect_detection_rate": round(self.calculate_defect_detection_rate(), 4),
            "efficiency_score": round(self.get_efficiency_score(), 1),
            "recommendations": self._get_recommendations()
        }

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
            recommendations.append("整体审查效率有待提高，参考上述具体建议")

        return recommendations if recommendations else ["当前审查流程表现良好！"]


def main():
    """主函数 - 演示代码审查指标分析"""
    print("=== 代码审查指标模拟器 ===\n")

    # 创建指标收集器
    metrics = ReviewMetrics()

    # 添加模拟审查数据
    sample_reviews = [
        {
            "review_time_hours": 1.5,
            "lines_of_code": 200,
            "comments_count": 8,
            "defects_found": 3,
            "total_defects": 4
        },
        {
            "review_time_hours": 3.0,
            "lines_of_code": 500,
            "comments_count": 15,
            "defects_found": 5,
            "total_defects": 8
        },
        {
            "review_time_hours": 0.8,
            "lines_of_code": 100,
            "comments_count": 6,
            "defects_found": 2,
            "total_defects": 2
        }
    ]

    for review in sample_reviews:
        metrics.add_review(review)

    # 生成报告
    report = metrics.generate_report()

    print("📈 代码审查指标报告:")
    print(f"   • 总审查次数: {report['total_reviews']}")
    print(f"   • 平均审查时间: {report['average_review_time_hours']} 小时")
    print(f"   • 平均每行代码评论数: {report['average_comments_per_loc']:.4f}")
    print(f"   • 整体缺陷检测率: {report['overall_defect_detection_rate']:.2%}")
    print(f"   • 审查效率分数: {report['efficiency_score']}/100")

    print("\n💡 改进建议:")
    for i, recommendation in enumerate(report["recommendations"], 1):
        print(f"   {i}. {recommendation}")

    # 显示原始数据
    print("\n📊 原始审查数据:")
    for i, review in enumerate(metrics.reviews, 1):
        print(f"   审查 #{i}:")
        print(f"     - 时间: {review['review_time_hours']}h")
        print(f"     - 代码行数: {review['lines_of_code']}")
        print(f"     - 评论数: {review['comments_count']}")
        print(f"     - 缺陷检测率: {review['defect_detection_rate']:.2%}")


if __name__ == "__main__":
    main()