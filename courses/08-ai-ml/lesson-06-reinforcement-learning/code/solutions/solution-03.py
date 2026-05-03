#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solution-03.py - 构建简单的多臂老虎机模拟器，比较探索策略

这个解决方案实现了一个完整的多臂老虎机模拟器，并系统性地比较
epsilon-greedy、softmax和UCB三种探索策略在不同场景下的表现。
"""

import numpy as np
import random
from collections import defaultdict


class MultiArmedBandit:
    """多臂老虎机环境"""

    def __init__(self, num_arms=10, reward_std=1.0):
        self.num_arms = num_arms
        self.reward_std = reward_std
        # 真实的臂价值（均值）
        self.true_values = np.random.normal(0, 1, num_arms)

    def pull_arm(self, arm):
        """拉动指定的臂，返回奖励"""
        if arm < 0 or arm >= self.num_arms:
            raise ValueError(f"臂索引 {arm} 超出范围 [0, {self.num_arms-1}]")
        return np.random.normal(self.true_values[arm], self.reward_std)

    def get_optimal_arm(self):
        """返回最优臂的索引"""
        return np.argmax(self.true_values)


class EpsilonGreedyAgent:
    """ε-greedy智能体"""

    def __init__(self, num_arms, epsilon=0.1):
        self.num_arms = num_arms
        self.epsilon = epsilon
        self.q_values = np.zeros(num_arms)
        self.action_counts = np.zeros(num_arms)

    def select_action(self):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.q_values)

    def update(self, action, reward):
        self.action_counts[action] += 1
        self.q_values[action] += (reward - self.q_values[action]) / self.action_counts[action]

    def get_name(self):
        return f"ε-greedy (ε={self.epsilon})"


class SoftmaxAgent:
    """Softmax智能体"""

    def __init__(self, num_arms, temperature=1.0):
        self.num_arms = num_arms
        self.temperature = temperature
        self.q_values = np.zeros(num_arms)
        self.action_counts = np.zeros(num_arms)

    def select_action(self):
        exp_values = np.exp(self.q_values / self.temperature)
        probabilities = exp_values / np.sum(exp_values)
        return np.random.choice(self.num_arms, p=probabilities)

    def update(self, action, reward):
        self.action_counts[action] += 1
        self.q_values[action] += (reward - self.q_values[action]) / self.action_counts[action]

    def get_name(self):
        return f"Softmax (T={self.temperature})"


class UCB1Agent:
    """UCB1智能体"""

    def __init__(self, num_arms, c=2.0):
        self.num_arms = num_arms
        self.c = c
        self.q_values = np.zeros(num_arms)
        self.action_counts = np.zeros(num_arms)
        self.total_counts = 0

    def select_action(self):
        if self.total_counts < self.num_arms:
            return self.total_counts

        ucb_values = self.q_values + self.c * np.sqrt(
            np.log(self.total_counts) / (self.action_counts + 1e-8)
        )
        return np.argmax(ucb_values)

    def update(self, action, reward):
        self.action_counts[action] += 1
        self.total_counts += 1
        self.q_values[action] += (reward - self.q_values[action]) / self.action_counts[action]

    def get_name(self):
        return f"UCB1 (c={self.c})"


def run_single_experiment(agent_class, bandit_params, agent_params, num_steps=1000):
    """运行单次实验"""
    bandit = MultiArmedBandit(**bandit_params)
    agent = agent_class(bandit.num_arms, **agent_params)

    rewards = []
    optimal_actions = []
    optimal_arm = bandit.get_optimal_arm()

    for step in range(num_steps):
        action = agent.select_action()
        reward = bandit.pull_arm(action)
        agent.update(action, reward)

        rewards.append(reward)
        optimal_actions.append(1 if action == optimal_arm else 0)

    return {
        'rewards': np.array(rewards),
        'optimal_actions': np.array(optimal_actions),
        'agent_name': agent.get_name(),
        'true_values': bandit.true_values.copy()
    }


def compare_strategies_systematic():
    """系统性比较不同探索策略"""
    print("=== 多臂老虎机探索策略系统性比较 ===\n")

    # 实验配置
    num_arms = 10
    num_steps = 1000
    num_runs = 500

    bandit_params = {'num_arms': num_arms, 'reward_std': 1.0}

    # 定义要测试的策略和参数
    strategies = [
        # ε-greedy with different epsilons
        (EpsilonGreedyAgent, {'epsilon': 0.01}, "低探索"),
        (EpsilonGreedyAgent, {'epsilon': 0.1}, "中等探索"),
        (EpsilonGreedyAgent, {'epsilon': 0.3}, "高探索"),

        # Softmax with different temperatures
        (SoftmaxAgent, {'temperature': 0.5}, "低温度"),
        (SoftmaxAgent, {'temperature': 1.0}, "中等温度"),
        (SoftmaxAgent, {'temperature': 2.0}, "高温度"),

        # UCB1 with different c values
        (UCB1Agent, {'c': 1.0}, "保守UCB"),
        (UCB1Agent, {'c': 2.0}, "标准UCB"),
        (UCB1Agent, {'c': 4.0}, "激进UCB")
    ]

    print(f"实验设置:")
    print(f"- 臂数量: {num_arms}")
    print(f"- 步数: {num_steps}")
    print(f"- 运行次数: {num_runs}")
    print(f"- 奖励标准差: {bandit_params['reward_std']}\n")

    results = {}

    for agent_class, agent_params, label in strategies:
        print(f"运行 {agent_class.__name__} {label} ...")

        all_rewards = []
        all_optimal = []

        for run in range(num_runs):
            result = run_single_experiment(
                agent_class, bandit_params, agent_params, num_steps
            )
            all_rewards.append(result['rewards'])
            all_optimal.append(result['optimal_actions'])

        avg_rewards = np.mean(all_rewards, axis=0)
        avg_optimal = np.mean(all_optimal, axis=0)

        total_reward = np.sum(avg_rewards)
        final_optimal_rate = np.mean(avg_optimal[-100:])  # 最后100步的最优选择率

        results[f"{result['agent_name']} ({label})"] = {
            'total_reward': total_reward,
            'final_optimal_rate': final_optimal_rate,
            'avg_rewards': avg_rewards,
            'avg_optimal': avg_optimal
        }

    # 打印详细结果
    print("\n=== 详细结果 ===")
    print(f"{'策略':<25} {'总奖励':<10} {'最终最优率':<12}")
    print("-" * 45)

    sorted_results = sorted(results.items(), key=lambda x: x[1]['total_reward'], reverse=True)

    for name, metrics in sorted_results:
        print(f"{name:<25} {metrics['total_reward']:<10.1f} "
              f"{metrics['final_optimal_rate']*100:<11.1f}%")

    # 分析不同场景
    print("\n=== 场景分析 ===")

    # 找出最佳策略
    best_strategy = sorted_results[0][0]
    best_total_reward = sorted_results[0][1]['total_reward']
    print(f"最佳策略: {best_strategy}")
    print(f"最佳总奖励: {best_total_reward:.1f}")

    # 分析探索强度的影响
    print("\n探索强度影响:")
    epsilon_strategies = [name for name in results.keys() if 'ε-greedy' in name]
    if epsilon_strategies:
        epsilon_results = [(name, results[name]) for name in epsilon_strategies]
        epsilon_results.sort(key=lambda x: float(x[0].split('ε=')[1].split(')')[0]))
        print("ε-greedy性能随ε变化:")
        for name, metrics in epsilon_results:
            epsilon_val = float(name.split('ε=')[1].split(')')[0])
            print(f"  ε={epsilon_val}: 总奖励={metrics['total_reward']:.1f}")

    # 讨论实际应用建议
    print("\n=== 实际应用建议 ===")
    print("1. 如果环境稳定且需要快速收敛，使用较低的探索率")
    print("2. 如果环境可能变化或存在多个局部最优，保持较高的探索率")
    print("3. UCB1在理论上有保证，但在实践中需要调整参数c")
    print("4. Softmax提供了更平滑的探索-利用权衡")
    print("5. 最佳策略通常取决于具体问题的特性")


if __name__ == "__main__":
    compare_strategies_systematic()