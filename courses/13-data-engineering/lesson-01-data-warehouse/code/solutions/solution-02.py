#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：缓慢变化维Type 2实现

实现SCD Type 2（缓慢变化维类型2），用于追踪维度表中数据的历史变化。
本示例以产品维度表为例，追踪产品价格的变化历史。
"""

import sqlite3
from datetime import datetime, date

def create_scd_type2_schema(conn):
    """创建支持SCD Type 2的表结构"""
    cursor = conn.cursor()

    # 产品维度表（支持SCD Type 2）
    cursor.execute('''
        CREATE TABLE dim_product_scd2 (
            product_sk INTEGER PRIMARY KEY,          -- 代理键（Surrogate Key）
            product_id INTEGER NOT NULL,             -- 业务键（Natural Key）
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            brand TEXT NOT NULL,
            price REAL NOT NULL,
            effective_date DATE NOT NULL,           -- 生效日期
            expiry_date DATE NOT NULL,              -- 失效日期
            is_current BOOLEAN NOT NULL DEFAULT 1,   -- 是否当前版本
            version INTEGER NOT NULL                -- 版本号
        )
    ''')

    conn.commit()

def insert_product_version(conn, product_id, product_name, category, brand, price, effective_date):
    """插入产品的新版本"""
    cursor = conn.cursor()

    # 首先将当前版本标记为非当前版本，并设置失效日期
    cursor.execute('''
        UPDATE dim_product_scd2
        SET is_current = 0, expiry_date = ?
        WHERE product_id = ? AND is_current = 1
    ''', (effective_date, product_id))

    # 获取新版本号
    cursor.execute('''
        SELECT COALESCE(MAX(version), 0) + 1
        FROM dim_product_scd2
        WHERE product_id = ?
    ''', (product_id,))
    version = cursor.fetchone()[0]

    # 插入新版本
    cursor.execute('''
        INSERT INTO dim_product_scd2 (
            product_id, product_name, category, brand, price,
            effective_date, expiry_date, is_current, version
        ) VALUES (?, ?, ?, ?, ?, ?, '9999-12-31', 1, ?)
    ''', (product_id, product_name, category, brand, price, effective_date, version))

    conn.commit()

def initialize_products(conn):
    """初始化产品数据（初始版本）"""
    products = [
        (1, 'iPhone 14', 'Smartphones', 'Apple', 799.00),
        (2, 'MacBook Pro', 'Laptops', 'Apple', 1999.00),
        (3, 'Samsung Galaxy S23', 'Smartphones', 'Samsung', 699.00),
    ]

    for product in products:
        insert_product_version(conn, *product, date(2023, 1, 1))

def simulate_price_changes(conn):
    """模拟产品价格变化"""
    print("=== 模拟产品价格变化 ===")

    # iPhone 14 在2023年6月1日降价
    insert_product_version(conn, 1, 'iPhone 14', 'Smartphones', 'Apple', 699.00, date(2023, 6, 1))
    print("✓ iPhone 14 价格从 $799 降至 $699 (2023-06-01)")

    # MacBook Pro 在2023年9月1日涨价
    insert_product_version(conn, 2, 'MacBook Pro', 'Laptops', 'Apple', 2199.00, date(2023, 9, 1))
    print("✓ MacBook Pro 价格从 $1999 升至 $2199 (2023-09-01)")

    # Samsung Galaxy S23 在2023年12月1日降价
    insert_product_version(conn, 3, 'Samsung Galaxy S23', 'Smartphones', 'Samsung', 599.00, date(2023, 12, 1))
    print("✓ Samsung Galaxy S23 价格从 $699 降至 $599 (2023-12-01)")

    print()

def query_current_products(conn):
    """查询当前有效的产品信息"""
    print("=== 当前有效的产品信息 ===")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT product_name, brand, price, effective_date
        FROM dim_product_scd2
        WHERE is_current = 1
        ORDER BY product_name
    ''')

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]} ({row[1]}): ${row[2]:.2f} (生效日期: {row[3]})")
    print()

def query_historical_products(conn, as_of_date):
    """查询指定日期的产品信息（历史查询）"""
    print(f"=== {as_of_date} 的产品信息 ===")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT product_name, brand, price
        FROM dim_product_scd2
        WHERE ? BETWEEN effective_date AND expiry_date
        ORDER BY product_name
    ''', (as_of_date,))

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]} ({row[1]}): ${row[2]:.2f}")
    print()

def demonstrate_time_travel_analysis(conn):
    """演示时间旅行分析"""
    print("=== 时间旅行分析示例 ===")

    # 查询不同时间点的产品价格
    query_historical_products(conn, date(2023, 3, 1))   # 2023年3月
    query_historical_products(conn, date(2023, 7, 1))   # 2023年7月
    query_historical_products(conn, date(2023, 10, 1))  # 2023年10月

def main():
    """主函数"""
    print("SCD Type 2 实现演示")
    print("=" * 25)

    # 创建内存数据库
    conn = sqlite3.connect(':memory:')

    # 创建SCD Type 2表结构
    create_scd_type2_schema(conn)
    print("✓ SCD Type 2 表结构创建完成")

    # 初始化产品数据
    initialize_products(conn)
    print("✓ 初始产品数据加载完成")

    # 查询初始状态
    query_current_products(conn)

    # 模拟价格变化
    simulate_price_changes(conn)

    # 查询当前状态
    query_current_products(conn)

    # 演示时间旅行分析
    demonstrate_time_travel_analysis(conn)

    # 关闭连接
    conn.close()

    print("SCD Type 2 关键特点总结:")
    print("- 使用代理键(product_sk)而非业务键作为主键")
    print("- 通过effective_date和expiry_date管理版本有效期")
    print("- is_current标志标识当前有效版本")
    print("- 支持完整的历史追溯和时间点查询")
    print("- 适用于需要保留完整历史记录的重要维度")

if __name__ == "__main__":
    main()