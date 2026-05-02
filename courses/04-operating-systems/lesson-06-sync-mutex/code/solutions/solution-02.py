#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 银行转账模拟

模拟多个账户之间的转账操作，确保转账过程线程安全。
使用锁的获取顺序来避免死锁。
"""

import threading
import time
import random

class Account:
    """银行账户类"""

    def __init__(self, account_id, initial_balance=0):
        """初始化账户

        Args:
            account_id: 账户ID
            initial_balance: 初始余额
        """
        self.account_id = account_id
        self.balance = initial_balance
        self.lock = threading.Lock()

    def __str__(self):
        return f"Account({self.account_id}, balance={self.balance})"

def transfer(from_account, to_account, amount):
    """转账函数 - 线程安全版本

    使用锁的获取顺序来避免死锁：
    总是按照账户ID的大小顺序获取锁。

    Args:
        from_account: 源账户
        to_account: 目标账户
        amount: 转账金额
    """
    # 确保总是按相同顺序获取锁，避免死锁
    if id(from_account) < id(to_account):
        first_lock = from_account.lock
        second_lock = to_account.lock
        first_account = from_account
        second_account = to_account
    else:
        first_lock = to_account.lock
        second_lock = from_account.lock
        first_account = to_account
        second_account = from_account

    # 获取第一个锁
    with first_lock:
        # 获取第二个锁
        with second_lock:
            # 执行转账操作
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                return True
            else:
                print(f"❌ 转账失败: {from_account.account_id} 余额不足")
                return False

def random_transfer(accounts, thread_id):
    """随机转账工作函数

    模拟随机的转账操作

    Args:
        accounts: 账户列表
        thread_id: 线程ID
    """
    for _ in range(100):  # 每个线程执行100次转账
        # 随机选择两个不同的账户
        from_idx, to_idx = random.sample(range(len(accounts)), 2)
        from_account = accounts[from_idx]
        to_account = accounts[to_idx]

        # 随机转账金额 (1-100)
        amount = random.randint(1, 100)

        success = transfer(from_account, to_account, amount)
        if success:
            print(f"✅ 线程{thread_id}: {from_account.account_id} -> {to_account.account_id} ${amount}")
        else:
            print(f"❌ 线程{thread_id}: 转账失败")

        # 短暂休眠，模拟真实场景
        time.sleep(0.001)

def main():
    """主函数 - 测试多线程转账"""
    # 创建账户
    accounts = [
        Account("A", 1000),
        Account("B", 1000),
        Account("C", 1000),
        Account("D", 1000)
    ]

    print("初始账户状态:")
    for account in accounts:
        print(f"  {account}")

    # 创建并启动转账线程
    threads = []
    for i in range(5):  # 5个并发转账线程
        thread = threading.Thread(
            target=random_transfer,
            args=(accounts, i+1),
            name=f"TransferThread-{i+1}"
        )
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("\n最终账户状态:")
    total_balance = 0
    for account in accounts:
        print(f"  {account}")
        total_balance += account.balance

    print(f"\n总余额: {total_balance}")
    print(f"初始总余额: {4 * 1000}")
    print(f"余额守恒: {total_balance == 4 * 1000}")

if __name__ == "__main__":
    main()