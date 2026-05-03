#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：冲刺计划实现
"""

from typing import List, Dict, Tuple


def calculate_team_velocity(completed_story_points: List[int]) -> float:
    if not completed_story_points:
        return 0.0
    return sum(completed_story_points) / len(completed_story_points)


def select_user_stories_for_sprint(
    backlog: List[Dict],
    team_velocity: float,
    buffer_ratio: float = 0.2
) -> Tuple[List[Dict], float]:
    available_capacity = team_velocity * (1 - buffer_ratio)
    sorted_backlog = sorted(backlog, key=lambda story: story['priority'])

    selected_stories = []
    total_points = 0.0

    for story in sorted_backlog:
        if total_points + story['story_points'] <= available_capacity:
            selected_stories.append(story)
            total_points += story['story_points']

    return selected_stories, total_points