#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：Lighthouse评分系统完整实现

这个解决方案提供了更精确的Lighthouse评分算法，
包括非线性评分曲线和实际的性能阈值。
"""

import math


def calculate_metric_score(value, good_threshold, poor_threshold):
    """
    通用指标评分函数

    :param value: 实际测量值
    :param good_threshold: 良好阈值
    :param poor_threshold: 差阈值
    :return: 指标得分 (0-100)
    """
    if value <= good_threshold:
        return 100
    elif value >= poor_threshold:
        return 0
    else:
        # 使用非线性插值（Lighthouse实际使用的算法）
        weight = (value - good_threshold) / (poor_threshold - good_threshold)
        score = 100 - (weight * 100)
        # 应用非线性调整
        adjusted_score = 100 * (1 - math.pow(weight, 2))
        return max(0, min(100, adjusted_score))


def calculate_lcp_score(lcp_time_ms):
    """计算LCP得分（使用实际Lighthouse阈值）"""
    return calculate_metric_score(lcp_time_ms, 2500, 4000)


def calculate_inp_score(inp_time_ms):
    """计算INP得分（使用实际Lighthouse阈值）"""
    return calculate_metric_score(inp_time_ms, 200, 500)


def calculate_cls_score(cls_value):
    """计算CLS得分（使用实际Lighthouse阈值）"""
    return calculate_metric_score(cls_value, 0.1, 0.25)


def calculate_performance_score(lcp_ms, inp_ms, cls_val):
    """计算综合性能得分"""
    lcp_score = calculate_lcp_score(lcp_ms)
    inp_score = calculate_inp_score(inp_ms)
    cls_score = calculate_cls_score(cls_val)

    # Lighthouse实际权重
    weighted_score = (lcp_score * 0.25 + inp_score * 0.25 + cls_score * 0.15 +
                     35)  # 其他指标占35%

    return round(min(100, max(0, weighted_score)), 1)


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        (1800, 150, 0.05),   # 优秀
        (3200, 350, 0.18),   # 中等
        (6500, 800, 0.45),   # 较差
    ]

    for lcp, inp, cls in test_cases:
        score = calculate_performance_score(lcp, inp, cls)
        print(f"LCP:{lcp}ms, INP:{inp}ms, CLS:{cls} -> 得分:{score}")