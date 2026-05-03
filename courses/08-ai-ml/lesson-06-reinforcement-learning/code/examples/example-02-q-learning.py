#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example-02-q-learning.py - Q-learning算法解决迷宫问题，打印学习进度

这个例子实现了完整的Q-learning算法来解决网格世界迷宫问题。
通过迭代学习，智能体逐步找到从起点到目标的最优路径。
"""

import numpy as np
import random


class MazeEnvironment:
    """迷宫环境类"""

    def __init__(self, size=5):
        self.size = size
        self.actions = ['up', 'down', 'left', 'right']
        self.action_to_idx = {action: idx for idx, action in enumerate(self.actions)}

        # 障碍物位置
        self.obstacles = {(1, 1), (2, 1), (3, 1), (1, 3), (2, 3), (3, 3)}
        self.start = (0, 0)
        self.goal = (size - 1, size - 1)
        self.current_state = self.start

    def reset(self):
        """重置到起始状态"""
        self.current_state = self.start
        return self._state_to_index(self.current_state)

    def _state_to_index(self, state):
        """状态坐标转索引"""
        return state[0] * self.size + state[1]

    def _index_to_state(self, index):
        """索引转状态坐标"""
        return (index // self.size, index % self.size)

    def is_valid_position(self, row, col):
        """检查位置是否有效（不在障碍物上且在边界内）"""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        if (row, col) in self.obstacles:
            return False
        return True

    def get_next_state(self, state, action):
        """获取执行动作后的下一个状态"""
        row, col = self._index_to_state(state)

        if action == 'up':
            new_row, new_col = row - 1, col
        elif action == 'down':
            new_row, new_col = row + 1, col
        elif action == 'left':
            new_row, new_col = row, col - 1
        elif action == 'right':
            new_row, new_col = row, col + 1
        else:
            raise ValueError(f"无效的动作: {action}")

        # 如果新位置无效，保持原位置
        if self.is_valid_position(new_row, new_col):
            return self._state_to_index((new_row, new_col))
        else:
            return state

    def get_reward(self, state, action, next_state):
        """获取奖励"""
        if self._index_to_state(next_state) == self.goal:
            return 10.0  # 到达目标
        elif next_state == state:
            return -1.0  # 撞墙或障碍物
        else:
            return -0.1  # 正常移动惩罚

    def is_terminal(self, state):
        """检查是否为终止状态"""
        return self._index_to_state(state) == self.goal

    def print_maze(self, agent_state=None):
        """打印迷宫"""
        grid = np.full((self.size, self.size), '.', dtype=str)

        # 标记障碍物
        for obs in self.obstacles:
            grid[obs] = 'X'

        # 标记起点和终点
        grid[self.start] = 'S'
        grid[self.goal] = 'G'

        # 标记智能体位置
        if agent_state is not None:
            agent_pos = self._index_to_state(agent_state)
            if agent_pos != self.goal:
                grid[agent_pos] = 'A'

        print("迷宫布局:")
        for row in grid:
            print(' '.join(row))
        print()


class QLearningAgent:
    """Q-learning智能体"""

    def __init__(self, state_size, action_size, learning_rate=0.1,
                 discount_factor=0.95, epsilon=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        # 初始化Q表
        self.q_table = np.zeros((state_size, action_size))

    def get_action(self, state, training=True):
        """根据ε-greedy策略选择动作"""
        if training and random.random() < self.epsilon:
            # 探索：随机选择动作
            return random.randint(0, self.action_size - 1)
        else:
            # 利用：选择Q值最大的动作
            return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        """更新Q值"""
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        target_q = reward + self.discount_factor * max_next_q
        self.q_table[state, action] += self.learning_rate * (target_q - current_q)


def train_q_learning():
    """训练Q-learning智能体"""
    print("=== Q-learning 迷宫求解 ===\n")

    # 创建环境和智能体
    env = MazeEnvironment(size=5)
    agent = QLearningAgent(
        state_size=env.size * env.size,
        action_size=len(env.actions),
        learning_rate=0.1,
        discount_factor=0.95,
        epsilon=0.1
    )

    print("迷宫初始布局:")
    env.print_maze()

    # 训练参数
    num_episodes = 200
    max_steps = 100

    episode_rewards = []
    episode_steps = []

    print("开始训练...")
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0.0
        steps = 0

        for step in range(max_steps):
            # 选择动作
            action_idx = agent.get_action(state)
            action = env.actions[action_idx]

            # 执行动作
            next_state = env.get_next_state(state, action)
            reward = env.get_reward(state, action, next_state)
            done = env.is_terminal(next_state)

            # 更新Q值
            agent.update_q_value(state, action_idx, reward, next_state)

            total_reward += reward
            steps += 1
            state = next_state

            if done:
                break

        episode_rewards.append(total_reward)
        episode_steps.append(steps)

        # 每50个episode打印一次进度
        if (episode + 1) % 50 == 0:
            avg_reward = np.mean(episode_rewards[-50:])
            avg_steps = np.mean(episode_steps[-50:])
            print(f"Episode {episode + 1}: 平均奖励 = {avg_reward:.2f}, "
                  f"平均步数 = {avg_steps:.1f}")

    print(f"\n训练完成！最终50个episode的平均性能:")
    print(f"平均奖励: {np.mean(episode_rewards[-50:]):.2f}")
    print(f"平均步数: {np.mean(episode_steps[-50:]):.1f}")

    # 演示学到的策略
    print("\n=== 学到的最优策略演示 ===")
    state = env.reset()
    path = [state]

    for step in range(50):  # 最多50步防止无限循环
        action_idx = agent.get_action(state, training=False)  # 关闭探索
        action = env.actions[action_idx]
        next_state = env.get_next_state(state, action)

        print(f"步骤 {step + 1}: 状态 {state} -> 动作 '{action}' -> 状态 {next_state}")
        path.append(next_state)

        if env.is_terminal(next_state):
            print("成功到达目标！")
            break

        state = next_state
    else:
        print("未能在50步内到达目标")

    # 显示最终路径
    print("\n最终学到的Q值表（部分）:")
    for i in range(0, min(10, agent.q_table.shape[0])):
        print(f"状态 {i}: {agent.q_table[i]}")


if __name__ == "__main__":
    train_q_learning()