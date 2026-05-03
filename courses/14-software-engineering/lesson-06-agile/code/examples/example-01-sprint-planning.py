#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：冲刺计划模拟
模拟冲刺规划过程：计算团队速度，根据优先级和容量选择用户故事
"""

from typing import List, Dict, Tuple


def calculate_team_velocity(completed_story_points: List[int]) -> float:
    """
    计算团队速度（平均完成的故事点数）

    :param completed_story_points: 过去几个冲刺中完成的故事点数列表
    :return: 团队平均速度
    """
    if not completed_story_points:
        return 0.0
    return sum(completed_story_points) / len(completed_story_points)


def select_user_stories_for_sprint(
    backlog: List[Dict],
    team_velocity: float,
    buffer_ratio: float = 0.2
) -> Tuple[List[Dict], float]:
    """
    根据团队速度和优先级选择冲刺中的用户故事

    :param backlog: 用户故事待办列表，每个故事包含 'id', 'title', 'story_points', 'priority'
    :param team_velocity: 团队速度（可完成的故事点数）
    :param buffer_ratio: 缓冲比例，用于应对不确定性（默认20%）
    :return: (选中的用户故事列表, 实际使用的故事点数)
    """
    # 计算实际可用容量（考虑缓冲）
    available_capacity = team_velocity * (1 - buffer_ratio)

    # 按优先级排序（优先级数字越小越重要）
    sorted_backlog = sorted(backlog, key=lambda story: story['priority'])

    selected_stories = []
    total_points = 0.0

    for story in sorted_backlog:
        # 检查是否还有足够容量
        if total_points + story['story_points'] <= available_capacity:
            selected_stories.append(story)
            total_points += story['story_points']
        else:
            # 如果当前故事太大，跳过（在实际中可能会拆分故事）
            continue

    return selected_stories, total_points


def main():
    """主函数：演示冲刺规划过程"""
    # 模拟过去3个冲刺的完成情况
    past_velocity = [25, 30, 28]  # 故事点数
    current_velocity = calculate_team_velocity(past_velocity)

    print(f"团队历史速度: {past_velocity}")
    print(f"计算出的团队速度: {current_velocity:.1f} 故事点")

    # 模拟产品待办列表
    product_backlog = [
        {'id': 'US-001', 'title': '用户登录功能', 'story_points': 8, 'priority': 1},
        {'id': 'US-002', 'title': '密码重置功能', 'story_points': 5, 'priority': 2},
        {'id': 'US-003', 'title': '用户个人资料页面', 'story_points': 13, 'priority': 3},
        {'id': 'US-004', 'title': '搜索功能优化', 'story_points': 8, 'priority': 4},
        {'id': 'US-005', 'title': '通知系统', 'story_points': 21, 'priority': 5},
        {'id': 'US-006', 'title': '数据导出功能', 'story_points': 3, 'priority': 6},
    ]

    print("\n产品待办列表:")
    for story in product_backlog:
        print(f"  {story['id']}: {story['title']} ({story['story_points']}点, 优先级{story['priority']})")

    # 选择冲刺故事
    selected_stories, used_points = select_user_stories_for_sprint(
        product_backlog, current_velocity
    )

    print(f"\n冲刺容量: {current_velocity * 0.8:.1f} 故事点 (考虑20%缓冲)")
    print(f"选中的用户故事 ({used_points:.1f} 故事点):")
    for story in selected_stories:
        print(f"  ✓ {story['id']}: {story['title']} ({story['story_points']}点)")

    remaining_capacity = current_velocity * 0.8 - used_points
    print(f"\n剩余容量: {remaining_capacity:.1f} 故事点")


if __name__ == "__main__":
    main()