#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：共识机制模拟器
比较工作量证明（PoW）和权益证明（PoS）
"""

import hashlib
import random
import time
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Node:
    """网络节点类"""
    name: str
    computing_power: float  # 计算能力（用于PoW）
    stake: float           # 质押代币数量（用于PoS）
    blocks_mined: int = 0


class ConsensusSimulator:
    """共识机制模拟器"""

    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.blockchain = []  # 简化的区块链，只记录谁挖出了区块

    def simulate_pow(self, num_blocks: int = 10) -> Dict[str, Any]:
        """
        模拟工作量证明共识

        Args:
            num_blocks: 要模拟的区块数量

        Returns:
            Dict: 模拟结果统计
        """
        print(f"⛏️  开始PoW模拟 ({num_blocks} 个区块)...")

        # 重置节点统计
        for node in self.nodes:
            node.blocks_mined = 0

        start_time = time.time()

        for block_num in range(num_blocks):
            # 根据计算能力选择获胜者（概率与计算能力成正比）
            total_power = sum(node.computing_power for node in self.nodes)
            rand_value = random.uniform(0, total_power)

            cumulative_power = 0
            winner = None
            for node in self.nodes:
                cumulative_power += node.computing_power
                if rand_value <= cumulative_power:
                    winner = node
                    break

            if winner:
                winner.blocks_mined += 1
                self.blockchain.append(winner.name)

                # 模拟挖矿时间（基于计算能力）
                mining_time = random.expovariate(winner.computing_power)
                time.sleep(min(mining_time * 0.1, 0.01))  # 缩短等待时间用于演示

        end_time = time.time()

        # 统计结果
        results = {
            "consensus_type": "Proof of Work (PoW)",
            "total_blocks": num_blocks,
            "simulation_time": end_time - start_time,
            "node_stats": []
        }

        for node in self.nodes:
            percentage = (node.blocks_mined / num_blocks) * 100
            results["node_stats"].append({
                "name": node.name,
                "blocks_mined": node.blocks_mined,
                "percentage": percentage,
                "computing_power": node.computing_power
            })

        return results

    def simulate_pos(self, num_blocks: int = 10) -> Dict[str, Any]:
        """
        模拟权益证明共识

        Args:
            num_blocks: 要模拟的区块数量

        Returns:
            Dict: 模拟结果统计
        """
        print(f"💰 开始PoS模拟 ({num_blocks} 个区块)...")

        # 重置节点统计
        for node in self.nodes:
            node.blocks_mined = 0

        start_time = time.time()

        for block_num in range(num_blocks):
            # 根据质押代币数量选择获胜者（概率与质押数量成正比）
            total_stake = sum(node.stake for node in self.nodes)
            if total_stake == 0:
                # 如果没有质押，随机选择
                winner = random.choice(self.nodes)
            else:
                rand_value = random.uniform(0, total_stake)

                cumulative_stake = 0
                winner = None
                for node in self.nodes:
                    cumulative_stake += node.stake
                    if rand_value <= cumulative_stake:
                        winner = node
                        break

                if winner is None:
                    winner = random.choice(self.nodes)

            winner.blocks_mined += 1
            self.blockchain.append(winner.name)

            # PoS验证更快，所以等待时间更短
            time.sleep(0.005)

        end_time = time.time()

        # 统计结果
        results = {
            "consensus_type": "Proof of Stake (PoS)",
            "total_blocks": num_blocks,
            "simulation_time": end_time - start_time,
            "node_stats": []
        }

        for node in self.nodes:
            percentage = (node.blocks_mined / num_blocks) * 100
            results["node_stats"].append({
                "name": node.name,
                "blocks_mined": node.blocks_mined,
                "percentage": percentage,
                "stake": node.stake
            })

        return results

    def display_results(self, results: Dict[str, Any]):
        """显示模拟结果"""
        print(f"\n📊 {results['consensus_type']} 模拟结果:")
        print(f"   总区块数: {results['total_blocks']}")
        print(f"   模拟耗时: {results['simulation_time']:.3f}秒")
        print(f"\n   节点表现:")

        for stat in results["node_stats"]:
            if "computing_power" in stat:
                extra_info = f"(计算力: {stat['computing_power']:.2f})"
            else:
                extra_info = f"(质押: {stat['stake']:.2f})"

            print(f"     • {stat['name']}: {stat['blocks_mined']} 区块 "
                  f"({stat['percentage']:.1f}%) {extra_info}")


def main():
    """主函数 - 运行共识机制比较"""
    print("=== 共识机制模拟器 ===\n")

    # 创建网络节点
    nodes = [
        Node("Alice", computing_power=3.0, stake=100.0),
        Node("Bob", computing_power=5.0, stake=200.0),
        Node("Charlie", computing_power=2.0, stake=50.0),
        Node("Diana", computing_power=4.0, stake=150.0)
    ]

    print("🌐 网络节点配置:")
    for node in nodes:
        print(f"   • {node.name}: 计算力={node.computing_power}, 质押={node.stake}")

    # 创建模拟器
    simulator = ConsensusSimulator(nodes)

    # 运行PoW模拟
    print("\n" + "="*50)
    pow_results = simulator.simulate_pow(num_blocks=20)
    simulator.display_results(pow_results)

    # 运行PoS模拟
    print("\n" + "="*50)
    pos_results = simulator.simulate_pos(num_blocks=20)
    simulator.display_results(pos_results)

    # 比较分析
    print("\n" + "="*50)
    print("🔍 共识机制对比分析:")

    # 计算集中度（使用简单的基尼系数近似）
    def calculate_concentration(blocks_list: List[int]) -> float:
        total = sum(blocks_list)
        if total == 0:
            return 0.0
        proportions = [b/total for b in blocks_list]
        return max(proportions)  # 最大占比作为集中度指标

    pow_concentration = calculate_concentration([s["blocks_mined"] for s in pow_results["node_stats"]])
    pos_concentration = calculate_concentration([s["blocks_mined"] for s in pos_results["node_stats"]])

    print(f"   • PoW 集中度: {pow_concentration:.2f}")
    print(f"   • PoS 集中度: {pos_concentration:.2f}")

    print(f"\n💡 关键差异:")
    print(f"   • PoW: 基于计算能力，能源消耗大，安全性高")
    print(f"   • PoS: 基于质押代币，节能环保，但可能导致富者愈富")
    print(f"   • 两种机制都有各自的权衡和适用场景")


if __name__ == "__main__":
    main()