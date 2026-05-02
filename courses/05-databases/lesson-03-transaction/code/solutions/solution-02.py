#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2: 并发银行系统

构建一个支持并发转账的银行系统，使用适当的隔离级别处理并发访问。
"""

import sqlite3
import threading
import time
import random
import os
from typing import List, Tuple


class BankingSystem:
    def __init__(self, db_path='banking.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建账户表
        cursor.execute('''
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL CHECK (balance >= 0),
                version INTEGER NOT NULL DEFAULT 0
            )
        ''')

        # 创建交易记录表
        cursor.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account_id INTEGER,
                to_account_id INTEGER,
                amount REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_account_id) REFERENCES accounts(id),
                FOREIGN KEY (to_account_id) REFERENCES accounts(id)
            )
        ''')

        # 插入初始账户
        initial_accounts = [
            ("Alice", 5000.0),
            ("Bob", 3000.0),
            ("Charlie", 7000.0),
            ("Diana", 4000.0)
        ]

        for name, balance in initial_accounts:
            cursor.execute(
                "INSERT INTO accounts (name, balance) VALUES (?, ?)",
                (name, balance)
            )

        conn.commit()
        conn.close()

    def get_account_id(self, account_name: str) -> int:
        """根据账户名获取账户ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def get_balance(self, account_name: str) -> float:
        """获取账户余额"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT balance FROM accounts WHERE name = ?", (account_name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0.0

    def transfer_funds_optimistic(self, from_name: str, to_name: str, amount: float) -> bool:
        """
        使用乐观锁进行转账（适合低并发场景）

        Args:
            from_name: 转出账户名
            to_name: 转入账户名
            amount: 转账金额

        Returns:
            bool: 转账是否成功
        """
        max_retries = 3
        retry_delay = 0.1

        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect(self.db_path)
                conn.execute("BEGIN")

                # 获取转出账户信息（包括版本号）
                cursor = conn.execute(
                    "SELECT id, balance, version FROM accounts WHERE name = ?",
                    (from_name,)
                )
                from_row = cursor.fetchone()
                if not from_row:
                    raise ValueError(f"账户 {from_name} 不存在")

                from_id, from_balance, from_version = from_row

                # 检查余额
                if from_balance < amount:
                    raise ValueError(f"账户 {from_name} 余额不足")

                # 获取转入账户信息
                cursor = conn.execute(
                    "SELECT id, version FROM accounts WHERE name = ?",
                    (to_name,)
                )
                to_row = cursor.fetchone()
                if not to_row:
                    raise ValueError(f"账户 {to_name} 不存在")

                to_id, to_version = to_row

                # 执行转账
                conn.execute(
                    "UPDATE accounts SET balance = balance - ?, version = version + 1 WHERE id = ? AND version = ?",
                    (amount, from_id, from_version)
                )

                conn.execute(
                    "UPDATE accounts SET balance = balance + ?, version = version + 1 WHERE id = ? AND version = ?",
                    (amount, to_id, to_version)
                )

                # 检查是否所有更新都成功（乐观锁验证）
                cursor = conn.execute(
                    "SELECT changes()"
                )
                changes = cursor.fetchone()[0]

                if changes != 2:  # 应该有2行被更新
                    conn.rollback()
                    if attempt < max_retries - 1:
                        # 等待随机时间后重试
                        time.sleep(retry_delay * (1 + random.random()))
                        conn.close()
                        continue
                    else:
                        raise RuntimeError("并发冲突，重试次数已用尽")

                # 记录交易
                conn.execute(
                    "INSERT INTO transactions (from_account_id, to_account_id, amount, status) VALUES (?, ?, ?, ?)",
                    (from_id, to_id, amount, 'completed')
                )

                conn.commit()
                conn.close()
                print(f"✅ {from_name} → {to_name}: {amount:.2f} 元 (乐观锁)")
                return True

            except Exception as e:
                conn.rollback()
                conn.close()
                if attempt == max_retries - 1:
                    print(f"❌ {from_name} → {to_name}: {amount:.2f} 元 失败 - {e}")
                    return False

    def transfer_funds_pessimistic(self, from_name: str, to_name: str, amount: float) -> bool:
        """
        使用悲观锁进行转账（适合高并发场景）

        Args:
            from_name: 转出账户名
            to_name: 转入账户名
            amount: 转账金额

        Returns:
            bool: 转账是否成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("BEGIN")

            # 按账户ID升序锁定账户，避免死锁
            from_id = self.get_account_id(from_name)
            to_id = self.get_account_id(to_name)

            if from_id is None or to_id is None:
                raise ValueError("账户不存在")

            first_lock = min(from_id, to_id)
            second_lock = max(from_id, to_id)

            # 锁定第一个账户
            cursor = conn.execute(
                "SELECT balance FROM accounts WHERE id = ? FOR UPDATE",
                (first_lock,)
            )
            first_balance = cursor.fetchone()[0]

            # 锁定第二个账户
            cursor = conn.execute(
                "SELECT balance FROM accounts WHERE id = ? FOR UPDATE",
                (second_lock,)
            )
            second_balance = cursor.fetchone()[0]

            # 验证转出账户余额
            actual_from_balance = first_balance if from_id == first_lock else second_balance
            if actual_from_balance < amount:
                raise ValueError(f"账户 {from_name} 余额不足")

            # 执行转账
            conn.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id)
            )
            conn.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id)
            )

            # 记录交易
            conn.execute(
                "INSERT INTO transactions (from_account_id, to_account_id, amount, status) VALUES (?, ?, ?, ?)",
                (from_id, to_id, amount, 'completed')
            )

            conn.commit()
            conn.close()
            print(f"✅ {from_name} → {to_name}: {amount:.2f} 元 (悲观锁)")
            return True

        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"❌ {from_name} → {to_name}: {amount:.2f} 元 失败 - {e}")
            return False

    def simulate_concurrent_transfers(self):
        """模拟并发转账场景"""
        print("🏦 开始模拟并发银行转账...")
        print("=" * 50)

        # 显示初始余额
        accounts = ["Alice", "Bob", "Charlie", "Diana"]
        print("初始余额:")
        for account in accounts:
            balance = self.get_balance(account)
            print(f"- {account}: {balance:.2f} 元")
        print()

        def transfer_task(from_name: str, to_name: str, amount: float, method: str = "optimistic"):
            """转账任务"""
            time.sleep(random.uniform(0.1, 0.3))  # 随机延迟

            if method == "optimistic":
                self.transfer_funds_optimistic(from_name, to_name, amount)
            else:
                self.transfer_funds_pessimistic(from_name, to_name, amount)

        # 定义转账任务
        transfer_tasks = [
            ("Alice", "Bob", 500.0, "optimistic"),
            ("Bob", "Charlie", 300.0, "optimistic"),
            ("Charlie", "Diana", 800.0, "pessimistic"),
            ("Diana", "Alice", 400.0, "pessimistic"),
            ("Alice", "Charlie", 600.0, "optimistic"),
            ("Bob", "Diana", 200.0, "pessimistic"),
        ]

        # 创建并启动线程
        threads = []
        for from_name, to_name, amount, method in transfer_tasks:
            thread = threading.Thread(
                target=transfer_task,
                args=(from_name, to_name, amount, method)
            )
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 显示最终余额
        print("\n📊 最终余额:")
        total_balance = 0
        for account in accounts:
            balance = self.get_balance(account)
            print(f"- {account}: {balance:.2f} 元")
            total_balance += balance

        print(f"\n💰 总资产: {total_balance:.2f} 元")
        print("✅ 资产守恒验证通过！" if abs(total_balance - 19000.0) < 0.01 else "❌ 资产不守恒！")


def main():
    """主函数"""
    bank = BankingSystem()
    bank.simulate_concurrent_transfers()


if __name__ == "__main__":
    main()