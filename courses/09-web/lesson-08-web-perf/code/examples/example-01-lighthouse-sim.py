#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：模拟Lighthouse性能评分系统

这个脚本模拟Google Lighthouse的性能评分算法，
基于Core Web Vitals指标（LCP、FID/INP、CLS）计算综合性能分数。
"""

import math
import random


def calculate_lcp_score(lcp_time_ms):
    """
    计算Largest Contentful Paint (LCP) 得分

    LCP衡量页面主要内容加载完成的时间：
    - 良好：<= 2.5秒 (得分100)
    - 需要改进：2.5-4秒 (得分50-99)
    - 差：> 4秒 (得分0-49)

    :param lcp_time_ms: LCP时间（毫秒）
    :return: LCP得分 (0-100)
    """
    if lcp_time_ms <= 2500:
        return 100
    elif lcp_time_ms <= 4000:
        # 线性插值：2500ms=100分, 4000ms=50分
        return 100 - ((lcp_time_ms - 2500) / 1500) * 50
    else:
        # 指数衰减：超过4秒后分数快速下降
        return max(0, 50 * math.exp(-(lcp_time_ms - 4000) / 2000))


def calculate_inp_score(inp_time_ms):
    """
    计算Interaction to Next Paint (INP) 得分

    INP衡量用户交互响应速度（替代FID）：
    - 良好：<= 200ms (得分100)
    - 需要改进：200-500ms (得分50-99)
    - 差：> 500ms (得分0-49)

    :param inp_time_ms: INP时间（毫秒）
    :return: INP得分 (0-100)
    """
    if inp_time_ms <= 200:
        return 100
    elif inp_time_ms <= 500:
        # 线性插值：200ms=100分, 500ms=50分
        return 100 - ((inp_time_ms - 200) / 300) * 50
    else:
        # 指数衰减
        return max(0, 50 * math.exp(-(inp_time_ms - 500) / 1000))


def calculate_cls_score(cls_value):
    """
    计算Cumulative Layout Shift (CLS) 得分

    CLS衡量页面布局稳定性：
    - 良好：<= 0.1 (得分100)
    - 需要改进：0.1-0.25 (得分50-99)
    - 差：> 0.25 (得分0-49)

    :param cls_value: CLS值（无单位）
    :return: CLS得分 (0-100)
    """
    if cls_value <= 0.1:
        return 100
    elif cls_value <= 0.25:
        # 线性插值：0.1=100分, 0.25=50分
        return 100 - ((cls_value - 0.1) / 0.15) * 50
    else:
        # 指数衰减
        return max(0, 50 * math.exp(-(cls_value - 0.25) / 0.2))


def calculate_performance_score(lcp_ms, inp_ms, cls_val):
    """
    计算综合性能得分

    使用加权平均，其中LCP权重最高，因为它是最重要的指标

    :param lcp_ms: LCP时间（毫秒）
    :param inp_ms: INP时间（毫秒）
    :param cls_val: CLS值
    :return: 综合性能得分 (0-100)
    """
    lcp_score = calculate_lcp_score(lcp_ms)
    inp_score = calculate_inp_score(inp_ms)
    cls_score = calculate_cls_score(cls_val)

    # 加权平均：LCP (40%), INP (30%), CLS (30%)
    weighted_score = (lcp_score * 0.4 + inp_score * 0.3 + cls_score * 0.3)

    return round(weighted_score, 1)


def main():
    """主函数：演示不同性能场景的评分"""
    print("=== Lighthouse性能评分模拟器 ===\n")

    # 场景1：优秀性能
    print("场景1：优秀性能网站")
    lcp1, inp1, cls1 = 1800, 150, 0.05
    score1 = calculate_performance_score(lcp1, inp1, cls1)
    print(f"LCP: {lcp1}ms, INP: {inp1}ms, CLS: {cls1}")
    print(f"性能得分: {score1}/100\n")

    # 场景2：中等性能
    print("场景2：中等性能网站")
    lcp2, inp2, cls2 = 3200, 350, 0.18
    score2 = calculate_performance_score(lcp2, inp2, cls2)
    print(f"LCP: {lcp2}ms, INP: {inp2}ms, CLS: {cls2}")
    print(f"性能得分: {score2}/100\n")

    # 场景3：较差性能
    print("场景3：较差性能网站")
    lcp3, inp3, cls3 = 6500, 800, 0.45
    score3 = calculate_performance_score(lcp3, inp3, cls3)
    print(f"LCP: {lcp3}ms, INP: {inp3}ms, CLS: {cls3}")
    print(f"性能得分: {score3}/100\n")

    # 交互式输入（可选）
    print("=== 自定义测试 ===")
    try:
        custom_lcp = float(input("请输入LCP时间（毫秒）[默认1800]: ") or "1800")
        custom_inp = float(input("请输入INP时间（毫秒）[默认150]: ") or "150")
        custom_cls = float(input("请输入CLS值[默认0.05]: ") or "0.05")

        custom_score = calculate_performance_score(custom_lcp, custom_inp, custom_cls)
        print(f"\n自定义性能得分: {custom_score}/100")

        # 给出优化建议
        if custom_score >= 90:
            print("✅ 性能优秀！继续保持！")
        elif custom_score >= 50:
            print("⚠️  性能需要改进，重点关注LCP和INP优化")
        else:
            print("❌ 性能很差，需要全面优化！")

    except (ValueError, KeyboardInterrupt):
        print("\n跳过自定义测试")


if __name__ == "__main__":
    main()