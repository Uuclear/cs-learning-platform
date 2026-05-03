#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solution-02.py - SARSA vs Q-learning在悬崖行走环境中的比较

这个解决方案实现了悬崖行走（Cliff Walking）环境，并比较SARSA和Q-learning算法的性能差异。
悬崖行走是一个经典的强化学习问题，展示了on-policy和off-policy方法的不同行为。
"""

import numpy as np
import random


class CliffWalkingEnv:
    """悬崖行走环境"""

    def __init__(self):
        self.height = 4
        self.width = 12
        self.start = (3, 0)      # 起点：左下角
        self.goal = (3, 11)      # 终点：右下角
        self.cliff = {(3, i) for i in range(1, 11)}  # 悬崖位置：底部中间10格

        self.actions = ['up', 'down', 'left', 'right']
        self.action_space = len(self.actions)
        self.state_space = self.height * self.width

    def reset(self):
        """重置到起点"""
        self.current_state = self.start
        return self._state_to_index(self.current_state)

    def _state_to_index(self, state):
        """状态坐标转索引"""
        return state[0] * self.width + state[1]

    def _index_to_state(self, index):
        """索引转状态坐标"""
        return (index // self.width, index % self.width)

    def step(self, action):
        """
        执行动作并返回 (下一个状态, 奖励, 是否完成)

        奖励规则:
        - 掉入悬崖: -100
        - 到达目标: 0
        - 其他移动: -1
        """
        current_row, current_col = self.current_state

        # 计算新位置
        if action == 'up':
            new_row, new_col = max(0, current_row - 1), current_col
        elif action == 'down':
            new_row, new_col = min(self.height - 1, current_row + 1), current_col
        elif action == 'left':
            new_row, new_col = current_row, max(0, current_col - 1)
        elif action == 'right':
            new_row, new_col = current_row, min(self.width - 1, current_col + 1)
        else:
            raise ValueError(f"无效动作: {action}")

        # 更新当前状态
        self.current_state = (new_row, new_col)
        next_state_idx = self._state_to_index(self.current_state)

        # 计算奖励
        if (new_row, new_col) in self.cliff:
            # 掉入悬崖，回到起点
            self.current_state = self.start
            reward = -100
            done = False  # 在悬崖行走中，掉入悬崖不算episode结束
        elif (new_row, new_col) == self.goal:
            # 到达目标
            reward = 0
            done = True
        else:
            # 正常移动
            reward = -1
            done = False

        return next_state_idx, reward, done

    def print_env(self, agent_state=None):
        """打印环境布局"""
        grid = np.full((self.height, self.width), '.', dtype=str)

        # 标记悬崖
        for cliff_row, cliff_col in self.cliff:
            grid[cliff_row, cliff_col] = 'C'

        # 标记起点和终点
        start_row, start_col = self.start
        goal_row, goal_col = self.goal
        grid[start_row, start_col] = 'S'
        grid[goal_row, goal_col] = 'G'

        # 标记智能体位置
        if agent_state is not None:
            agent_pos = self._index_to_state(agent_state)
            if agent_pos != self.goal and agent_pos not in self.cliff:
                grid[agent_pos] = 'A'

        print("悬崖行走环境:")
        for row in grid:
            print(' '.join(row))
        print()


class QLearningAgent:
    """Q-learning智能体（off-policy）"""

    def __init__(self, state_size, action_size, learning_rate=0.1,
                 discount_factor=0.99, epsilon=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((state_size, action_size))

    def get_action(self, state, training=True):
        """ε-greedy动作选择"""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        else:
            return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        """Q-learning更新规则"""
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        target_q = reward + self.discount_factor * max_next_q
        self.q_table[state, action] += self.learning_rate * (target_q - current_q)


class SARSAAgent:
    """SARSA智能体（on-policy）"""

    def __init__(self, state_size, action_size, learning_rate=0.1,
                 discount_factor=0.99, epsilon=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((state_size, action_size))

    def get_action(self, state, training=True):
        """ε-greedy动作选择"""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        else:
            return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state, next_action):
        """SARSA更新规则"""
        current_q = self.q_table[state, action]
        next_q = self.q_table[next_state, next_action]
        target_q = reward + self.discount_factor * next_q
        self.q_table[state, action] += self.learning_rate * (target_q - current_q)


def train_agent(agent_class, env, num_episodes=500, **agent_kwargs):
    """训练指定类型的智能体"""
    agent = agent_class(
        state_size=env.state_space,
        action_size=env.action_space,
        **agent_kwargs
    )

    episode_rewards = []
    episode_steps = []

    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0.0
        steps = 0

        # 对于SARSA，需要先选择第一个动作
        if isinstance(agent, SARSAAgent):
            action = agent.get_action(state)

        for step in range(1000):  # 最大步数限制
            if isinstance(agent, QLearningAgent):
                # Q-learning: 选择动作并执行
                action = agent.get_action(state)
                next_state, reward, done = env.step(env.actions[action])
                agent.update(state, action, reward, next_state)
            else:  # SARSA
                # SARSA: 执行当前动作，然后选择下一个动作
                next_state, reward, done = env.step(env.actions[action])
                next_action = agent.get_action(next_state)
                agent.update(state, action, reward, next_state, next_action)
                action = next_action

            total_reward += reward
            steps += 1
            state = next_state

            if done:
                break

        episode_rewards.append(total_reward)
        episode_steps.append(steps)

        # 衰减epsilon
        if episode > 100:
            agent.epsilon = max(0.01, agent.epsilon * 0.99)

    return agent, episode_rewards, episode_steps


def compare_sarsa_qlearning():
    """比较SARSA和Q-learning"""
    print("=== SARSA vs Q-learning: 悬崖行走环境 ===\n")

    env = CliffWalkingEnv()
    print("环境布局:")
    env.print_env()

    # 训练Q-learning智能体
    print("训练Q-learning智能体...")
    q_agent, q_rewards, q_steps = train_agent(
        QLearningAgent,
        env,
        num_episodes=500,
        learning_rate=0.1,
        discount_factor=0.99,
        epsilon=0.1
    )

    # 训练SARSA智能体
    print("训练SARSA智能体...")
    sarsa_agent, sarsa_rewards, sarsa_steps = train_agent(
        SARSAAgent,
        env,
        num_episodes=500,
        learning_rate=0.1,
        discount_factor=0.99,
        epsilon=0.1
    )

    # 分析结果
    print("\n=== 训练结果分析 ===")

    # 计算最后100个episode的平均性能
    q_avg_reward = np.mean(q_rewards[-100:])
    q_avg_steps = np.mean(q_steps[-100:])
    sarsa_avg_reward = np.mean(sarsa_rewards[-100:])
    sarsa_avg_steps = np.mean(sarsa_steps[-100:])

    print(f"Q-learning (最后100个episode):")
    print(f"  平均奖励: {q_avg_reward:.2f}")
    print(f"  平均步数: {q_avg_steps:.1f}")

    print(f"\nSARSA (最后100个episode):")
    print(f"  平均奖励: {sarsa_avg_reward:.2f}")
    print(f"  平均步数: {sarsa_avg_steps:.1f}")

    # 演示学到的策略
    print("\n=== 策略演示 ===")

    # Q-learning策略演示
    print("Q-learning学到的路径:")
    state = env.reset()
    path = [state]
    for step in range(50):
        action = q_agent.get_action(state, training=False)
        next_state, reward, done = env.step(env.actions[action])
        path.append(next_state)
        if done:
            break
        state = next_state

    env.print_env(path[-1] if path else None)

    # SARSA策略演示
    print("SARSA学到的路径:")
    state = env.reset()
    path = [state]
    for step in range(50):
        action = sarsa_agent.get_action(state, training=False)
        next_state, reward, done = env.step(env.actions[action])
        path.append(next_state)
        if done:
            break
        state = next_state

    env.print_env(path[-1] if path else None)

    print("\n关键观察:")
    print("• Q-learning (off-policy): 学习最优策略，可能贴近悬崖但风险高")
    print("• SARSA (on-policy): 学习安全策略，远离悬崖但路径较长")
    print("• 这体现了探索策略对最终学到策略的影响")


if __name__ == "__main__":
    compare_sarsa_qlearning()