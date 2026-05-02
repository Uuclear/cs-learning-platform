#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N皇后问题 - 回溯算法经典示例

在一个N×N的棋盘上放置N个皇后，使得它们互不攻击。
皇后的攻击范围：同一行、同一列、同一对角线。

回溯策略：
1. 按行逐个放置皇后
2. 对于每一行，尝试每一列的位置
3. 检查当前位置是否与已放置的皇后冲突
4. 如果不冲突，放置皇后并递归处理下一行
5. 如果冲突或递归返回失败，回溯（移除当前皇后）并尝试下一列
"""

from typing import List, Set


def solve_n_queens(n: int) -> List[List[str]]:
    """
    解决N皇后问题

    Args:
        n: 棋盘大小和皇后数量

    Returns:
        所有可能的解决方案列表，每个方案是一个字符串列表
    """
    def is_safe(row: int, col: int, cols: Set[int], diag1: Set[int], diag2: Set[int]) -> bool:
        """
        检查在(row, col)位置放置皇后是否安全

        使用三个集合来快速检查冲突：
        - cols: 已占用的列
        - diag1: 已占用的主对角线 (row - col 为常数)
        - diag2: 已占用的副对角线 (row + col 为常数)
        """
        return col not in cols and (row - col) not in diag1 and (row + col) not in diag2

    def backtrack(row: int, current_solution: List[int],
                  cols: Set[int], diag1: Set[int], diag2: Set[int]) -> None:
        """
        回溯函数

        Args:
            row: 当前行
            current_solution: 当前解（每行皇后所在的列）
            cols: 已占用的列集合
            diag1: 已占用的主对角线集合
            diag2: 已占用的副对角线集合
        """
        # 基础情况：所有行都已处理完毕
        if row == n:
            # 将数字解转换为棋盘字符串表示
            board = []
            for r in range(n):
                row_str = ['.'] * n
                row_str[current_solution[r]] = 'Q'
                board.append(''.join(row_str))
            solutions.append(board)
            return

        # 尝试当前行的每一列
        for col in range(n):
            # 剪枝：检查当前位置是否安全
            if is_safe(row, col, cols, diag1, diag2):
                # 选择：放置皇后
                current_solution.append(col)
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)

                # 递归：处理下一行
                backtrack(row + 1, current_solution, cols, diag1, diag2)

                # 回溯：撤销选择（恢复状态）
                current_solution.pop()
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)

    solutions: List[List[str]] = []
    backtrack(0, [], set(), set(), set())
    return solutions


def print_solutions(solutions: List[List[str]]) -> None:
    """打印所有解决方案"""
    print(f"找到 {len(solutions)} 个解决方案：\n")
    for i, solution in enumerate(solutions, 1):
        print(f"方案 {i}:")
        for row in solution:
            print(row)
        print()


if __name__ == "__main__":
    # 测试4皇后问题
    n = 4
    print(f"解决 {n} 皇后问题：\n")
    solutions = solve_n_queens(n)
    print_solutions(solutions)