#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trie树（前缀树）实现示例

Trie树是一种用于存储字符串集合的树形数据结构，
每个节点代表一个字符，从根到叶子的路径构成完整的字符串。
Trie树在自动补全、拼写检查、IP路由等场景中有广泛应用。
"""

from typing import Dict, Optional, List


class TrieNode:
    """Trie树的节点类"""

    def __init__(self):
        # 子节点字典，键为字符，值为对应的子节点
        self.children: Dict[str, 'TrieNode'] = {}
        # 标记当前节点是否为某个单词的结尾
        self.is_end_of_word: bool = False
        # 可选：存储以当前前缀开头的单词数量（用于统计）
        self.word_count: int = 0


class Trie:
    """Trie树实现"""

    def __init__(self):
        # 根节点不包含任何字符
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        向Trie树中插入一个单词

        Args:
            word: 要插入的单词
        """
        current = self.root

        for char in word:
            # 如果当前字符不存在，则创建新节点
            if char not in current.children:
                current.children[char] = TrieNode()

            current = current.children[char]
            current.word_count += 1  # 增加以当前前缀开头的单词计数

        # 标记单词结尾
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        在Trie树中搜索完整单词

        Args:
            word: 要搜索的单词

        Returns:
            如果存在该单词返回True，否则返回False
        """
        current = self.root

        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]

        # 必须是完整单词的结尾
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        检查Trie树中是否存在以指定前缀开头的单词

        Args:
            prefix: 前缀字符串

        Returns:
            如果存在以该前缀开头的单词返回True，否则返回False
        """
        current = self.root

        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]

        return True

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        获取所有以指定前缀开头的单词

        Args:
            prefix: 前缀字符串

        Returns:
            所有匹配的单词列表
        """
        current = self.root

        # 先找到前缀对应的节点
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        # 从当前节点开始DFS遍历所有可能的单词
        words = []
        self._dfs(current, prefix, words)
        return words

    def _dfs(self, node: TrieNode, current_word: str, words: List[str]) -> None:
        """
        深度优先搜索辅助函数

        Args:
            node: 当前节点
            current_word: 当前构建的单词
            words: 结果列表
        """
        if node.is_end_of_word:
            words.append(current_word)

        for char, child_node in node.children.items():
            self._dfs(child_node, current_word + char, words)

    def delete(self, word: str) -> bool:
        """
        从Trie树中删除一个单词

        Args:
            word: 要删除的单词

        Returns:
            如果成功删除返回True，如果单词不存在返回False
        """
        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            """
            删除辅助函数，返回当前节点是否应该被删除
            """
            if index == len(word):
                # 到达单词末尾
                if not node.is_end_of_word:
                    return False  # 单词不存在

                node.is_end_of_word = False
                node.word_count -= 1
                # 如果没有子节点且不是其他单词的结尾，则可以删除
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False  # 单词不存在

            child_node = node.children[char]
            should_delete_child = _delete_helper(child_node, word, index + 1)

            if should_delete_child:
                del node.children[char]
                node.word_count -= 1

            # 当前节点可以被删除的条件：
            # 1. 不是任何单词的结尾
            # 2. 没有子节点
            return not node.is_end_of_word and len(node.children) == 0

        return _delete_helper(self.root, word, 0)


def main():
    """Trie树演示"""
    trie = Trie()

    # 插入单词
    words_to_insert = ["apple", "app", "application", "apply", "aptitude", "banana", "band"]
    print("=== Trie树（前缀树）演示 ===")
    print(f"插入单词: {words_to_insert}")

    for word in words_to_insert:
        trie.insert(word)

    # 搜索完整单词
    print("\n--- 完整单词搜索 ---")
    test_words = ["app", "apple", "appl", "banana", "ban"]
    for word in test_words:
        exists = trie.search(word)
        print(f"'{word}' 存在: {exists}")

    # 前缀搜索
    print("\n--- 前缀搜索 ---")
    prefixes = ["app", "ban", "ap", "xyz"]
    for prefix in prefixes:
        has_prefix = trie.starts_with(prefix)
        print(f"存在以 '{prefix}' 开头的单词: {has_prefix}")

    # 获取所有以指定前缀开头的单词
    print("\n--- 获取前缀匹配的单词 ---")
    prefix_words = trie.get_words_with_prefix("app")
    print(f"以 'app' 开头的单词: {prefix_words}")

    # 删除单词
    print("\n--- 删除操作 ---")
    deleted = trie.delete("app")
    print(f"删除 'app': {'成功' if deleted else '失败（不存在）'}")

    # 验证删除结果
    print(f"删除后 'app' 存在: {trie.search('app')}")
    print(f"删除后 'apple' 存在: {trie.search('apple')}")


if __name__ == "__main__":
    main()