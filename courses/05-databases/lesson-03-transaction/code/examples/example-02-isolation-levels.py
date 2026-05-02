#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 隔离级别演示

这个脚本使用多线程来演示不同隔离级别下的并发行为，
展示脏读、不可重复读和幻读等并发异常。
"""

import sqlite3
import threading
import time
import os


def setup_database():
    """初始化数据库"""
    if os.path.exists('isolation.db'):
        os.remove('isolation.db')

    conn = sqlite3.connect('isolation.db')
    cursor = conn.cursor()

    # 创建产品表
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # 插入初始数据
    cursor.execute("INSERT INTO products (name, price, stock) VALUES ('笔记本电脑', 5000.0, 10)")
    cursor.execute("INSERT INTO products (name, price, stock) VALUES ('手机', 3000.0, 20)")

    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def transaction_read_uncommitted():
    """演示读未提交隔离级别（脏读）"""
    print("\n🔍 演示读未提交隔离级别（可能导致脏读）")

    def writer_thread():
        """写入线程 - 执行未提交的更新"""
        conn = sqlite3.connect('isolation.db')
        try:
            conn.execute("BEGIN")
            # 更新价格但不提交
            conn.execute("UPDATE products SET price = 6000.0 WHERE name = '笔记本电脑'")
            print("   写入线程: 已将笔记本电脑价格更新为 6000.0（未提交）")

            # 等待一段时间，让读取线程有机会读取
            time.sleep(2)

            # 回滚事务（模拟失败）
            conn.rollback()
            print("   写入线程: 回滚事务，价格恢复为 5000.0")
        finally:
            conn.close()

    def reader_thread():
        """读取线程 - 在写入线程未提交时读取"""
        time.sleep(1)  # 等待写入线程开始
        conn = sqlite3.connect('isolation.db')
        try:
            # SQLite 默认是 READ UNCOMMITTED 对于 WAL 模式
            # 但在普通模式下实际上是 SERIALIZABLE
            # 我们这里主要演示概念
            cursor = conn.execute("SELECT name, price FROM products WHERE name = '笔记本电脑'")
            row = cursor.fetchone()
            print(f"   读取线程: 读取到笔记本电脑价格为 {row[1]:.1f} 元")
        finally:
            conn.close()

    # 启动线程
    writer = threading.Thread(target=writer_thread)
    reader = threading.Thread(target=reader_thread)

    writer.start()
    reader.start()

    writer.join()
    reader.join()


def transaction_read_committed():
    """演示读已提交隔离级别（避免脏读，但可能有不可重复读）"""
    print("\n🔍 演示读已提交隔离级别")

    def first_reader():
        """第一次读取"""
        conn = sqlite3.connect('isolation.db')
        try:
            cursor = conn.execute("SELECT stock FROM products WHERE name = '手机'")
            stock1 = cursor.fetchone()[0]
            print(f"   第一次读取: 手机库存为 {stock1}")

            # 等待其他事务提交
            time.sleep(3)

            cursor = conn.execute("SELECT stock FROM products WHERE name = '手机'")
            stock2 = cursor.fetchone()[0]
            print(f"   第二次读取: 手机库存为 {stock2}")

            if stock1 != stock2:
                print("   ⚠️  发现不可重复读！")
        finally:
            conn.close()

    def updater():
        """更新库存"""
        time.sleep(1)
        conn = sqlite3.connect('isolation.db')
        try:
            conn.execute("BEGIN")
            conn.execute("UPDATE products SET stock = stock - 5 WHERE name = '手机'")
            conn.commit()
            print("   更新线程: 已提交库存更新（减少5台）")
        finally:
            conn.close()

    # 启动线程
    reader = threading.Thread(target=first_reader)
    updater_thread = threading.Thread(target=updater)

    reader.start()
    updater_thread.start()

    reader.join()
    updater_thread.join()


def transaction_repeatable_read_concept():
    """演示可重复读概念（SQLite 实际上是串行化，但展示概念）"""
    print("\n🔍 演示可重复读概念")

    def consistent_reader():
        """一致性读取者"""
        conn = sqlite3.connect('isolation.db')
        try:
            # 开始事务
            conn.execute("BEGIN")

            # 第一次查询
            cursor = conn.execute("SELECT COUNT(*) FROM products")
            count1 = cursor.fetchone()[0]
            print(f"   事务内第一次查询: 产品总数 {count1}")

            time.sleep(2)  # 等待其他线程

            # 第二次查询（在同一事务中）
            cursor = conn.execute("SELECT COUNT(*) FROM products")
            count2 = cursor.fetchone()[0]
            print(f"   事务内第二次查询: 产品总数 {count2}")

            if count1 == count2:
                print("   ✅ 可重复读：两次查询结果一致")
            else:
                print("   ⚠️  出现幻读！")

            conn.commit()
        finally:
            conn.close()

    def inserter():
        """插入新产品的线程"""
        time.sleep(1)
        conn = sqlite3.connect('isolation.db')
        try:
            conn.execute("INSERT INTO products (name, price, stock) VALUES ('平板电脑', 2500.0, 15)")
            conn.commit()
            print("   插入线程: 已添加新产品'平板电脑'")
        finally:
            conn.close()

    # 启动线程
    reader = threading.Thread(target=consistent_reader)
    inserter_thread = threading.Thread(target=inserter)

    reader.start()
    inserter_thread.start()

    reader.join()
    inserter_thread.join()


def main():
    """主函数"""
    print("📊 数据库隔离级别演示")
    print("=" * 40)

    setup_database()

    # 演示不同的隔离级别场景
    transaction_read_uncommitted()
    transaction_read_committed()
    transaction_repeatable_read_concept()

    print("\n📝 总结:")
    print("- 读未提交: 可能读取未提交的数据（脏读）")
    print("- 读已提交: 避免脏读，但同一事务内多次读取可能不同（不可重复读）")
    print("- 可重复读: 同一事务内多次读取结果一致，但可能看到新插入的行（幻读）")
    print("- 串行化: 完全隔离，并发事务如同串行执行")


if __name__ == "__main__":
    main()