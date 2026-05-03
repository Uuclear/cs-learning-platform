#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：完整的简易区块链实现
包含交易、挖矿和验证功能
"""

import hashlib
import time
import json
from typing import List, Dict, Any, Optional


class Transaction:
    """交易类"""

    def __init__(self, sender: str, receiver: str, amount: float, timestamp: float = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

    def __str__(self) -> str:
        return f"{self.sender} → {self.receiver}: {self.amount}"


class Block:
    """区块类"""

    def __init__(self, index: int, transactions: List[Transaction],
                 previous_hash: str, nonce: int = 0, timestamp: float = None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """计算区块哈希"""
        # 将交易转换为字典列表以便序列化
        transactions_data = [tx.to_dict() for tx in self.transactions]
        block_string = json.dumps({
            "index": self.index,
            "transactions": transactions_data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> float:
        """
        挖矿函数

        Args:
            difficulty: 挖矿难度

        Returns:
            float: 挖矿耗时（秒）
        """
        target = '0' * difficulty
        start_time = time.time()

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        end_time = time.time()
        return end_time - start_time

    def has_valid_transactions(self) -> bool:
        """验证区块内所有交易的有效性"""
        # 简单验证：检查交易金额是否为正数
        for tx in self.transactions:
            if tx.amount <= 0:
                return False
        return True


class Blockchain:
    """完整区块链实现"""

    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """创建创世区块"""
        genesis_block = Block(0, [], "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """获取最新区块"""
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """添加交易到待处理列表"""
        # 基本验证
        if not transaction.sender or not transaction.receiver:
            raise ValueError("交易必须包含发送方和接收方")
        if transaction.amount <= 0:
            raise ValueError("交易金额必须大于0")

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str) -> float:
        """
        挖掘待处理交易

        Args:
            miner_address: 矿工地址（用于接收奖励）

        Returns:
            float: 挖矿耗时
        """
        # 添加矿工奖励交易
        reward_tx = Transaction("SYSTEM", miner_address, 1.0)
        block_transactions = self.pending_transactions + [reward_tx]

        # 创建新区块
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            transactions=block_transactions,
            previous_hash=latest_block.hash
        )

        # 挖矿
        mining_time = new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        # 清空待处理交易
        self.pending_transactions = []

        return mining_time

    def is_chain_valid(self) -> bool:
        """验证整个区块链的有效性"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 验证当前区块哈希
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ 区块 {current_block.index} 哈希无效")
                return False

            # 验证前一区块哈希链接
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ 区块 {current_block.index} 前一哈希链接无效")
                return False

            # 验证区块内交易
            if not current_block.has_valid_transactions():
                print(f"❌ 区块 {current_block.index} 包含无效交易")
                return False

            # 验证工作量证明
            target = '0' * self.difficulty
            if current_block.hash[:self.difficulty] != target:
                print(f"❌ 区块 {current_block.index} 工作量证明无效")
                return False

        return True

    def get_balance(self, address: str) -> float:
        """获取地址余额（简化版，仅遍历链上交易）"""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance


def main():
    """主函数 - 演示完整区块链功能"""
    print("=== 完整区块链演示 ===\n")

    # 创建区块链（难度设为3以加快演示速度）
    blockchain = Blockchain(difficulty=3)

    print("👤 创建用户: Alice, Bob, Charlie")
    print("💰 初始余额都为0\n")

    # 添加一些交易
    print("📝 添加交易...")
    blockchain.add_transaction(Transaction("Alice", "Bob", 10))
    blockchain.add_transaction(Transaction("Bob", "Charlie", 5))

    # 挖掘交易
    print("⛏️  开始挖矿...")
    mining_time = blockchain.mine_pending_transactions("Miner1")
    print(f"✅ 挖矿完成！耗时: {mining_time:.2f}秒")

    # 添加更多交易
    print("\n📝 添加更多交易...")
    blockchain.add_transaction(Transaction("Charlie", "Alice", 3))
    blockchain.add_transaction(Transaction("Alice", "Charlie", 7))

    print("⛏️  再次挖矿...")
    mining_time = blockchain.mine_pending_transactions("Miner2")
    print(f"✅ 挖矿完成！耗时: {mining_time:.2f}秒")

    # 验证区块链
    print(f"\n🔍 验证区块链完整性: {'✅ 有效' if blockchain.is_chain_valid() else '❌ 无效'}")

    # 显示余额
    print("\n💰 账户余额:")
    print(f"   Alice: {blockchain.get_balance('Alice')}")
    print(f"   Bob: {blockchain.get_balance('Bob')}")
    print(f"   Charlie: {blockchain.get_balance('Charlie')}")
    print(f"   Miner1: {blockchain.get_balance('Miner1')}")
    print(f"   Miner2: {blockchain.get_balance('Miner2')}")

    # 显示区块链信息
    print(f"\n📊 区块链统计:")
    print(f"   总区块数: {len(blockchain.chain)}")
    print(f"   总交易数: {sum(len(block.transactions) for block in blockchain.chain)}")


if __name__ == "__main__":
    main()