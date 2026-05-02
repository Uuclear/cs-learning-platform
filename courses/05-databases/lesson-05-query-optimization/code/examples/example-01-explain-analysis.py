#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: EXPLAIN 分析不同查询

本脚本演示如何使用 SQLite 的 EXPLAIN QUERY PLAN 功能来分析
不同查询的执行计划，理解索引的使用情况。
"""

import sqlite3
import time
import random
from typing import List, Tuple


def create_sample_data(conn: sqlite3.Connection) -> None:
    """创建示例数据表并填充数据"""
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 创建订单表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_name TEXT,
            amount REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("示例数据已存在，跳过数据生成...")
        return

    print("正在生成示例数据...")

    # 生成用户数据 (10000+ 行)
    users_data = []
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安']
    for i in range(10000):
        name = f"用户{i:04d}"
        email = f"user{i:04d}@example.com"
        age = random.randint(18, 80)
        city = random.choice(cities)
        users_data.append((name, email, age, city))

    cursor.executemany(
        "INSERT INTO users (name, email, age, city) VALUES (?, ?, ?, ?)",
        users_data
    )

    # 生成订单数据 (20000+ 行)
    orders_data = []
    products = ['笔记本电脑', '手机', '平板', '耳机', '键盘', '鼠标', '显示器']
    statuses = ['pending', 'shipped', 'delivered', 'cancelled']
    for i in range(20000):
        user_id = random.randint(1, 10000)
        product_name = random.choice(products)
        amount = round(random.uniform(10, 5000), 2)
        status = random.choice(statuses)
        orders_data.append((user_id, product_name, amount, status))

    cursor.executemany(
        "INSERT INTO orders (user_id, product_name, amount, status) VALUES (?, ?, ?, ?)",
        orders_data
    )

    conn.commit()
    print(f"成功生成 {len(users_data)} 个用户和 {len(orders_data)} 个订单")


def analyze_query_plan(conn: sqlite3.Connection, query: str, description: str) -> None:
    """分析单个查询的执行计划"""
    print(f"\n🔍 {description}")
    print(f"查询语句: {query}")

    # 获取执行计划
    cursor = conn.cursor()
    cursor.execute(f"EXPLAIN QUERY PLAN {query}")
    plan = cursor.fetchall()

    print("执行计划:")
    for row in plan:
        # EXPLAIN QUERY PLAN 返回 (id, parent, notused, detail)
        print(f"  {row[3]}")

    # 测量实际执行时间
    start_time = time.time()
    cursor.execute(query)
    results = cursor.fetchall()
    end_time = time.time()

    print(f"返回行数: {len(results)}")
    print(f"执行时间: {(end_time - start_time) * 1000:.2f} ms")


def main() -> None:
    """主函数"""
    print("📊 示例 1: EXPLAIN 分析不同查询")
    print("=" * 60)

    # 连接数据库
    conn = sqlite3.connect(":memory:")  # 使用内存数据库进行快速测试

    try:
        # 创建示例数据
        create_sample_data(conn)

        # 分析场景 1: 没有索引的查询 (全表扫描)
        analyze_query_plan(
            conn,
            "SELECT * FROM users WHERE email = 'user1234@example.com'",
            "场景 1: 按邮箱查询用户 (无索引)"
        )

        # 创建索引
        print("\n🔧 创建索引...")
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX idx_users_age ON users(age)")
        cursor.execute("CREATE INDEX idx_orders_user_id ON orders(user_id)")
        cursor.execute("CREATE INDEX idx_orders_status ON orders(status)")
        conn.commit()
        print("索引创建完成!")

        # 分析场景 2: 有索引的查询 (索引扫描)
        analyze_query_plan(
            conn,
            "SELECT * FROM users WHERE email = 'user1234@example.com'",
            "场景 2: 按邮箱查询用户 (有索引)"
        )

        # 分析场景 3: 范围查询
        analyze_query_plan(
            conn,
            "SELECT * FROM users WHERE age BETWEEN 25 AND 35",
            "场景 3: 按年龄范围查询 (有索引)"
        )

        # 分析场景 4: 复合条件查询
        analyze_query_plan(
            conn,
            "SELECT u.name, o.product_name, o.amount FROM users u JOIN orders o ON u.id = o.user_id WHERE u.age > 30 AND o.status = 'delivered'",
            "场景 4: JOIN 查询 (有索引)"
        )

        # 分析场景 5: 函数导致索引失效
        analyze_query_plan(
            conn,
            "SELECT * FROM users WHERE UPPER(email) = 'USER1234@EXAMPLE.COM'",
            "场景 5: 使用函数的查询 (索引失效)"
        )

        print("\n💡 关键观察:")
        print("- 全表扫描显示为 'SCAN TABLE'")
        print("- 索引扫描显示为 'SEARCH TABLE ... USING INDEX'")
        print("- 即使有索引，某些查询模式仍可能导致索引失效")
        print("- JOIN 查询会显示多个表的访问方式")

    finally:
        conn.close()


if __name__ == "__main__":
    main()