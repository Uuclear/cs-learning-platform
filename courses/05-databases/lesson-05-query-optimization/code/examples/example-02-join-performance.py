#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: 连接性能对比

本脚本演示不同连接算法的性能差异，比较嵌套循环连接、
索引连接等在不同数据量下的表现。
"""

import sqlite3
import time
import random
from typing import List, Tuple


def create_sample_data(conn: sqlite3.Connection, users_count: int = 10000, orders_count: int = 50000) -> None:
    """创建示例数据表并填充指定数量的数据"""
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 创建订单表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            product_category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print(f"示例数据已存在 ({users_count} 用户, {orders_count} 订单)，跳过数据生成...")
        return

    print(f"正在生成 {users_count} 个用户和 {orders_count} 个订单...")

    # 生成用户数据
    users_data = []
    departments = list(range(1, 101))  # 100个部门
    for i in range(users_count):
        name = f"用户{i:05d}"
        email = f"user{i:05d}@company.com"
        department_id = random.choice(departments)
        users_data.append((name, email, department_id))

    cursor.executemany(
        "INSERT INTO users (name, email, department_id) VALUES (?, ?, ?)",
        users_data
    )

    # 生成订单数据
    orders_data = []
    categories = ['electronics', 'clothing', 'books', 'home', 'sports', 'beauty']
    for i in range(orders_count):
        user_id = random.randint(1, users_count)
        amount = round(random.uniform(10, 1000), 2)
        category = random.choice(categories)
        orders_data.append((user_id, amount, category))

    cursor.executemany(
        "INSERT INTO orders (user_id, amount, product_category) VALUES (?, ?, ?)",
        orders_data
    )

    conn.commit()
    print("示例数据生成完成!")


def measure_query_performance(conn: sqlite3.Connection, query: str, description: str, iterations: int = 3) -> float:
    """测量查询性能，返回平均执行时间（毫秒）"""
    print(f"\n⚡ {description}")
    print(f"查询语句: {query}")

    cursor = conn.cursor()
    total_time = 0.0

    for i in range(iterations):
        # 清除缓存影响（SQLite 中通过重新准备语句）
        start_time = time.time()
        cursor.execute(query)
        results = cursor.fetchall()
        end_time = time.time()

        execution_time = (end_time - start_time) * 1000  # 转换为毫秒
        total_time += execution_time

        if i == 0:  # 只在第一次显示结果数量
            print(f"返回行数: {len(results)}")

    avg_time = total_time / iterations
    print(f"平均执行时间 ({iterations} 次): {avg_time:.2f} ms")
    return avg_time


def test_nested_loop_join(conn: sqlite3.Connection) -> None:
    """测试嵌套循环连接性能"""
    # 强制使用嵌套循环（SQLite 默认可能选择其他算法）
    # 在没有合适索引的情况下，会使用嵌套循环
    query = """
        SELECT u.name, o.amount, o.product_category
        FROM users u, orders o
        WHERE u.id = o.user_id
        AND u.department_id = 42
    """
    measure_query_performance(conn, query, "嵌套循环连接 (无索引优化)")


def test_indexed_join(conn: sqlite3.Connection) -> None:
    """测试索引连接性能"""
    # 创建索引后，SQLite 会使用更高效的连接算法
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_department ON users(department_id)")
    conn.commit()

    query = """
        SELECT u.name, o.amount, o.product_category
        FROM users u
        JOIN orders o ON u.id = o.user_id
        WHERE u.department_id = 42
    """
    measure_query_performance(conn, query, "索引连接 (有索引优化)")


def test_hash_like_join(conn: sqlite3.Connection) -> None:
    """测试类似哈希连接的性能（通过临时表和索引）"""
    cursor = conn.cursor()

    # 创建临时筛选表
    cursor.execute("""
        CREATE TEMP TABLE temp_filtered_users AS
        SELECT id, name FROM users WHERE department_id = 42
    """)
    cursor.execute("CREATE INDEX idx_temp_users ON temp_filtered_users(id)")

    query = """
        SELECT t.name, o.amount, o.product_category
        FROM temp_filtered_users t
        JOIN orders o ON t.id = o.user_id
    """
    measure_query_performance(conn, query, "临时表连接 (类似哈希连接)")

    # 清理临时表
    cursor.execute("DROP TABLE temp_filtered_users")


def compare_join_algorithms() -> None:
    """比较不同连接算法的性能"""
    print("🔄 示例 2: 连接性能对比")
    print("=" * 60)
    print("本示例将比较不同连接算法在大数据量下的性能表现")

    # 使用内存数据库进行快速测试
    conn = sqlite3.connect(":memory:")

    try:
        # 创建大量示例数据
        create_sample_data(conn, users_count=10000, orders_count=50000)

        # 测试各种连接算法
        nested_time = test_nested_loop_join(conn)
        indexed_time = test_indexed_join(conn)
        hash_time = test_hash_like_join(conn)

        print("\n📈 性能对比总结:")
        print(f"嵌套循环连接:     {nested_time:.2f} ms")
        print(f"索引连接:         {indexed_time:.2f} ms")
        print(f"临时表连接:       {hash_time:.2f} ms")

        # 计算性能提升
        if nested_time > 0:
            indexed_improvement = (nested_time - indexed_time) / nested_time * 100
            hash_improvement = (nested_time - hash_time) / nested_time * 100
            print(f"\n💡 性能提升:")
            print(f"索引连接相比嵌套循环提升: {indexed_improvement:.1f}%")
            print(f"临时表连接相比嵌套循环提升: {hash_improvement:.1f}%")

        print("\n🔍 关键观察:")
        print("- 嵌套循环连接的时间复杂度接近 O(n*m)")
        print("- 索引连接通过索引快速定位，大大减少扫描行数")
        print("- 适当的索引设计对连接性能至关重要")
        print("- SQLite 会自动选择最优的连接算法，但需要合适的索引支持")

    finally:
        conn.close()


def main() -> None:
    """主函数"""
    compare_join_algorithms()


if __name__ == "__main__":
    main()