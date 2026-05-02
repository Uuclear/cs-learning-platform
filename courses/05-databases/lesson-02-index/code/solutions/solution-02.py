#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 复合索引优化

为products表创建复合索引并验证效果。
"""

import sqlite3
import time
import random

def create_products_table():
    """创建产品表并插入测试数据"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建产品表
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            brand TEXT
        )
    ''')

    # 生成5000条测试数据
    categories = ['electronics', 'books', 'clothing', 'food', 'sports']
    brands = ['brand_a', 'brand_b', 'brand_c', 'brand_d']

    products_data = []
    for i in range(5000):
        product = (
            i + 1,
            f"product_{i}",
            random.choice(categories),
            round(random.uniform(10, 1000), 2),
            random.choice(brands)
        )
        products_data.append(product)

    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products_data)
    conn.commit()

    return conn, cursor

def test_composite_index():
    """测试复合索引效果"""
    conn, cursor = create_products_table()

    # 测试无索引查询
    print("=== 无索引查询测试 ===")
    start_time = time.time()
    cursor.execute("""
        SELECT * FROM products
        WHERE category = 'electronics' AND price BETWEEN 100 AND 500
    """)
    results = cursor.fetchall()
    no_index_time = time.time() - start_time
    print(f"查询到 {len(results)} 条记录")
    print(f"无索引耗时: {no_index_time * 1000:.2f} 毫秒")

    # 创建复合索引（category在前，因为选择性更高）
    print("\n=== 创建复合索引 ===")
    cursor.execute('CREATE INDEX idx_cat_price ON products(category, price)')
    print("复合索引 idx_cat_price (category, price) 创建成功！")

    # 测试有索引查询
    print("\n=== 有索引查询测试 ===")
    start_time = time.time()
    cursor.execute("""
        SELECT * FROM products
        WHERE category = 'electronics' AND price BETWEEN 100 AND 500
    """)
    results = cursor.fetchall()
    with_index_time = time.time() - start_time
    print(f"查询到 {len(results)} 条记录")
    print(f"有索引耗时: {with_index_time * 1000:.2f} 毫秒")

    # 使用EXPLAIN验证索引使用
    print("\n=== EXPLAIN 查询计划 ===")
    cursor.execute("""
        EXPLAIN QUERY PLAN
        SELECT * FROM products
        WHERE category = 'electronics' AND price BETWEEN 100 AND 500
    """)
    plan = cursor.fetchall()
    print("查询计划:", plan)
    # 在SQLite中，如果使用了索引，会显示 "SEARCH TABLE ... USING INDEX ..."

    if with_index_time > 0:
        speedup = no_index_time / with_index_time
        print(f"\n🎉 性能提升: {speedup:.1f} 倍!")

    conn.close()

if __name__ == "__main__":
    test_composite_index()