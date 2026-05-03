#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：工作量证明（Proof of Work）
实现PoW挖矿算法，演示难度调整机制
"""

import hashlib
import time
from typing import Optional


class ProofOfWork:
    """工作量证明类"""

    def __init__(self, difficulty: int = 4):
        """
        初始化PoW

        Args:
            difficulty: 挖矿难度，表示哈希值前导零的位数
        """
        self.difficulty = difficulty
        self.target = '0' * difficulty  # 目标哈希前缀

    def mine_block(self, block_data: str) -> tuple[str, int, float]:
        """
        挖矿函数 - 寻找满足条件的nonce值

        Args:
            block_data: 区块数据

        Returns:
            tuple: (计算出的哈希值, nonce值, 耗时)
        """
        nonce = 0
        start_time = time.time()

        print(f"⛏️  开始挖矿... 目标: 哈希值前{self.difficulty}位为0")
        print(f"🎯 目标前缀: {self.target}")

        while True:
            # 将区块数据和nonce组合后计算哈希
            data_with_nonce = f"{block_data}{nonce}"
            hash_result = hashlib.sha256(data_with_nonce.encode()).hexdigest()

            # 检查哈希是否满足目标条件
            if hash_result[:self.difficulty] == self.target:
                end_time = time.time()
                duration = end_time - start_time
                print(f"✅ 挖矿成功！")
                print(f"   Nonce: {nonce}")
                print(f"   哈希: {hash_result}")
                print(f"   耗时: {duration:.2f}秒")
                return hash_result, nonce, duration

            nonce += 1

            # 每100万次尝试显示进度（避免输出过多）
            if nonce % 1000000 == 0:
                print(f"   已尝试 {nonce} 次...")

    def adjust_difficulty(self, last_block_time: float, target_time: float = 10.0) -> int:
        """
        根据上一个区块的挖矿时间调整难度

        Args:
            last_block_time: 上一个区块的挖矿耗时（秒）
            target_time: 目标挖矿时间（秒）

        Returns:
            int: 调整后的难度
        """
        if last_block_time < target_time * 0.8:
            # 挖矿太快，增加难度
            new_difficulty = self.difficulty + 1
            print(f"📈 挖矿速度过快 ({last_block_time:.2f}s)，难度从 {self.difficulty} 增加到 {new_difficulty}")
        elif last_block_time > target_time * 1.2:
            # 挖矿太慢，降低难度
            new_difficulty = max(1, self.difficulty - 1)
            print(f"📉 挖矿速度过慢 ({last_block_time:.2f}s)，难度从 {self.difficulty} 降低到 {new_difficulty}")
        else:
            # 难度合适，保持不变
            new_difficulty = self.difficulty
            print(f"✅ 挖矿速度合适 ({last_block_time:.2f}s)，难度保持 {self.difficulty}")

        return new_difficulty


def main():
    """主函数 - 演示工作量证明挖矿"""
    print("=== 工作量证明（PoW）演示 ===\n")

    # 初始难度为4
    pow_miner = ProofOfWork(difficulty=4)

    # 模拟挖矿第一个区块
    print("📦 区块1数据: 'Alice pays Bob 10 BTC'")
    hash1, nonce1, time1 = pow_miner.mine_block("Alice pays Bob 10 BTC")

    # 根据第一个区块的挖矿时间调整难度
    print("\n🔄 调整挖矿难度...")
    new_difficulty = pow_miner.adjust_difficulty(time1)
    pow_miner.difficulty = new_difficulty
    pow_miner.target = '0' * new_difficulty

    # 挖矿第二个区块（使用新难度）
    print(f"\n📦 区块2数据: 'Charlie pays David 5 BTC' (难度: {new_difficulty})")
    hash2, nonce2, time2 = pow_miner.mine_block("Charlie pays David 5 BTC")

    # 再次调整难度
    print("\n🔄 再次调整挖矿难度...")
    final_difficulty = pow_miner.adjust_difficulty(time2)
    print(f"📊 最终难度: {final_difficulty}")

    print("\n💡 工作量证明要点:")
    print("   • 挖矿过程需要大量计算资源")
    print("   • 验证结果只需要一次哈希计算")
    print("   • 难度调整确保区块生成时间稳定")
    print("   • 攻击者需要超过50%的算力才能篡改历史")


if __name__ == "__main__":
    main()