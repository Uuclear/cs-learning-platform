#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：默克尔树（Merkle Tree）
构建默克尔树并演示数据完整性验证
"""

import hashlib
from typing import List, Optional


def hash_data(data: str) -> str:
    """对数据进行SHA256哈希"""
    return hashlib.sha256(data.encode()).hexdigest()


class MerkleTree:
    """默克尔树实现"""

    def __init__(self, transactions: List[str]):
        """
        初始化默克尔树

        Args:
            transactions: 交易数据列表
        """
        self.transactions = [hash_data(tx) for tx in transactions]  # 先对所有交易哈希
        self.tree = self.build_tree()

    def build_tree(self) -> List[List[str]]:
        """
        构建默克尔树
        返回一个二维列表，每层包含该层的所有哈希值
        """
        if not self.transactions:
            return []

        tree = [self.transactions.copy()]  # 第0层是叶子节点（交易哈希）

        # 逐层向上构建
        current_level = self.transactions
        while len(current_level) > 1:
            next_level = []
            # 处理成对的哈希值
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # 如果是奇数个，最后一个节点与自己配对
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                # 组合左右哈希并再次哈希
                combined = left + right
                parent_hash = hash_data(combined)
                next_level.append(parent_hash)
            tree.append(next_level)
            current_level = next_level

        return tree

    def get_root(self) -> Optional[str]:
        """获取默克尔根（树顶哈希）"""
        if not self.tree:
            return None
        return self.tree[-1][0]

    def get_merkle_proof(self, transaction_index: int) -> List[tuple[str, str]]:
        """
        获取指定交易的默克尔证明路径

        Args:
            transaction_index: 交易在原始列表中的索引

        Returns:
            List[tuple]: 证明路径，每个元素包含(兄弟哈希, 方向)
        """
        if transaction_index >= len(self.transactions):
            raise IndexError("交易索引超出范围")

        proof = []
        index = transaction_index
        hash_value = self.transactions[index]

        # 从叶子节点向上遍历到根节点
        for level in range(len(self.tree) - 1):
            current_level = self.tree[level]
            # 确定当前节点在父级中的位置
            is_left = (index % 2 == 0)
            if is_left:
                # 当前是左节点，需要右兄弟
                sibling_index = index + 1
                if sibling_index < len(current_level):
                    sibling_hash = current_level[sibling_index]
                else:
                    # 奇数情况下，右兄弟就是自己
                    sibling_hash = current_level[index]
                proof.append((sibling_hash, "right"))
            else:
                # 当前是右节点，需要左兄弟
                sibling_hash = current_level[index - 1]
                proof.append((sibling_hash, "left"))

            # 移动到父级
            index = index // 2

        return proof

    def verify_transaction(self, transaction: str, proof: List[tuple[str, str]]) -> bool:
        """
        验证交易是否存在于默克尔树中

        Args:
            transaction: 要验证的交易数据
            proof: 默克尔证明路径

        Returns:
            bool: 验证是否成功
        """
        current_hash = hash_data(transaction)

        # 使用证明路径重建到根的路径
        for sibling_hash, direction in proof:
            if direction == "left":
                combined = sibling_hash + current_hash
            else:  # direction == "right"
                combined = current_hash + sibling_hash
            current_hash = hash_data(combined)

        # 检查最终哈希是否等于默克尔根
        return current_hash == self.get_root()

    def display_tree(self):
        """显示默克尔树结构"""
        print("🌳 默克尔树结构:")
        for level_idx, level in enumerate(self.tree):
            indent = "  " * (len(self.tree) - level_idx - 1)
            hashes = [h[:8] + "..." for h in level]
            print(f"{indent}Level {level_idx}: {hashes}")


def main():
    """主函数 - 演示默克尔树功能"""
    print("=== 默克尔树（Merkle Tree）演示 ===\n")

    # 创建一些交易数据
    transactions = [
        "Alice pays Bob 1 BTC",
        "Charlie pays David 2 BTC",
        "Eve pays Frank 3 BTC",
        "Grace pays Henry 4 BTC"
    ]

    print("📦 交易列表:")
    for i, tx in enumerate(transactions):
        print(f"   [{i}] {tx}")

    # 构建默克尔树
    print("\n🏗️  构建默克尔树...")
    merkle_tree = MerkleTree(transactions)
    merkle_tree.display_tree()

    root = merkle_tree.get_root()
    print(f"\n🔑 默克尔根: {root[:16]}...")

    # 验证交易存在性
    print("\n🔍 验证交易存在性...")
    test_transaction = "Alice pays Bob 1 BTC"
    proof = merkle_tree.get_merkle_proof(0)

    print(f"📝 交易 '{test_transaction}' 的证明路径:")
    for i, (sibling, direction) in enumerate(proof):
        print(f"   Step {i+1}: {direction} sibling = {sibling[:8]}...")

    is_valid = merkle_tree.verify_transaction(test_transaction, proof)
    print(f"\n✅ 验证结果: {'成功' if is_valid else '失败'}")

    # 演示篡改检测
    print("\n🎭 模拟篡改交易...")
    tampered_transaction = "Alice pays Bob 100 BTC"  # 篡改金额
    is_tampered_valid = merkle_tree.verify_transaction(tampered_transaction, proof)
    print(f"❌ 篡改交易验证结果: {'成功' if is_tampered_valid else '失败'}")

    print("\n💡 默克尔树优势:")
    print("   • 只需O(log n)的证明数据就能验证交易")
    print("   • 轻量级客户端无需下载完整区块链")
    print("   • 高效的数据完整性验证")
    print("   • 广泛应用于比特币、以太坊等区块链")


if __name__ == "__main__":
    main()