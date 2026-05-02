#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 复合索引实战
这个脚本演示复合索引（多列索引）的工作原理和最左前缀原则。
"""

import sqlite3
import time
from typing import List, Tuple


def create_composite_index_database() -> sqlite3.Connection:
    """
    创建用于复合索引测试的数据库

    Returns:
        SQLite数据库连接
    """
    # 创建内存数据库
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建订单表
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            status TEXT,
            amount DECIMAL(10,2),
            created_at TIMESTAMP,
            category TEXT
        )
    ''')

    # 插入测试数据
    print("🔧 正在生成订单测试数据...")
    orders_data: List[Tuple] = []

    statuses = ['pending', 'shipped', 'delivered', 'cancelled']
    categories = ['electronics', 'books', 'clothing', 'home']

    for i in range(5000):  # 5,000条订单记录
        user_id = (i % 100) + 1  # 100个用户
        status = random.choice(statuses)
        amount = round(random.uniform(10.0, 1000.0), 2)
        # 创建时间从最近30天内随机选择
        days_ago = random.randint(0, 30)
        created_at = f"2026-04-{30 - days_ago:02d} 12:00:00"
        category = random.choice(categories)
        orders_data.append((user_id, status, amount, created_at, category))

    cursor.executemany(
        'INSERT INTO orders (user_id, status, amount, created_at, category) VALUES (?, ?, ?, ?, ?)',
        orders_data
    )

    conn.commit()
    print(f"✅ 成功插入 {len(orders_data)} 条订单记录")

    return conn


def test_composite_index_scenarios(conn: sqlite3.Connection) -> None:
    """
    测试复合索引的各种使用场景

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    # 创建复合索引: (user_id, status, created_at)
    print("\n🔧 创建复合索引 (user_id, status, created_at)...")
    cursor.execute('''
        CREATE INDEX idx_orders_user_status_time
        ON orders(user_id, status, created_at)
    ''')
    conn.commit()
    print("✅ 复合索引创建完成")

    print("\n🔍 测试复合索引的各种查询场景:")

    # 场景1: 使用最左列 (user_id) - ✅ 应该使用索引
    print("\n1. 仅使用最左列 (user_id = 50):")
    start_time = time.time()
    cursor.execute("SELECT * FROM orders WHERE user_id = 50")
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    # 查看执行计划
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 50")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 场景2: 使用最左两列 (user_id, status) - ✅ 应该使用索引
    print("\n2. 使用最左两列 (user_id = 50 AND status = 'delivered'):")
    start_time = time.time()
    cursor.execute("SELECT * FROM orders WHERE user_id = 50 AND status = 'delivered'")
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 50 AND status = 'delivered'")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 场景3: 使用所有三列 - ✅ 应该使用索引
    print("\n3. 使用所有三列 (user_id = 50 AND status = 'delivered' AND created_at > '2026-04-15'):")
    start_time = time.time()
    cursor.execute("""
        SELECT * FROM orders
        WHERE user_id = 50
        AND status = 'delivered'
        AND created_at > '2026-04-15 00:00:00'
    """)
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("""
        EXPLAIN QUERY PLAN SELECT * FROM orders
        WHERE user_id = 50
        AND status = 'delivered'
        AND created_at > '2026-04-15 00:00:00'
    """)
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 场景4: 跳过最左列，只使用中间列 (status) - ❌ 不应该使用索引
    print("\n4. 跳过最左列，仅使用中间列 (status = 'delivered'):")
    start_time = time.time()
    cursor.execute("SELECT * FROM orders WHERE status = 'delivered'")
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'delivered'")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 场景5: 跳过中间列，使用最左和最右列 (user_id, created_at) - ⚠️ 部分使用索引
    print("\n5. 跳过中间列，使用最左和最右列 (user_id = 50 AND created_at > '2026-04-15'):")
    start_time = time.time()
    cursor.execute("""
        SELECT * FROM orders
        WHERE user_id = 50
        AND created_at > '2026-04-15 00:00:00'
    """)
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("""
        EXPLAIN QUERY PLAN SELECT * FROM orders
        WHERE user_id = 50
        AND created_at > '2026-04-15 00:00:00'
    """)
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 场景6: 只使用最右列 (created_at) - ❌ 不应该使用索引
    print("\n6. 仅使用最右列 (created_at > '2026-04-15'):")
    start_time = time.time()
    cursor.execute("SELECT * FROM orders WHERE created_at > '2026-04-15 00:00:00'")
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE created_at > '2026-04-15 00:00:00'")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")


def demonstrate_covering_index(conn: sqlite3.Connection) -> None:
    """
    演示覆盖索引的概念

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    # 创建覆盖索引: 包含查询所需的所有列
    print("\n" + "="*60)
    print("📊 覆盖索引演示")
    print("创建覆盖索引 (user_id, status, amount)...")

    cursor.execute('DROP INDEX IF EXISTS idx_orders_covering')
    cursor.execute('''
        CREATE INDEX idx_orders_covering
        ON orders(user_id, status, amount)
    ''')
    conn.commit()

    # 查询只需要索引中的列
    print("\n查询只需要索引中的列 (SELECT user_id, status, amount WHERE user_id = 50):")
    start_time = time.time()
    cursor.execute("SELECT user_id, status, amount FROM orders WHERE user_id = 50")
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("EXPLAIN QUERY PLAN SELECT user_id, status, amount FROM orders WHERE user_id = 50")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")
    print("   💡 注意: 这个查询可以直接从索引中获取所有数据，无需访问表数据（覆盖索引）")

    # 对比需要回表的查询
    print("\n对比需要回表的查询 (SELECT * WHERE user_id = 50):")
    start_time = time.time()
    cursor.execute("SELECT * FROM orders WHERE user_id = 50")
    result = cursor.fetchall()
    end_time = time.time()
    print(f"   找到 {len(result)} 条记录, 耗时 {end_time - start_time:.4f} 秒")

    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 50")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")
    print("   💡 注意: 这个查询需要回表获取完整数据行")


def main():
    """主函数：运行复合索引演示"""
    print("📚 复合索引实战演示")
    print("=" * 60)
    print("复合索引遵循最左前缀原则：")
    print("  - ✅ 可以使用: 最左列、最左连续多列")
    print("  - ❌ 无法使用: 跳过最左列、非连续列")
    print("  - ⚠️ 部分使用: 最左列 + 后续非连续列（只能利用最左部分）")

    # 导入random模块
    global random
    import random

    # 创建测试数据库
    conn = create_composite_index_database()

    try:
        # 测试复合索引场景
        test_composite_index_scenarios(conn)

        # 演示覆盖索引
        demonstrate_covering_index(conn)

    finally:
        conn.close()

    print("\n🎯 关键结论:")
    print("1. 复合索引必须从最左边开始连续使用才能有效")
    print("2. 覆盖索引可以避免回表操作，显著提升查询性能")
    print("3. 设计复合索引时，要考虑实际的查询模式和列的选择性")


if __name__ == "__main__":
    main()