#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数独求解器 - 回溯算法应用

数独规则：
1. 每行包含数字1-9，不重复
2. 每列包含数字1-9，不重复
3. 每个3×3宫格包含数字1-9，不重复

回溯策略：
1. 找到下一个空格（值为0的位置）
2. 尝试填入1-9的数字
3. 检查填入后是否违反数独规则
4. 如果合法，递归求解剩余部分
5. 如果递归成功返回True，否则回溯并尝试下一个数字
"""

from typing import List


def is_valid(board: List[List[str]], row: int, col: int, num: str) -> bool:
    """
    检查在(row, col)位置填入num是否合法

    Args:
        board: 数独棋盘
        row: 行索引
        col: 列索引
        num: 要填入的数字

    Returns:
        是否合法
    """
    # 检查行是否有重复
    for j in range(9):
        if board[row][j] == num:
            return False

    # 检查列是否有重复
    for i in range(9):
        if board[i][col] == num:
            return False

    # 检查3×3宫格是否有重复
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def solve_sudoku(board: List[List[str]]) -> bool:
    """
    回溯求解数独

    Args:
        board: 数独棋盘，空格用'.'表示

    Returns:
        是否成功求解
    """
    for i in range(9):
        for j in range(9):
            # 找到空格
            if board[i][j] == '.':
                # 尝试填入1-9
                for num in map(str, range(1, 10)):
                    # 剪枝：检查是否合法
                    if is_valid(board, i, j, num):
                        # 选择：填入数字
                        board[i][j] = num

                        # 递归：继续求解
                        if solve_sudoku(board):
                            return True

                        # 回溯：撤销选择
                        board[i][j] = '.'

                # 所有数字都尝试过都不行，回溯
                return False

    # 所有空格都已填满，求解成功
    return True


def print_board(board: List[List[str]]) -> None:
    """打印数独棋盘"""
    print("+" + "-" * 21 + "+")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("|" + "-" * 21 + "|")

        row_str = "|"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += " |"
            row_str += f" {board[i][j]}"
        row_str += " |"
        print(row_str)
    print("+" + "-" * 21 + "+")


if __name__ == "__main__":
    # 测试数独
    sudoku_board = [
        ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
        ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
        ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
        ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
        ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
        ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
        ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
        ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
        ['.', '.', '.', '.', '8', '.', '.', '7', '9']
    ]

    print("原始数独：")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\n求解后的数独：")
        print_board(sudoku_board)
    else:
        print("\n无解！")