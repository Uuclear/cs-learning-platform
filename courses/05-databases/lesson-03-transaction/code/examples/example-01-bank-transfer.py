#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 银行转账事务演示

这个脚本演示了如何使用数据库事务来确保银行转账的原子性。
如果转账过程中发生错误，整个操作会回滚，保证数据一致性。
"""

import sqlite3
import os
import sys


def setup_database():
    """初始化数据库和测试数据"""
    # 删除已存在的数据库文件（如果存在）
    if os.path.exists('bank.db'):
        os.remove('bank.db')

    # 连接数据库
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # 创建账户表
    cursor.execute('''
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL CHECK (balance >= 0)
        )
    ''')

    # 插入初始数据
    cursor.execute("INSERT INTO accounts (id, name, balance) VALUES ('A', '张三', 2000.0)")
    cursor.execute("INSERT INTO accounts (id, name, balance) VALUES ('B', '李四', 1500.0)")
    cursor.execute("INSERT INTO accounts (id, name, balance) VALUES ('C', '王五', 3000.0)")

    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")
    print("初始账户余额:")
    print("- 账户A (张三): 2000.00 元")
    print("- 账户B (李四): 1500.00 元")
    print("- 账户C (王五): 3000.00 元")
    print()


def display_balances():
    """显示所有账户余额"""
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, balance FROM accounts ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    print("当前账户余额:")
    for row in rows:
        print(f"- 账户{row[0]} ({row[1]}): {row[2]:.2f} 元")
    print()


def transfer_money_safe(from_account, to_account, amount):
    """安全的转账函数 - 使用事务"""
    print(f"🔄 开始转账: 从账户{from_account} 转 {amount:.2f} 元 到 账户{to_account}")

    conn = sqlite3.connect('bank.db')
    try:
        # 开始事务
        conn.execute("BEGIN")

        # 检查转出账户余额
        cursor = conn.execute("SELECT balance FROM accounts WHERE id = ?", (from_account,))
        from_balance = cursor.fetchone()
        if not from_balance:
            raise ValueError(f"账户 {from_account} 不存在")

        if from_balance[0] < amount:
            raise ValueError(f"账户 {from_account} 余额不足")

        # 执行转账
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?",
                    (amount, from_account))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?",
                    (amount, to_account))

        # 提交事务
        conn.commit()
        print(f"✅ 转账成功!")

    except Exception as e:
        # 发生错误时回滚事务
        conn.rollback()
        print(f"❌ 转账失败: {e}")
        raise
    finally:
        conn.close()


def transfer_money_unsafe(from_account, to_account, amount):
    """不安全的转账函数 - 不使用事务（仅用于演示问题）"""
    print(f"⚠️  开始不安全转账: 从账户{from_account} 转 {amount:.2f} 元 到 账户{to_account}")

    conn = sqlite3.connect('bank.db')
    try:
        # 不使用事务 - 自动提交模式

        # 检查并扣款（这一步会立即生效）
        cursor = conn.execute("SELECT balance FROM accounts WHERE id = ?", (from_account,))
        from_balance = cursor.fetchone()
        if not from_balance:
            raise ValueError(f"账户 {from_account} 不存在")

        if from_balance[0] < amount:
            raise ValueError(f"账户 {from_account} 余额不足")

        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?",
                    (amount, from_account))
        conn.commit()  # 立即提交扣款

        print(f"   已从账户{from_account} 扣除 {amount:.2f} 元")

        # 模拟在存款前发生错误
        raise RuntimeError("模拟系统故障！存款操作无法执行")

        # 这行永远不会执行
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?",
                    (amount, to_account))
        conn.commit()

    except Exception as e:
        print(f"❌ 不安全转账失败: {e}")
        # 注意：这里无法回滚已经提交的扣款操作！
        raise
    finally:
        conn.close()


def main():
    """主函数 - 演示事务的重要性"""
    print("🏦 银行转账事务演示")
    print("=" * 50)

    # 初始化数据库
    setup_database()

    # 显示初始状态
    display_balances()

    print("案例1: 安全转账（使用事务）")
    print("-" * 30)
    try:
        transfer_money_safe('A', 'B', 500.0)
    except Exception:
        pass  # 忽略异常，继续演示

    display_balances()

    print("\n案例2: 不安全转账（无事务保护）")
    print("-" * 35)
    try:
        transfer_money_unsafe('C', 'A', 1000.0)
    except Exception:
        pass  # 忽略异常

    display_balances()

    print("💡 总结:")
    print("- 使用事务可以保证操作的原子性")
    print("- 不使用事务可能导致数据不一致")
    print("- COMMIT提交事务，ROLLBACK回滚事务")


if __name__ == "__main__":
    main()