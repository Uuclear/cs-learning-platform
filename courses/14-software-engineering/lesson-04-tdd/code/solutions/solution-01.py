#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：FizzBuzz游戏实现

使用TDD方式实现的FizzBuzz游戏
"""

def fizzbuzz(number):
    """
    FizzBuzz游戏实现

    Args:
        number (int): 输入的数字

    Returns:
        str: 根据规则返回的结果
            - 能被3和5整除：返回"FizzBuzz"
            - 能被3整除：返回"Fizz"
            - 能被5整除：返回"Buzz"
            - 其他情况：返回数字的字符串形式
    """
    if number % 15 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return str(number)


if __name__ == '__main__':
    # 测试FizzBuzz函数
    for i in range(1, 21):
        print(f"{i}: {fizzbuzz(i)}")