#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：银行账户类实现

使用TDD方式实现的简单银行账户类，支持存款、取款和查询余额
"""

class BankAccount:
    """银行账户类"""

    def __init__(self, initial_balance=0):
        """
        初始化银行账户

        Args:
            initial_balance (float): 初始余额，默认为0

        Raises:
            ValueError: 如果初始余额为负数
        """
        if initial_balance < 0:
            raise ValueError("初始余额不能为负数")
        self._balance = initial_balance

    def deposit(self, amount):
        """
        存款

        Args:
            amount (float): 存款金额

        Raises:
            ValueError: 如果存款金额小于等于0
        """
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        self._balance += amount

    def withdraw(self, amount):
        """
        取款

        Args:
            amount (float): 取款金额

        Raises:
            ValueError: 如果取款金额小于等于0或超过余额
        """
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount

    def get_balance(self):
        """
        获取当前余额

        Returns:
            float: 当前余额
        """
        return self._balance

    def transfer(self, other_account, amount):
        """
        转账到另一个账户

        Args:
            other_account (BankAccount): 目标账户
            amount (float): 转账金额

        Raises:
            ValueError: 如果转账金额无效或余额不足
            TypeError: 如果目标账户不是BankAccount实例
        """
        if not isinstance(other_account, BankAccount):
            raise TypeError("目标账户必须是BankAccount实例")

        # 先从当前账户取款，再向目标账户存款
        self.withdraw(amount)
        other_account.deposit(amount)


if __name__ == '__main__':
    # 测试银行账户功能
    account1 = BankAccount(100)
    account2 = BankAccount(50)

    print(f"账户1初始余额: {account1.get_balance()}")
    print(f"账户2初始余额: {account2.get_balance()}")

    # 存款测试
    account1.deposit(50)
    print(f"账户1存款50后余额: {account1.get_balance()}")

    # 取款测试
    account1.withdraw(30)
    print(f"账户1取款30后余额: {account1.get_balance()}")

    # 转账测试
    account1.transfer(account2, 20)
    print(f"转账20后 - 账户1余额: {account1.get_balance()}, 账户2余额: {account2.get_balance()}")