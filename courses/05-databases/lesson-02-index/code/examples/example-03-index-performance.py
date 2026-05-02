#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 索引性能对比实验

全面测试索引对查询和写入性能的影响，展示索引的双面性。
"""

import sqlite3
import time
import random

def performance_test():
    """性能对比测试函数"""
    # 创建内存数据库
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建产品表
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            created_at TEXT
        )
    ''')

    print("正在生成10万条测试数据...")

    # 生成测试数据
    categories = ['electronics', 'books', 'clothing', 'food', 'sports']
    products_data = []
    for i in range(1, 100001):
        product = (
            i,
            f"product_{i}",
            random.choice(categories),
            round(random.uniform(1, 1000), 2),
            f"2026-01-{random.randint(1, 31):02d}"
        )
        products_data.append(product)

    # 批量插入数据
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products_data)
    conn.commit()
    print("测试数据准备完成！\n")

    # 测试1: 无索引查询性能
    print("=== 无索引查询测试 ===")
    start_time = time.time()
    cursor.execute("SELECT * FROM products WHERE category = 'electronics'")
    results1 = cursor.fetchall()
    time1 = time.time() - start_time
    print(f"查询到 {len(results1)} 条记录")
    print(f"耗时: {time1 * 1000:.2f} 毫秒")

    # 创建索引
    print("\n=== 创建索引 ===")
    cursor.execute('CREATE INDEX idx_category ON products(category)')
    print("索引 idx_category 创建成功！\n")

    # 测试2: 有索引查询性能
    print("=== 有索引查询测试 ===")
    start_time = time.time()
    cursor.execute("SELECT * FROM products WHERE category = 'electronics'")
    results2 = cursor.fetchall()
    time2 = time.time() - start_time
    print(f"查询到 {len(results2)} 条记录")
    print(f"耗时: {time2 * 1000:.2f} 毫秒")

    # 计算性能提升
    if time2 > 0:
        speedup = time1 / time2
        print(f"\n🎉 性能提升: {speedup:.1f} 倍!")

    # 测试写入性能影响
    print("\n=== 写入性能测试 ===")

    # 先删除索引测试无索引插入
    cursor.execute('DROP INDEX idx_category')
    start_time = time.time()
    cursor.execute('INSERT INTO products VALUES (?, ?, ?, ?, ?)',
                   (100001, "new_product", "electronics", 99.99, "2026-05-03"))
    insert_time_no_index = time.time() - start_time

    # 重新创建索引测试有索引插入
    cursor.execute('CREATE INDEX idx_category ON products(category)')
    start_time = time.time()
    cursor.execute('INSERT INTO products VALUES (?, ?, ?, ?, ?)',
                   (100002, "new_product2", "books", 88.88, "2026-05-03"))
    insert_time_with_index = time.time() - start_time

    print(f"无索引插入耗时: {insert_time_no_index * 1000:.4f} 毫秒")
    print(f"有索引插入耗时: {insert_time_with_index * 1000:.4f} 毫秒")
    if insert_time_no_index > 0:
        write_overhead = insert_time_with_index / insert_time_no_index
        print(f"写入开销增加: {write_overhead:.1f} 倍")

    # 测试覆盖索引
    print("\n=== 覆盖索引测试 ===")
    cursor.execute('CREATE INDEX idx_cat_price ON products(category, price)')

    # 非覆盖索引查询（需要回表）
    start_time = time.time()
    cursor.execute("SELECT * FROM products WHERE category = 'electronics' AND price > 500")
    cursor.fetchall()
    non_covering_time = time.time() - start_time

    # 覆盖索引查询（无需回表）
    start_time = time.time()
    cursor.execute("SELECT category, price FROM products WHERE category = 'electronics' AND price > 500")
    cursor.fetchall()
    covering_time = time.time() - start_time

    print(f"非覆盖索引查询耗时: {non_covering_time * 1000:.2f} 毫秒")
    print(f"覆盖索引查询耗时: {covering_time * 1000:.2f} 毫秒")
    if covering_time > 0:
        covering_speedup = non_covering_time / covering_time
        print(f"覆盖索引性能提升: {covering_speedup:.1f} 倍")

    conn.close()

def main():
    print("=== 索引性能全面对比实验 ===\n")
    performance_test()
    print("\n🎯 实验结论:")
    print("   - 索引大幅提升查询性能")
    print("   - 索引略微增加写入开销")
    print("   - 覆盖索引可以进一步优化查询性能")

if __name__ == "__main__":
    main()