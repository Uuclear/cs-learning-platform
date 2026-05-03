#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：OLTP vs OLAP 查询对比

本示例演示在线事务处理(OLTP)和在线分析处理(OLAP)的查询差异。
使用SQLite数据库模拟两种不同类型的查询模式。
"""

import sqlite3
import time
import random
from datetime import datetime, timedelta

def setup_database():
    """创建并初始化数据库"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建用户表（OLTP场景）
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 创建订单表（OLTP场景）
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # 插入测试数据
    for i in range(1000):
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (f"用户{i}", f"user{i}@example.com")
        )

    # 为每个用户创建随机订单
    for user_id in range(1, 1001):
        order_count = random.randint(1, 10)
        for _ in range(order_count):
            amount = round(random.uniform(10, 1000), 2)
            status = random.choice(['pending', 'completed', 'cancelled'])
            cursor.execute(
                "INSERT INTO orders (user_id, amount, status) VALUES (?, ?, ?)",
                (user_id, amount, status)
            )

    conn.commit()
    return conn

def oltp_query_example(conn):
    """OLTP查询示例：查找特定用户的订单"""
    print("=== OLTP 查询示例 ===")
    print("查询：查找用户ID为500的所有订单")

    start_time = time.time()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.amount, o.status, u.name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE u.id = ?
    """, (500,))

    results = cursor.fetchall()
    end_time = time.time()

    print(f"找到 {len(results)} 个订单")
    print(f"查询耗时: {(end_time - start_time) * 1000:.2f} 毫秒")
    print(f"示例结果: {results[:2]}")  # 只显示前2个
    print()

def olap_query_example(conn):
    """OLAP查询示例：分析所有用户的订单统计"""
    print("=== OLAP 查询示例 ===")
    print("查询：按状态统计订单数量和总金额")

    start_time = time.time()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            status,
            COUNT(*) as order_count,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM orders
        GROUP BY status
        ORDER BY total_amount DESC
    """)

    results = cursor.fetchall()
    end_time = time.time()

    print("订单统计结果:")
    for row in results:
        print(f"  状态: {row[0]}, 数量: {row[1]}, 总金额: {row[2]:.2f}, 平均金额: {row[3]:.2f}")

    print(f"查询耗时: {(end_time - start_time) * 1000:.2f} 毫秒")
    print()

def main():
    """主函数"""
    print("OLTP vs OLAP 查询对比演示")
    print("=" * 50)

    # 设置数据库
    conn = setup_database()

    # 执行OLTP查询
    oltp_query_example(conn)

    # 执行OLAP查询
    olap_query_example(conn)

    # 关闭连接
    conn.close()

    print("演示完成！")
    print("\n关键区别总结:")
    print("- OLTP: 快速、简单、基于主键/索引的查询")
    print("- OLAP: 复杂、聚合、全表扫描或大范围扫描")
    print("- OLTP关注单条记录，OLAP关注整体趋势")

if __name__ == "__main__":
    main()