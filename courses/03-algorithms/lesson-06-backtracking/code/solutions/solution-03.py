#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编程挑战3解答：单词搜索

给定一个 m x n 二维字符网格 board 和一个字符串单词 word，
如果 word 存在于网格中，返回 true；否则，返回 false。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，
其中"相邻"单元格是那些水平相邻或垂直相邻的单元格。
同一个单元格内的字母不允许被重复使用。
"""

from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    """
    在网格中搜索单词

    Args:
        board: 字符网格
        word: 要搜索的单词

    Returns:
        单词是否存在
    """
    if not board or not board[0] or not word:
        return False

    rows, cols = len(board), len(board[0])

    def dfs(row: int, col: int, index: int, visited: set) -> bool:
        """
        深度优先搜索（回溯）

        Args:
            row: 当前行
            col: 当前列
            index: 当前匹配到单词的第几个字符
            visited: 已访问的位置集合
        """
        # 基础情况：已匹配完整个单词
        if index == len(word):
            return True

        # 边界检查和访问检查
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            (row, col) in visited or board[row][col] != word[index]):
            return False

        # 标记当前位置为已访问
        visited.add((row, col))

        # 向四个方向递归搜索
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            if dfs(row + dr, col + dc, index + 1, visited):
                return True

        # 回溯：撤销访问标记
        visited.remove((row, col))
        return False

    # 尝试从每个位置开始搜索
    for i in range(rows):
        for j in range(cols):
            if dfs(i, j, 0, set()):
                return True

    return False


if __name__ == "__main__":
    # 测试用例1
    board1 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word1 = "ABCCED"
    print(f"网格1: {board1}")
    print(f"单词1: {word1}")
    print(f"结果: {exist(board1, word1)}")  # 应该返回True

    print()

    # 测试用例2
    board2 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word2 = "SEE"
    print(f"网格2: {board2}")
    print(f"单词2: {word2}")
    print(f"结果: {exist(board2, word2)}")  # 应该返回True

    print()

    # 测试用例3
    board3 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word3 = "ABCB"
    print(f"网格3: {board3}")
    print(f"单词3: {word3}")
    print(f"结果: {exist(board3, word3)}")  # 应该返回False