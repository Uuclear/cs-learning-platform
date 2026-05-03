#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example-01-mdp-basics.py - 实现一个简单的网格世界MDP，演示状态转移和奖励机制

这个例子展示了一个5x5的网格世界，其中：
- 智能体从左上角(0,0)开始
- 目标在右下角(4,4)，到达后获得+10奖励
- 有障碍物在特定位置，碰撞后获得-1奖励
- 每步移动获得-0.1的小惩罚（鼓励快速到达目标）
"""

import numpy as np


class GridWorldMDP:
    """简单的网格世界MDP实现"""

    def __init__(self, size=5):
        self.size = size
        self.actions = ['up', 'down', 'left', 'right']
        self.action_space = len(self.actions)
        self.state_space = size * size

        # 定义障碍物位置 (row, col)
        self.obstacles = {(2, 2), (3, 1), (1, 3)}

        # 目标位置
        self.goal = (size - 1, size - 1)

        # 当前状态
        self.current_state = (0, 0)

    def reset(self):
        """重置环境到初始状态"""
        self.current_state = (0, 0)
        return self._state_to_index(self.current_state)

    def _state_to_index(self, state):
        """将(row, col)状态转换为索引"""
        return state[0] * self.size + state[1]

    def _index_to_state(self, index):
        """将索引转换为(row, col)状态"""
        return (index // self.size, index % self.size)

    def get_possible_actions(self, state_idx):
        """获取当前状态下可能的动作"""
        row, col = self._index_to_state(state_idx)
        possible_actions = []

        if row > 0:
            possible_actions.append('up')
        if row < self.size - 1:
            possible_actions.append('down')
        if col > 0:
            possible_actions.append('left')
        if col < self.size - 1:
            possible_actions.append('right')

        return possible_actions

    def step(self, action):
        """
        执行动作并返回 (下一个状态, 奖励, 是否完成)

        参数:
            action: 动作字符串 ('up', 'down', 'left', 'right')

        返回:
            next_state_idx: 下一个状态的索引
            reward: 即时奖励
            done: 是否到达终止状态
        """
        current_row, current_col = self.current_state

        # 计算新位置
        new_row, new_col = current_row, current_col
        if action == 'up':
            new_row = max(0, current_row - 1)
        elif action == 'down':
            new_row = min(self.size - 1, current_row + 1)
        elif action == 'left':
            new_col = max(0, current_col - 1)
        elif action == 'right':
            new_col = min(self.size - 1, current_col + 1)

        # 检查是否撞到障碍物
        if (new_row, new_col) in self.obstacles:
            # 如果会撞到障碍物，保持原位置
            new_row, new_col = current_row, current_col
            reward = -1.0  # 碰撞惩罚
        elif (new_row, new_col) == self.goal:
            # 到达目标
            reward = 10.0
        else:
            # 正常移动
            reward = -0.1  # 小的移动惩罚

        # 更新当前状态
        self.current_state = (new_row, new_col)
        next_state_idx = self._state_to_index(self.current_state)
        done = (new_row, new_col) == self.goal

        return next_state_idx, reward, done

    def print_grid(self):
        """打印当前网格状态"""
        grid = np.full((self.size, self.size), '.', dtype=str)

        # 标记障碍物
        for obs_row, obs_col in self.obstacles:
            grid[obs_row, obs_col] = 'X'

        # 标记目标
        goal_row, goal_col = self.goal
        grid[goal_row, goal_col] = 'G'

        # 标记智能体当前位置
        agent_row, agent_col = self.current_state
        if (agent_row, agent_col) != self.goal:
            grid[agent_row, agent_col] = 'A'

        print("网格世界状态:")
        for row in grid:
            print(' '.join(row))
        print()


def demonstrate_mdp():
    """演示MDP的基本功能"""
    print("=== 网格世界MDP演示 ===\n")

    env = GridWorldMDP(size=5)

    # 显示初始状态
    print("初始状态:")
    env.print_grid()

    # 演示一些随机动作
    print("执行一些动作演示状态转移和奖励:\n")

    actions_sequence = ['right', 'right', 'down', 'down', 'right', 'down', 'right']

    state = env.reset()
    total_reward = 0.0

    for i, action in enumerate(actions_sequence):
        if action not in env.get_possible_actions(state):
            print(f"步骤 {i+1}: 动作 '{action}' 在当前位置不可用，跳过")
            continue

        next_state, reward, done = env.step(action)
        total_reward += reward

        print(f"步骤 {i+1}: 执行动作 '{action}'")
        print(f"  奖励: {reward:.1f}, 累计奖励: {total_reward:.1f}, 完成: {done}")
        env.print_grid()

        if done:
            print("已到达目标！")
            break

        state = next_state

    # 展示MDP的状态转移概率（确定性环境）
    print("\n=== MDP组件说明 ===")
    print(f"状态空间大小: {env.state_space}")
    print(f"动作空间大小: {env.action_space}")
    print("转移概率: 确定性环境 (P(s'|s,a) = 1.0 对于有效转移)")
    print("奖励函数: ")
    print("  - 到达目标: +10.0")
    print("  - 碰撞障碍物: -1.0")
    print("  - 正常移动: -0.1")


if __name__ == "__main__":
    demonstrate_mdp()