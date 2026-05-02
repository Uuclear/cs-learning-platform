#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 索引性能对比
这个脚本使用SQLite演示有索引和无索引情况下查询性能的巨大差异。
"""

import sqlite3
import time
import random
from typing import List, Tuple


def create_test_database() -> sqlite3.Connection:
    """
    创建测试数据库并填充大量数据

    Returns:
        SQLite数据库连接
    """
    # 创建内存数据库（更快）
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            age INTEGER,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 生成大量测试数据
    print("🔧 正在生成测试数据...")
    users_data: List[Tuple] = []

    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安']
    names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']

    for i in range(10000):  # 10,000条记录
        name = f"{random.choice(names)}{i}"
        email = f"user{i}@example.com"
        age = random.randint(18, 80)
        city = random.choice(cities)
        users_data.append((name, email, age, city))

    # 批量插入数据
    cursor.executemany(
        'INSERT INTO users (name, email, age, city) VALUES (?, ?, ?, ?)',
        users_data
    )

    conn.commit()
    print(f"✅ 成功插入 {len(users_data)} 条用户记录")

    return conn


def test_query_without_index(conn: sqlite3.Connection) -> float:
    """
    测试没有索引情况下的查询性能

    Args:
        conn: 数据库连接

    Returns:
        查询耗时（秒）
    """
    cursor = conn.cursor()

    # 先确保没有索引
    cursor.execute("DROP INDEX IF EXISTS idx_users_email")
    cursor.execute("DROP INDEX IF EXISTS idx_users_age")
    cursor.execute("DROP INDEX IF EXISTS idx_users_city")
    conn.commit()

    print("\n🔍 测试无索引查询性能...")

    # 测试点查询（通过email查找）
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE email = 'user5000@example.com'")
    result = cursor.fetchall()
    end_time = time.time()

    query_time = end_time - start_time
    print(f"  邮箱查询 (user5000@example.com): 找到 {len(result)} 条记录, 耗时 {query_time:.4f} 秒")

    # 测试范围查询（年龄范围）
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE age BETWEEN 25 AND 35")
    result = cursor.fetchall()
    end_time = time.time()

    range_time = end_time - start_time
    print(f"  年龄范围查询 (25-35岁): 找到 {len(result)} 条记录, 耗时 {range_time:.4f} 秒")

    # 测试模糊查询（城市）
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE city = '北京'")
    result = cursor.fetchall()
    end_time = time.time()

    city_time = end_time - start_time
    print(f"  城市查询 (北京): 找到 {len(result)} 条记录, 耗时 {city_time:.4f} 秒")

    total_time = query_time + range_time + city_time
    print(f"  无索引总耗时: {total_time:.4f} 秒")

    return total_time


def test_query_with_index(conn: sqlite3.Connection) -> float:
    """
    测试有索引情况下的查询性能

    Args:
        conn: 数据库连接

    Returns:
        查询耗时（秒）
    """
    cursor = conn.cursor()

    # 创建索引
    print("\n🔧 创建索引...")
    cursor.execute("CREATE INDEX idx_users_email ON users(email)")
    cursor.execute("CREATE INDEX idx_users_age ON users(age)")
    cursor.execute("CREATE INDEX idx_users_city ON users(city)")
    conn.commit()
    print("✅ 索引创建完成")

    print("\n🔍 测试有索引查询性能...")

    # 测试点查询（通过email查找）
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE email = 'user5000@example.com'")
    result = cursor.fetchall()
    end_time = time.time()

    query_time = end_time - start_time
    print(f"  邮箱查询 (user5000@example.com): 找到 {len(result)} 条记录, 耗时 {query_time:.4f} 秒")

    # 测试范围查询（年龄范围）
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE age BETWEEN 25 AND 35")
    result = cursor.fetchall()
    end_time = time.time()

    range_time = end_time - start_time
    print(f"  年龄范围查询 (25-35岁): 找到 {len(result)} 条记录, 耗时 {range_time:.4f} 秒")

    # 测试模糊查询（城市）
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE city = '北京'")
    result = cursor.fetchall()
    end_time = time.time()

    city_time = end_time - start_time
    print(f"  城市查询 (北京): 找到 {len(result)} 条记录, 耗时 {city_time:.4f} 秒")

    total_time = query_time + range_time + city_time
    print(f"  有索引总耗时: {total_time:.4f} 秒")

    return total_time


def analyze_query_plan(conn: sqlite3.Connection) -> None:
    """
    分析查询执行计划，展示索引的使用情况

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    print("\n📊 查询执行计划分析:")

    # 显示无索引时的执行计划
    cursor.execute("DROP INDEX IF EXISTS idx_users_email")
    conn.commit()

    print("  无索引时的邮箱查询计划:")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com'")
    plan = cursor.fetchall()
    for row in plan:
        print(f"    {row}")

    # 显示有索引时的执行计划
    cursor.execute("CREATE INDEX idx_users_email ON users(email)")
    conn.commit()

    print("  有索引时的邮箱查询计划:")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com'")
    plan = cursor.fetchall()
    for row in plan:
        print(f"    {row}")


def main():
    """主函数：运行性能对比测试"""
    print("🚀 索引性能对比演示")
    print("=" * 60)

    # 创建测试数据库
    conn = create_test_database()

    try:
        # 测试无索引性能
        no_index_time = test_query_without_index(conn)

        # 测试有索引性能
        with_index_time = test_query_with_index(conn)

        # 计算性能提升
        if with_index_time > 0:
            speedup = no_index_time / with_index_time
            print(f"\n📈 性能提升: {speedup:.2f}x")
            print(f"   无索引: {no_index_time:.4f} 秒")
            print(f"   有索引: {with_index_time:.4f} 秒")

        # 分析查询计划
        analyze_query_plan(conn)

    finally:
        conn.close()

    print("\n💡 结论: 索引可以显著提升查询性能，特别是在大数据量的情况下！")


if __name__ == "__main__":
    main()