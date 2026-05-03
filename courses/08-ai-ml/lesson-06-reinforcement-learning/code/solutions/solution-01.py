#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solution-01.py - 使用Q-learning解决CartPole-like平衡问题（使用numpy模拟）

这个解决方案实现了一个简化的CartPole环境，并使用Q-learning来学习平衡策略。
由于状态空间是连续的，我们使用状态离散化来应用表格型Q-learning。
"""

import numpy as np
import random


class CartPoleEnv:
    """简化的CartPole环境模拟器"""

    def __init__(self):
        # 物理参数
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masscart + self.masspole
        self.length = 0.5  # 杆子长度的一半
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02  # 时间步长

        # 状态边界
        self.x_threshold = 2.4
        self.theta_threshold_radians = 12 * 2 * np.pi / 360  # 12度

        # 动作：0=向左推，1=向右推
        self.action_space = 2

        # 初始状态
        self.state = None

    def reset(self):
        """重置环境到初始状态"""
        # 在小范围内随机初始化
        self.state = np.random.uniform(low=-0.05, high=0.05, size=4)
        return self._discretize_state(self.state)

    def _discretize_state(self, state):
        """
        将连续状态离散化为有限的状态索引
        状态包括：[cart_position, cart_velocity, pole_angle, pole_angular_velocity]
        """
        # 定义每个维度的离散化区间数
        bins = [10, 10, 10, 10]  # 每个维度10个区间

        # 定义每个维度的边界
        bounds = [
            (-self.x_threshold, self.x_threshold),           # cart position
            (-1.0, 1.0),                                     # cart velocity
            (-self.theta_threshold_radians, self.theta_threshold_radians),  # pole angle
            (-1.0, 1.0)                                      # pole angular velocity
        ]

        # 将每个状态分量离散化
        discretized = []
        for i, (low, high) in enumerate(bounds):
            # 处理超出边界的情况
            val = np.clip(state[i], low, high)
            # 映射到离散区间
            bin_width = (high - low) / bins[i]
            bin_idx = int((val - low) / bin_width)
            bin_idx = min(bin_idx, bins[i] - 1)  # 确保不越界
            discretized.append(bin_idx)

        # 计算唯一的状态索引
        state_idx = 0
        multiplier = 1
        for i in range(len(discretized) - 1, -1, -1):
            state_idx += discretized[i] * multiplier
            multiplier *= bins[i]

        return state_idx

    def step(self, action):
        """
        执行动作并返回下一个状态、奖励和是否完成

        参数:
            action: 0 (向左) 或 1 (向右)

        返回:
            next_state_idx: 离散化的下一个状态索引
            reward: 奖励 (1.0 如果未失败，0.0 如果失败)
            done: 是否失败（小车超出范围或杆子倒下）
        """
        x, x_dot, theta, theta_dot = self.state

        # 应用力
        force = self.force_mag if action == 1 else -self.force_mag

        # 计算加速度（来自物理方程）
        costheta = np.cos(theta)
        sintheta = np.sin(theta)

        temp = (force + self.polemass_length * theta_dot ** 2 * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.masspole * costheta ** 2 / self.total_mass)
        )
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        # 更新状态（欧拉积分）
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc

        self.state = np.array([x, x_dot, theta, theta_dot])

        # 检查是否失败
        done = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        # 奖励：只要没失败就给1.0
        reward = 1.0 if not done else 0.0

        next_state_idx = self._discretize_state(self.state)
        return next_state_idx, reward, done


class QLearningAgent:
    """Q-learning智能体用于CartPole"""

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

    def update_q_value(self, state, action, reward, next_state):
        """更新Q值"""
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        target_q = reward + self.discount_factor * max_next_q
        self.q_table[state, action] += self.learning_rate * (target_q - current_q)


def solve_cartpole():
    """使用Q-learning解决CartPole问题"""
    print("=== CartPole平衡问题Q-learning解决方案 ===\n")

    # 创建环境
    env = CartPoleEnv()

    # 计算状态空间大小（基于离散化）
    state_bins = [10, 10, 10, 10]
    state_size = np.prod(state_bins)
    action_size = env.action_space

    print(f"离散化后的状态空间大小: {state_size}")
    print(f"动作空间大小: {action_size}\n")

    # 创建智能体
    agent = QLearningAgent(
        state_size=state_size,
        action_size=action_size,
        learning_rate=0.2,
        discount_factor=0.99,
        epsilon=0.1
    )

    # 训练参数
    num_episodes = 2000
    max_steps = 200

    episode_rewards = []
    episode_lengths = []

    print("开始训练...")
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0.0
        steps = 0

        for step in range(max_steps):
            # 选择动作
            action = agent.get_action(state)

            # 执行动作
            next_state, reward, done = env.step(action)

            # 更新Q值
            agent.update_q_value(state, action, reward, next_state)

            total_reward += reward
            steps += 1
            state = next_state

            if done:
                break

        episode_rewards.append(total_reward)
        episode_lengths.append(steps)

        # 衰减epsilon（减少探索）
        if episode > 1000:
            agent.epsilon = max(0.01, agent.epsilon * 0.995)

        # 每200个episode打印进度
        if (episode + 1) % 200 == 0:
            avg_reward = np.mean(episode_rewards[-200:])
            avg_length = np.mean(episode_lengths[-200:])
            print(f"Episode {episode + 1}: 平均奖励 = {avg_reward:.1f}, "
                  f"平均步数 = {avg_length:.1f}, epsilon = {agent.epsilon:.3f}")

    # 测试学到的策略
    print(f"\n训练完成！测试最终策略...")
    test_rewards = []
    test_lengths = []

    for test_episode in range(10):
        state = env.reset()
        total_reward = 0.0
        steps = 0

        for step in range(500):  # 测试时允许更长的episode
            action = agent.get_action(state, training=False)
            next_state, reward, done = env.step(action)

            total_reward += reward
            steps += 1
            state = next_state

            if done:
                break

        test_rewards.append(total_reward)
        test_lengths.append(steps)

    print(f"测试结果 (10次运行):")
    print(f"平均奖励: {np.mean(test_rewards):.1f}")
    print(f"平均步数: {np.mean(test_lengths):.1f}")
    print(f"最大步数: {np.max(test_lengths)}")

    # 成功标准：能够持续平衡200步以上
    success_rate = np.mean(np.array(test_lengths) >= 200)
    print(f"成功率 (≥200步): {success_rate * 100:.1f}%")


if __name__ == "__main__":
    solve_cartpole()