#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 死锁演示

这个脚本演示了数据库死锁的场景以及如何处理死锁。
两个线程试图以相反的顺序锁定相同的资源，导致死锁。
"""

import sqlite3
import threading
import time
import os
import random


def setup_database():
    """初始化数据库"""
    if os.path.exists('deadlock.db'):
        os.remove('deadlock.db')

    conn = sqlite3.connect('deadlock.db')
    cursor = conn.cursor()

    # 创建账户表
    cursor.execute('''
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')

    # 插入初始数据
    cursor.execute("INSERT INTO accounts (name, balance) VALUES ('账户1', 1000.0)")
    cursor.execute("INSERT INTO accounts (name, balance) VALUES ('账户2', 2000.0)")

    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def transfer_with_deadlock_risk(from_id, to_id, amount, thread_name):
    """有死锁风险的转账函数"""
    print(f"   {thread_name}: 尝试从账户{from_id} 转 {amount:.2f} 到 账户{to_id}")

    conn = sqlite3.connect('deadlock.db')
    try:
        conn.execute("BEGIN")

        # 先锁定转出账户（按ID顺序）
        conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (from_id,))
        time.sleep(0.1)  # 增加死锁概率

        # 再锁定转入账户
        conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (to_id,))

        # 执行转账
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))

        conn.commit()
        print(f"   {thread_name}: 转账成功！")

    except Exception as e:
        conn.rollback()
        print(f"   {thread_name}: 转账失败 - {e}")
    finally:
        conn.close()


def transfer_with_deadlock_prevention(from_id, to_id, amount, thread_name):
    """预防死锁的转账函数 - 总是按相同顺序锁定资源"""
    print(f"   {thread_name}: 尝试从账户{from_id} 转 {amount:.2f} 到 账户{to_id}")

    # 确保总是按ID升序锁定账户，避免循环等待
    first_lock = min(from_id, to_id)
    second_lock = max(from_id, to_id)

    conn = sqlite3.connect('deadlock.db')
    try:
        conn.execute("BEGIN")

        # 总是先锁定ID较小的账户
        conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (first_lock,))
        time.sleep(0.1)

        # 再锁定ID较大的账户
        conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (second_lock,))

        # 执行转账
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))

        conn.commit()
        print(f"   {thread_name}: 转账成功！")

    except Exception as e:
        conn.rollback()
        print(f"   {thread_name}: 转账失败 - {e}")
    finally:
        conn.close()


def demonstrate_deadlock():
    """演示死锁场景"""
    print("\n🔄 演示死锁场景")
    print("-" * 25)

    def thread1():
        """线程1: 从账户1转到账户2"""
        transfer_with_deadlock_risk(1, 2, 100.0, "线程1")

    def thread2():
        """线程2: 从账户2转到账户1"""
        transfer_with_deadlock_risk(2, 1, 200.0, "线程2")

    # 启动两个线程，它们会尝试以相反顺序锁定资源
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    t1.start()
    t2.start()

    t1.join(timeout=5)  # 设置超时避免无限等待
    t2.join(timeout=5)

    if t1.is_alive() or t2.is_alive():
        print("   ⚠️  检测到死锁！线程被强制终止")
    else:
        print("   死锁演示完成")


def demonstrate_deadlock_prevention():
    """演示死锁预防"""
    print("\n✅ 演示死锁预防")
    print("-" * 25)

    # 重置数据库
    setup_database()

    def thread1():
        """线程1: 从账户1转到账户2"""
        transfer_with_deadlock_prevention(1, 2, 100.0, "线程1")

    def thread2():
        """线程2: 从账户2转到账户1"""
        transfer_with_deadlock_prevention(2, 1, 200.0, "线程2")

    # 启动两个线程
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("   死锁预防演示完成")


def demonstrate_timeout_retry():
    """演示带超时和重试的死锁处理"""
    print("\n⏰ 演示超时重试机制")
    print("-" * 25)

    def safe_transfer_with_retry(from_id, to_id, amount, thread_name, max_retries=3):
        """带重试机制的安全转账"""
        for attempt in range(max_retries):
            try:
                print(f"   {thread_name}: 第{attempt + 1}次尝试转账")

                conn = sqlite3.connect('deadlock.db', timeout=2.0)  # 2秒超时
                conn.execute("BEGIN")

                # 按固定顺序锁定
                first_lock = min(from_id, to_id)
                second_lock = max(from_id, to_id)

                conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (first_lock,))
                time.sleep(0.1)
                conn.execute("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", (second_lock,))

                conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
                conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))

                conn.commit()
                conn.close()
                print(f"   {thread_name}: 转账成功！")
                return True

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    conn.rollback()
                    conn.close()
                    wait_time = random.uniform(0.1, 0.5)
                    print(f"   {thread_name}: 数据库锁定，{wait_time:.2f}秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    conn.rollback()
                    conn.close()
                    print(f"   {thread_name}: 转账失败 - {e}")
                    return False
            except Exception as e:
                conn.rollback()
                conn.close()
                print(f"   {thread_name}: 转账失败 - {e}")
                return False

    # 重置数据库
    setup_database()

    def thread1():
        safe_transfer_with_retry(1, 2, 150.0, "线程1")

    def thread2():
        safe_transfer_with_retry(2, 1, 250.0, "线程2")

    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def main():
    """主函数"""
    print("🔒 数据库死锁演示")
    print("=" * 30)

    setup_database()

    # 演示死锁
    demonstrate_deadlock()

    # 演示死锁预防
    demonstrate_deadlock_prevention()

    # 演示超时重试
    demonstrate_timeout_retry()

    print("\n💡 死锁处理策略:")
    print("- 按固定顺序获取锁（预防）")
    print("- 设置超时时间（检测）")
    print("- 实现重试机制（恢复）")
    print("- 使用死锁检测算法（高级）")


if __name__ == "__main__":
    main()