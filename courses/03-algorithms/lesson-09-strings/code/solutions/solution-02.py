#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：实现单词查找树的自动补全功能
基于之前实现的Trie树，添加自动补全功能
"""

from typing import List


class TrieNode:
    """Trie树节点"""

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class AutocompleteTrie:
    """支持自动补全的Trie树"""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """插入单词"""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search_prefix(self, prefix: str) -> 'TrieNode':
        """查找前缀对应的节点"""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current

    def get_suggestions(self, prefix: str, max_suggestions: int = 5) -> List[str]:
        """
        获取自动补全建议

        Args:
            prefix: 输入的前缀
            max_suggestions: 最大建议数量

        Returns:
            自动补全建议列表
        """
        node = self.search_prefix(prefix)
        if not node:
            return []

        suggestions = []
        self._dfs(node, prefix, suggestions, max_suggestions)
        return suggestions[:max_suggestions]

    def _dfs(self, node: 'TrieNode', current_word: str, suggestions: List[str], max_suggestions: int) -> None:
        """深度优先搜索获取建议"""
        if len(suggestions) >= max_suggestions:
            return

        if node.is_end_of_word:
            suggestions.append(current_word)

        # 按字典序遍历子节点（确保结果有序）
        for char in sorted(node.children.keys()):
            self._dfs(node.children[char], current_word + char, suggestions, max_suggestions)


def main():
    # 构建词典
    autocomplete = AutocompleteTrie()
    dictionary = [
        "apple", "application", "apply", "appreciate", "approach",
        "banana", "band", "bandage", "bank", "base",
        "cat", "car", "card", "care", "career"
    ]

    for word in dictionary:
        autocomplete.insert(word)

    # 测试自动补全
    test_prefixes = ["app", "ba", "ca", "xyz"]
    print("=== 自动补全演示 ===")
    for prefix in test_prefixes:
        suggestions = autocomplete.get_suggestions(prefix)
        print(f"前缀 '{prefix}' 的建议: {suggestions}")


if __name__ == "__main__":
    main()