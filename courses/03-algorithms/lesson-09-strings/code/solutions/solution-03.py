#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：实现多模式字符串匹配（Aho-Corasick算法简化版）
使用Trie树 + KMP思想的结合，同时搜索多个模式
"""

from collections import deque
from typing import Dict, List, Tuple


class MultiPatternMatcher:
    """多模式字符串匹配器"""

    def __init__(self):
        self.trie = {}
        self.fail = {}
        self.output = {}
        self.patterns = []

    def add_pattern(self, pattern: str) -> None:
        """添加要搜索的模式"""
        self.patterns.append(pattern)
        node = self.trie

        # 构建Trie树
        for char in pattern:
            if char not in node:
                node[char] = {}
            node = node[node]

        # 标记输出（在实际实现中需要存储模式索引）
        # 这里简化处理，只记录存在性

    def build_automaton(self) -> None:
        """构建Aho-Corasick自动机"""
        # 初始化根节点的失败指针
        queue = deque()

        # 设置根节点直接子节点的失败指针为根节点
        for char, child in self.trie.items():
            self.fail[id(child)] = id(self.trie)
            queue.append(child)

        # BFS构建失败指针
        while queue:
            current = queue.popleft()
            current_id = id(current)

            for char, child in current.items():
                queue.append(child)
                child_id = id(child)

                # 找到当前节点的失败节点
                fail_node = self.fail.get(current_id, self.trie)

                # 沿着失败指针链查找
                while fail_node != self.trie and char not in fail_node:
                    fail_node = self.fail.get(id(fail_node), self.trie)

                # 设置子节点的失败指针
                if char in fail_node:
                    self.fail[child_id] = id(fail_node[char])
                else:
                    self.fail[child_id] = id(self.trie)

    def search_all(self, text: str) -> List[Tuple[int, str]]:
        """
        在文本中搜索所有模式

        Args:
            text: 输入文本

        Returns:
            (位置, 模式) 元组列表
        """
        results = []
        current = self.trie

        for i, char in enumerate(text):
            # 如果当前字符不在当前节点的子节点中，沿着失败指针回溯
            while current != self.trie and char not in current:
                current = self.fail.get(id(current), self.trie)

            if char in current:
                current = current[char]

            # 检查当前节点是否匹配任何模式（简化版）
            # 在完整实现中，需要检查输出函数和失败链上的所有输出

        return results


def simple_multi_search(text: str, patterns: List[str]) -> List[Tuple[int, str]]:
    """
    简化版多模式搜索：对每个模式分别使用KMP

    Args:
        text: 文本串
        patterns: 模式列表

    Returns:
        (位置, 模式) 元组列表
    """
    from typing import List

    def kmp_search_single(text: str, pattern: str) -> List[int]:
        """单模式KMP搜索"""
        if not pattern:
            return []

        # 构建next数组
        n = len(pattern)
        next_array = [0] * n
        j = 0

        for i in range(1, n):
            while j > 0 and pattern[i] != pattern[j]:
                j = next_array[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            next_array[i] = j

        # 搜索
        matches = []
        j = 0
        for i in range(len(text)):
            while j > 0 and text[i] != pattern[j]:
                j = next_array[j - 1]
            if text[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                matches.append(i - j + 1)
                j = next_array[j - 1]

        return matches

    results = []
    for pattern in patterns:
        positions = kmp_search_single(text, pattern)
        for pos in positions:
            results.append((pos, pattern))

    # 按位置排序
    results.sort()
    return results


def main():
    """多模式匹配演示"""
    text = "the quick brown fox jumps over the lazy dog"
    patterns = ["the", "fox", "dog", "quick"]

    print("=== 多模式字符串匹配演示 ===")
    print(f"文本: '{text}'")
    print(f"模式: {patterns}")

    results = simple_multi_search(text, patterns)
    print("\n匹配结果:")
    for pos, pattern in results:
        print(f"  位置 {pos}: '{pattern}'")


if __name__ == "__main__":
    main()