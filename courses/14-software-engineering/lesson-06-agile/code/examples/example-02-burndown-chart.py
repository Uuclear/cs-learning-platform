#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：燃尽图数据生成
从冲刺进度生成ASCII燃尽图数据（每日剩余故事点数 vs 理想线）
"""

from typing import List, Tuple
import math


def calculate_burndown_data(
    total_story_points: int,
    daily_progress: List[int],
    sprint_days: int = 10
) -> Tuple[List[int], List[float]]:
    """
    计算燃尽图数据

    :param total_story_points: 冲刺总故事点数
    :param daily_progress: 每日完成的故事点数列表
    :param sprint_days: 冲刺天数（默认10天）
    :return: (实际剩余点数列表, 理想剩余点数列表)
    """
    # 确保daily_progress长度不超过sprint_days
    if len(daily_progress) > sprint_days:
        daily_progress = daily_progress[:sprint_days]

    # 补齐到sprint_days长度（如果数据不足）
    while len(daily_progress) < sprint_days:
        daily_progress.append(0)

    # 计算实际剩余故事点数
    actual_remaining = [total_story_points]
    cumulative_done = 0

    for day_progress in daily_progress:
        cumulative_done += day_progress
        remaining = max(0, total_story_points - cumulative_done)
        actual_remaining.append(remaining)

    # 计算理想燃尽线（线性下降）
    ideal_remaining = []
    for day in range(sprint_days + 1):
        ideal_points = total_story_points * (1 - day / sprint_days)
        ideal_remaining.append(ideal_points)

    return actual_remaining, ideal_remaining


def generate_ascii_burndown_chart(
    actual_remaining: List[int],
    ideal_remaining: List[float],
    chart_width: int = 50,
    chart_height: int = 20
) -> str:
    """
    生成ASCII燃尽图

    :param actual_remaining: 实际剩余故事点数列表
    :param ideal_remaining: 理想剩余故事点数列表
    :param chart_width: 图表宽度
    :param chart_height: 图表高度
    :return: ASCII图表字符串
    """
    if not actual_remaining:
        return "没有数据可显示"

    max_points = max(max(actual_remaining), max(ideal_remaining))
    if max_points == 0:
        max_points = 1

    # 创建图表网格
    grid = [[' ' for _ in range(chart_width)] for _ in range(chart_height)]

    # 绘制坐标轴
    for i in range(chart_height):
        grid[i][0] = '|'
    for j in range(chart_width):
        grid[chart_height-1][j] = '-'
    grid[chart_height-1][0] = '+'

    # 绘制理想线
    for day, points in enumerate(ideal_remaining):
        x = int(day * (chart_width - 2) / (len(ideal_remaining) - 1)) + 1
        y = chart_height - 2 - int(points * (chart_height - 2) / max_points)
        if 0 <= y < chart_height - 1 and 0 <= x < chart_width:
            grid[y][x] = '.'

    # 绘制实际线
    for day, points in enumerate(actual_remaining):
        x = int(day * (chart_width - 2) / (len(actual_remaining) - 1)) + 1
        y = chart_height - 2 - int(points * (chart_height - 2) / max_points)
        if 0 <= y < chart_height - 1 and 0 <= x < chart_width:
            grid[y][x] = '*'

    # 生成图表字符串
    chart_lines = []
    for row in grid:
        chart_lines.append(''.join(row))

    # 添加图例
    chart_lines.append("")
    chart_lines.append("图例: * = 实际进度, . = 理想进度")
    chart_lines.append(f"Y轴: 剩余故事点数 (0-{int(max_points)})")
    chart_lines.append(f"X轴: 冲刺天数 (0-{len(actual_remaining)-1})")

    return '\n'.join(chart_lines)


def main():
    """主函数：演示燃尽图生成"""
    # 示例数据
    total_points = 40
    daily_done = [5, 8, 6, 4, 7, 3, 2, 1, 0, 0]  # 前10天的完成情况

    print("冲刺燃尽图演示")
    print("=" * 50)
    print(f"冲刺总故事点数: {total_points}")
    print(f"每日完成点数: {daily_done}")

    actual_remaining, ideal_remaining = calculate_burndown_data(
        total_points, daily_done, sprint_days=10
    )

    print(f"\n实际剩余点数: {actual_remaining}")
    print(f"理想剩余点数: {[round(x, 1) for x in ideal_remaining]}")

    # 生成并显示ASCII图表
    chart = generate_ascii_burndown_chart(actual_remaining, ideal_remaining)
    print("\n燃尽图:")
    print(chart)


if __name__ == "__main__":
    main()