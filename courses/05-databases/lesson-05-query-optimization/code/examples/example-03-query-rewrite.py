#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: 查询重写优化

本脚本演示如何通过重写查询来提升性能，包括：
- 子查询转 JOIN
- EXISTS 转 JOIN
- 避免 SELECT *
- 使用 LIMIT 限制结果集
"""

import sqlite3
import time
import random
from typing import List, Tuple


def create_sample_data(conn: sqlite3.Connection) -> None:
    """创建示例数据表并填充数据"""
    cursor = conn.cursor()

    # 创建产品表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock_quantity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 创建订单表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer_id INTEGER,
            quantity INTEGER,
            status TEXT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # 创建客户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        print("示例数据已存在，跳过数据生成...")
        return

    print("正在生成示例数据...")

    # 生成产品数据 (5000+ 行)
    products_data = []
    categories = ['electronics', 'clothing', 'books', 'home', 'sports', 'beauty', 'toys', 'food']
    for i in range(5000):
        name = f"产品{i:04d}"
        category = random.choice(categories)
        price = round(random.uniform(10, 1000), 2)
        stock_quantity = random.randint(0, 1000)
        products_data.append((name, category, price, stock_quantity))

    cursor.executemany(
        "INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)",
        products_data
    )

    # 生成客户数据 (10000+ 行)
    customers_data = []
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '重庆']
    for i in range(10000):
        name = f"客户{i:05d}"
        email = f"customer{i:05d}@example.com"
        city = random.choice(cities)
        customers_data.append((name, email, city))

    cursor.executemany(
        "INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
        customers_data
    )

    # 生成订单数据 (50000+ 行)
    orders_data = []
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    for i in range(50000):
        product_id = random.randint(1, 5000)
        customer_id = random.randint(1, 10000)
        quantity = random.randint(1, 10)
        status = random.choice(statuses)
        orders_data.append((product_id, customer_id, quantity, status))

    cursor.executemany(
        "INSERT INTO orders (product_id, customer_id, quantity, status) VALUES (?, ?, ?, ?)",
        orders_data
    )

    # 创建索引
    cursor.execute("CREATE INDEX idx_products_category ON products(category)")
    cursor.execute("CREATE INDEX idx_orders_product_id ON orders(product_id)")
    cursor.execute("CREATE INDEX idx_orders_customer_id ON orders(customer_id)")
    cursor.execute("CREATE INDEX idx_orders_status ON orders(status)")
    cursor.execute("CREATE INDEX idx_customers_city ON customers(city)")

    conn.commit()
    print(f"成功生成 {len(products_data)} 个产品, {len(customers_data)} 个客户, {len(orders_data)} 个订单")


def measure_and_compare(conn: sqlite3.Connection, slow_query: str, optimized_query: str, description: str) -> None:
    """测量并比较慢查询和优化后查询的性能"""
    print(f"\n🔄 {description}")
    print("-" * 50)

    # 测试慢查询
    print("🐢 慢查询版本:")
    print(f"  {slow_query}")
    slow_time = measure_query_performance(conn, slow_query, "慢查询")

    # 测试优化查询
    print("\n🚀 优化查询版本:")
    print(f"  {optimized_query}")
    fast_time = measure_query_performance(conn, optimized_query, "优化查询")

    # 显示性能对比
    if slow_time > 0:
        improvement = (slow_time - fast_time) / slow_time * 100
        print(f"\n📈 性能提升: {improvement:.1f}%")
        print(f"⏱️  时间减少: {(slow_time - fast_time):.2f} ms")


def measure_query_performance(conn: sqlite3.Connection, query: str, label: str, iterations: int = 3) -> float:
    """测量查询性能"""
    cursor = conn.cursor()
    total_time = 0.0

    for i in range(iterations):
        start_time = time.time()
        cursor.execute(query)
        results = cursor.fetchall()
        end_time = time.time()
        total_time += (end_time - start_time) * 1000

        if i == 0:
            print(f"{label} - 返回行数: {len(results)}")

    avg_time = total_time / iterations
    print(f"{label} - 平均时间: {avg_time:.2f} ms")
    return avg_time


def demonstrate_subquery_to_join() -> None:
    """演示子查询转 JOIN 的优化"""
    print("\n📊 优化技术 1: 子查询转 JOIN")

    slow_query = """
        SELECT * FROM products
        WHERE id IN (
            SELECT product_id FROM orders
            WHERE status = 'delivered'
        )
    """

    optimized_query = """
        SELECT DISTINCT p.*
        FROM products p
        INNER JOIN orders o ON p.id = o.product_id
        WHERE o.status = 'delivered'
    """

    return slow_query, optimized_query, "子查询转 JOIN"


def demonstrate_exists_to_join() -> None:
    """演示 EXISTS 转 JOIN 的优化"""
    print("\n📊 优化技术 2: EXISTS 转 JOIN")

    slow_query = """
        SELECT * FROM customers c
        WHERE EXISTS (
            SELECT 1 FROM orders o
            WHERE o.customer_id = c.id
            AND o.status = 'delivered'
        )
    """

    optimized_query = """
        SELECT DISTINCT c.*
        FROM customers c
        INNER JOIN orders o ON c.id = o.customer_id
        WHERE o.status = 'delivered'
    """

    return slow_query, optimized_query, "EXISTS 转 JOIN"


def demonstrate_select_star_optimization() -> None:
    """演示避免 SELECT * 的优化"""
    print("\n📊 优化技术 3: 避免 SELECT *")

    slow_query = """
        SELECT * FROM products
        WHERE category = 'electronics'
        ORDER BY price DESC
        LIMIT 10
    """

    optimized_query = """
        SELECT id, name, price
        FROM products
        WHERE category = 'electronics'
        ORDER BY price DESC
        LIMIT 10
    """

    return slow_query, optimized_query, "只选择需要的列"


def demonstrate_limit_optimization() -> None:
    """演示使用 LIMIT 的优化"""
    print("\n📊 优化技术 4: 合理使用 LIMIT")

    slow_query = """
        SELECT p.name, c.name as customer_name, o.quantity, o.order_date
        FROM orders o
        JOIN products p ON o.product_id = p.id
        JOIN customers c ON o.customer_id = c.id
        WHERE o.status = 'delivered'
        ORDER BY o.order_date DESC
    """

    optimized_query = """
        SELECT p.name, c.name as customer_name, o.quantity, o.order_date
        FROM orders o
        JOIN products p ON o.product_id = p.id
        JOIN customers c ON o.customer_id = c.id
        WHERE o.status = 'delivered'
        ORDER BY o.order_date DESC
        LIMIT 50
    """

    return slow_query, optimized_query, "添加 LIMIT 限制结果集"


def main() -> None:
    """主函数"""
    print("🔄 示例 3: 查询重写优化")
    print("=" * 60)

    # 使用内存数据库
    conn = sqlite3.connect(":memory:")

    try:
        # 创建示例数据
        create_sample_data(conn)

        # 获取各种优化示例
        examples = [
            demonstrate_subquery_to_join(),
            demonstrate_exists_to_join(),
            demonstrate_select_star_optimization(),
            demonstrate_limit_optimization()
        ]

        # 测试每个优化示例
        for slow_query, optimized_query, description in examples:
            measure_and_compare(conn, slow_query, optimized_query, description)

        print("\n💡 查询重写优化总结:")
        print("- 子查询通常比 JOIN 慢，因为可能重复执行")
        print("- EXISTS 可以转换为 JOIN 来利用索引")
        print("- 只选择需要的列可以减少 I/O 和网络传输")
        print("- 合理使用 LIMIT 可以避免处理不必要的数据")
        print("- 优化器有时无法自动进行这些转换，需要手动重写")

        print("\n🔍 最佳实践:")
        print("1. 优先使用 JOIN 而不是子查询")
        print("2. 避免 SELECT *，明确指定需要的列")
        print("3. 在分页查询中总是使用 LIMIT")
        print("4. 复杂查询先用 EXPLAIN 分析执行计划")
        print("5. 定期测试和验证优化效果")

    finally:
        conn.close()


if __name__ == "__main__":
    main()