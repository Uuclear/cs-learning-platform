#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1: 电商系统索引设计
为给定的电商查询模式设计最优的索引策略。
"""

import sqlite3
from typing import List, Dict, Any


def analyze_ecommerce_queries() -> Dict[str, List[str]]:
    """
    分析电商系统的典型查询模式

    Returns:
        包含各种查询场景的字典
    """
    queries = {
        "user_orders": [
            "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
            "SELECT * FROM orders WHERE user_id = ? AND status = ?",
            "SELECT COUNT(*) FROM orders WHERE user_id = ?"
        ],
        "product_search": [
            "SELECT * FROM products WHERE category = ? AND price BETWEEN ? AND ?",
            "SELECT * FROM products WHERE name LIKE ?",
            "SELECT * FROM products WHERE brand = ? ORDER BY price"
        ],
        "admin_reports": [
            "SELECT status, COUNT(*) FROM orders GROUP BY status",
            "SELECT DATE(created_at), COUNT(*) FROM orders WHERE created_at >= ? GROUP BY DATE(created_at)",
            "SELECT p.category, SUM(o.amount) FROM orders o JOIN products p ON o.product_id = p.id WHERE o.created_at >= ? GROUP BY p.category"
        ],
        "popular_items": [
            "SELECT product_id, COUNT(*) as order_count FROM orders WHERE created_at >= ? GROUP BY product_id ORDER BY order_count DESC LIMIT 10",
            "SELECT category, AVG(rating) FROM products GROUP BY category"
        ]
    }

    return queries


def create_optimal_indexes(conn: sqlite3.Connection) -> None:
    """
    为电商系统创建最优的索引

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    print("🔧 为电商系统创建最优索引...")

    # 订单表索引
    # 1. 用户订单查询: (user_id, created_at) - 支持按用户和时间排序
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_orders_user_created
        ON orders(user_id, created_at DESC)
    ''')

    # 2. 用户+状态查询: (user_id, status, created_at) - 支持复合条件
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_orders_user_status_created
        ON orders(user_id, status, created_at DESC)
    ''')

    # 3. 管理员报表: (created_at, status) - 支持时间范围和状态分组
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_orders_created_status
        ON orders(created_at, status)
    ''')

    # 4. 热门商品统计: (created_at, product_id) - 支持时间范围内的商品统计
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_orders_created_product
        ON orders(created_at, product_id)
    ''')

    # 商品表索引
    # 5. 商品搜索: (category, price) - 支持分类和价格范围查询
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_products_category_price
        ON products(category, price)
    ''')

    # 6. 品牌查询: (brand, price) - 支持品牌查询和价格排序
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_products_brand_price
        ON products(brand, price)
    ''')

    # 7. 覆盖索引: (category, rating) - 支持分类评分统计，避免回表
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_products_category_rating
        ON products(category, rating)
    ''')

    # 全文搜索需要特殊处理，这里使用简单的name索引
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_products_name
        ON products(name)
    ''')

    conn.commit()
    print("✅ 所有最优索引创建完成")


def create_sample_ecommerce_schema(conn: sqlite3.Connection) -> None:
    """
    创建电商系统的示例表结构

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    # 创建订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP
        )
    ''')

    # 创建商品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            rating DECIMAL(2,1),
            stock_quantity INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    ''')

    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    ''')

    conn.commit()


def demonstrate_index_usage(conn: sqlite3.Connection) -> None:
    """
    演示索引在实际查询中的使用

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    print("\n🔍 演示索引使用情况:")

    # 示例1: 用户订单查询（应该使用 idx_orders_user_created）
    print("\n1. 用户订单查询:")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 示例2: 商品分类+价格查询（应该使用 idx_products_category_price）
    print("\n2. 商品分类+价格查询:")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM products WHERE category = 'electronics' AND price BETWEEN 100 AND 500")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")

    # 示例3: 时间范围订单统计（应该使用 idx_orders_created_status）
    print("\n3. 时间范围订单统计:")
    cursor.execute("EXPLAIN QUERY PLAN SELECT status, COUNT(*) FROM orders WHERE created_at >= '2026-01-01' GROUP BY status")
    plan = cursor.fetchall()
    print(f"   执行计划: {plan}")


def evaluate_index_strategy() -> None:
    """
    评估索引策略的有效性
    """
    print("\n📊 索引策略评估:")
    print("优点:")
    print("  ✅ 覆盖了所有主要查询模式")
    print("  ✅ 使用复合索引减少索引数量")
    print("  ✅ 考虑了排序需求（DESC）")
    print("  ✅ 包含覆盖索引避免回表")
    print("  ✅ 针对高频查询优化")

    print("\n注意事项:")
    print("  ⚠️ 索引会增加写操作开销")
    print("  ⚠️ 需要定期监控索引使用情况")
    print("  ⚠️ 对于全文搜索，可能需要专门的搜索引擎")
    print("  ⚠️ 根据实际数据分布调整索引顺序")


def main():
    """主函数：运行电商索引设计解决方案"""
    print("🎯 电商系统最优索引设计方案")
    print("=" * 50)

    # 分析查询模式
    queries = analyze_ecommerce_queries()
    print("📋 识别的查询模式:")
    for scenario, query_list in queries.items():
        print(f"  {scenario}: {len(query_list)} 个查询")

    # 创建数据库连接
    conn = sqlite3.connect(':memory:')

    try:
        # 创建表结构
        create_sample_ecommerce_schema(conn)

        # 创建最优索引
        create_optimal_indexes(conn)

        # 演示索引使用
        demonstrate_index_usage(conn)

        # 评估策略
        evaluate_index_strategy()

    finally:
        conn.close()

    print("\n💡 结论: 通过分析实际查询模式，我们可以设计出高效的索引策略，")
    print("   在保证查询性能的同时，避免过度索引带来的维护开销。")


if __name__ == "__main__":
    main()