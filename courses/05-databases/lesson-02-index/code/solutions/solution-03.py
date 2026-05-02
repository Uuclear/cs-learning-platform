#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 索引失效分析

演示索引失效的情况并提供优化方案。
"""

import sqlite3
import time

def create_orders_table():
    """创建订单表"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建订单表
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,  -- 存储为 'YYYY-MM-DD' 格式
            amount REAL,
            status TEXT
        )
    ''')

    # 插入测试数据
    orders_data = [
        (1, 1001, '2026-01-15', 99.99, 'completed'),
        (2, 1002, '2026-02-20', 149.50, 'completed'),
        (3, 1003, '2026-03-10', 75.25, 'pending'),
        (4, 1004, '2026-04-05', 200.00, 'completed'),
        (5, 1005, '2026-05-01', 50.75, 'cancelled')
    ]

    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', orders_data)
    conn.commit()

    return conn, cursor

def demonstrate_index_failure():
    """演示索引失效的情况"""
    conn, cursor = create_orders_table()

    # 创建日期索引
    cursor.execute('CREATE INDEX idx_order_date ON orders(order_date)')
    print("索引 idx_order_date 已创建\n")

    # 情况1: 在索引列上使用函数（索引失效）
    print("=== 情况1: 使用函数导致索引失效 ===")
    print("查询: SELECT * FROM orders WHERE strftime('%Y', order_date) = '2026'")

    cursor.execute('EXPLAIN QUERY PLAN SELECT * FROM orders WHERE strftime("%Y", order_date) = "2026"')
    plan1 = cursor.fetchall()
    print("查询计划:", plan1)
    print("❌ 索引失效！因为对order_date使用了strftime函数\n")

    # 情况2: 类型不匹配（索引可能失效）
    print("=== 情况2: 类型不匹配 ===")
    print("查询: SELECT * FROM orders WHERE order_date = 20260115")  # 数字 vs 字符串

    cursor.execute('EXPLAIN QUERY PLAN SELECT * FROM orders WHERE order_date = 20260115')
    plan2 = cursor.fetchall()
    print("查询计划:", plan2)
    print("⚠️ 可能索引失效！因为类型不匹配\n")

    # 优化方案1: 使用范围查询代替函数
    print("=== 优化方案1: 范围查询代替函数 ===")
    print("查询: SELECT * FROM orders WHERE order_date BETWEEN '2026-01-01' AND '2026-12-31'")

    cursor.execute('''
        EXPLAIN QUERY PLAN
        SELECT * FROM orders WHERE order_date BETWEEN '2026-01-01' AND '2026-12-31'
    ''')
    plan3 = cursor.fetchall()
    print("查询计划:", plan3)
    print("✅ 成功使用索引！\n")

    # 优化方案2: 确保类型匹配
    print("=== 优化方案2: 确保类型匹配 ===")
    print("查询: SELECT * FROM orders WHERE order_date = '2026-01-15'")

    cursor.execute('EXPLAIN QUERY PLAN SELECT * FROM orders WHERE order_date = "2026-01-15"')
    plan4 = cursor.fetchall()
    print("查询计划:", plan4)
    print("✅ 成功使用索引！\n")

    # 额外优化: 创建函数索引（SQLite 3.8.7+ 支持）
    print("=== 额外优化: 函数索引 ===")
    try:
        cursor.execute('CREATE INDEX idx_year ON orders(strftime("%Y", order_date))')
        print("函数索引 idx_year 创建成功！")

        cursor.execute('EXPLAIN QUERY PLAN SELECT * FROM orders WHERE strftime("%Y", order_date) = "2026"')
        plan5 = cursor.fetchall()
        print("使用函数索引的查询计划:", plan5)
        print("✅ 函数索引可以解决特定场景的问题！")
    except sqlite3.OperationalError as e:
        print(f"⚠️ 当前SQLite版本可能不支持函数索引: {e}")

    conn.close()

def main():
    print("=== 索引失效分析与优化 ===\n")
    demonstrate_index_failure()
    print("\n💡 总结:")
    print("   1. 避免在索引列上使用函数或表达式")
    print("   2. 确保查询条件的数据类型与列类型匹配")
    print("   3. 使用范围查询代替函数操作")
    print("   4. 某些数据库支持函数索引作为特殊解决方案")

if __name__ == "__main__":
    main()