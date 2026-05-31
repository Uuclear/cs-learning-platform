#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：区块链基础结构
演示区块链接、哈希链和篡改检测机制
"""

import hashlib
import time
from typing import List, Dict, Any


class Block:
    """区块类 - 区块链的基本单元"""

    def __init__(self, index: int, transactions: List[Dict[str, Any]],
                 previous_hash: str, timestamp: float = None):
        """
        初始化区块

        Args:
            index: 区块在链中的位置
            transactions: 区块包含的交易列表
            previous_hash: 前一个区块的哈希值
            timestamp: 时间戳，默认为当前时间
        """
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        计算区块的哈希值
        将区块的所有关键信息组合后进行SHA256哈希
        """
        block_string = f"{self.index}{self.transactions}{self.previous_hash}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __str__(self) -> str:
        """返回区块的字符串表示"""
        return f"区块 #{self.index} | 哈希: {self.hash[:8]}... | 交易数: {len(self.transactions)}"


class Blockchain:
    """简易区块链类"""

    def __init__(self):
        """初始化区块链，创建创世区块"""
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """创建创世区块（第一个区块）"""
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)
        print(f"✅ 创建创世区块: {genesis_block}")

    def get_latest_block(self) -> Block:
        """获取最新的区块"""
        return self.chain[-1]

    def add_block(self, transactions: List[Dict[str, Any]]):
        """
        添加新区块到区块链

        Args:
            transactions: 要包含在新区块中的交易列表
        """
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            transactions=transactions,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)
        print(f"✅ 添加新区块: {new_block}")

    def is_chain_valid(self) -> bool:
        """
        验证区块链的完整性
        检查每个区块的哈希是否正确，以及是否正确链接到前一个区块
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 验证当前区块的哈希是否正确
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ 区块 #{current_block.index} 的哈希值不正确！")
                return False

            # 验证当前区块是否正确链接到前一个区块
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ 区块 #{current_block.index} 的前一区块哈希不匹配！")
                return False

        print("✅ 区块链验证通过！所有区块完整且未被篡改。")
        return True

    def tamper_block(self, index: int, new_transactions: List[Dict[str, Any]]):
        """
        模拟篡改区块（仅用于演示）

        Args:
            index: 要篡改的区块索引
            new_transactions: 新的交易数据
        """
        if 0 <= index < len(self.chain):
            self.chain[index].transactions = new_transactions
            # 注意：这里没有重新计算哈希，模拟恶意篡改
            print(f"⚠️  模拟篡改区块 #{index} 的交易数据")


def main():
    """主函数 - 演示区块链的基本功能"""
    print("=== 区块链基础演示 ===\n")

    # 创建区块链
    blockchain = Blockchain()

    # 添加一些交易区块
    print("\n📝 添加交易区块...")
    blockchain.add_block([
        {"sender": "Alice", "receiver": "Bob", "amount": 10},
        {"sender": "Charlie", "receiver": "David", "amount": 5}
    ])

    blockchain.add_block([
        {"sender": "Eve", "receiver": "Frank", "amount": 15}
    ])

    # 验证区块链
    print("\n🔍 验证区块链完整性...")
    blockchain.is_chain_valid()

    # 演示篡改检测
    print("\n🎭 模拟篡改攻击...")
    blockchain.tamper_block(1, [{"sender": "Hacker", "receiver": "Thief", "amount": 100}])

    print("\n🔍 再次验证区块链完整性（预期失败：篡改后哈希不匹配）...")
    if not blockchain.is_chain_valid():
        print("✅ 篡改已被检测到 — 这正是区块链防篡改的核心机制！")


if __name__ == "__main__":
    main()