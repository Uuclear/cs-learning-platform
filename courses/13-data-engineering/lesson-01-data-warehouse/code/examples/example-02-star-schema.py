#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：星型模型创建与查询

本示例演示如何创建星型模型（Star Schema）并执行OLAP查询。
包含一个事实表（销售事实）和三个维度表（时间、产品、客户）。
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_star_schema(conn):
    """创建星型模型"""
    cursor = conn.cursor()

    # 创建时间维度表
    cursor.execute('''
        CREATE TABLE dim_date (
            date_id INTEGER PRIMARY KEY,
            full_date DATE,
            year INTEGER,
            quarter INTEGER,
            month INTEGER,
            day INTEGER,
            day_of_week INTEGER,
            is_weekend BOOLEAN
        )
    ''')

    # 创建产品维度表
    cursor.execute('''
        CREATE TABLE dim_product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            brand TEXT,
            price REAL
        )
    ''')

    # 创建客户维度表
    cursor.execute('''
        CREATE TABLE dim_customer (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            city TEXT,
            region TEXT,
            customer_segment TEXT
        )
    ''')

    # 创建销售事实表
    cursor.execute('''
        CREATE TABLE fact_sales (
            sale_id INTEGER PRIMARY KEY,
            date_id INTEGER,
            product_id INTEGER,
            customer_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            total_amount REAL,
            FOREIGN KEY (date_id) REFERENCES dim_date (date_id),
            FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
            FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id)
        )
    ''')

    conn.commit()

def populate_dimensions(conn):
    """填充维度表数据"""
    cursor = conn.cursor()

    # 填充时间维度（过去一年的数据）
    start_date = datetime(2023, 1, 1)
    for i in range(365):
        current_date = start_date + timedelta(days=i)
        date_id = int(current_date.strftime('%Y%m%d'))
        cursor.execute('''
            INSERT INTO dim_date VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            date_id,
            current_date.date(),
            current_date.year,
            (current_date.month - 1) // 3 + 1,
            current_date.month,
            current_date.day,
            current_date.weekday(),
            current_date.weekday() >= 5
        ))

    # 填充产品维度
    products = [
        ('iPhone 14', '手机', 'Apple', 7999.00),
        ('MacBook Pro', '电脑', 'Apple', 12999.00),
        ('Samsung Galaxy S23', '手机', 'Samsung', 6999.00),
        ('Dell XPS 13', '电脑', 'Dell', 8999.00),
        ('iPad Air', '平板', 'Apple', 4999.00),
        ('Surface Pro', '平板', 'Microsoft', 7499.00),
    ]

    for i, (name, category, brand, price) in enumerate(products, 1):
        cursor.execute('''
            INSERT INTO dim_product VALUES (?, ?, ?, ?, ?)
        ''', (i, name, category, brand, price))

    # 填充客户维度
    customers = [
        ('张三', '北京', '华北', '企业客户'),
        ('李四', '上海', '华东', '个人客户'),
        ('王五', '广州', '华南', '企业客户'),
        ('赵六', '深圳', '华南', '个人客户'),
        ('钱七', '杭州', '华东', '企业客户'),
    ]

    for i, (name, city, region, segment) in enumerate(customers, 1):
        cursor.execute('''
            INSERT INTO dim_customer VALUES (?, ?, ?, ?, ?)
        ''', (i, name, city, region, segment))

    conn.commit()

def populate_facts(conn):
    """填充事实表数据"""
    cursor = conn.cursor()

    # 获取维度数据
    cursor.execute("SELECT date_id FROM dim_date")
    date_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT product_id, price FROM dim_product")
    products = cursor.fetchall()

    cursor.execute("SELECT customer_id FROM dim_customer")
    customer_ids = [row[0] for row in cursor.fetchall()]

    # 生成销售事实数据
    for _ in range(1000):
        date_id = random.choice(date_ids)
        product_id, base_price = random.choice(products)
        customer_id = random.choice(customer_ids)
        quantity = random.randint(1, 5)

        # 价格可能有折扣
        unit_price = round(base_price * random.uniform(0.8, 1.0), 2)
        total_amount = round(quantity * unit_price, 2)

        cursor.execute('''
            INSERT INTO fact_sales (date_id, product_id, customer_id, quantity, unit_price, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date_id, product_id, customer_id, quantity, unit_price, total_amount))

    conn.commit()

def run_olap_queries(conn):
    """执行OLAP查询"""
    cursor = conn.cursor()

    print("=== 星型模型 OLAP 查询示例 ===\n")

    # 查询1：按产品类别统计销售额
    print("1. 按产品类别统计销售额:")
    cursor.execute('''
        SELECT
            p.category,
            SUM(f.total_amount) as total_sales,
            COUNT(f.sale_id) as order_count
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_sales DESC
    ''')

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]}: 销售额 ¥{row[1]:,.2f}, 订单数 {row[2]}")
    print()

    # 查询2：按地区和月份分析销售趋势
    print("2. 按地区和月份分析销售趋势:")
    cursor.execute('''
        SELECT
            c.region,
            d.month,
            SUM(f.total_amount) as monthly_sales
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE d.year = 2023 AND d.month IN (1, 2, 3)
        GROUP BY c.region, d.month
        ORDER BY c.region, d.month
    ''')

    results = cursor.fetchall()
    current_region = None
    for row in results:
        if row[0] != current_region:
            current_region = row[0]
            print(f"   {current_region}:")
        print(f"      2023年{row[1]}月: ¥{row[2]:,.2f}")
    print()

    # 查询3：客户细分分析
    print("3. 客户细分分析:")
    cursor.execute('''
        SELECT
            c.customer_segment,
            AVG(f.total_amount) as avg_order_value,
            SUM(f.total_amount) as total_revenue
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        GROUP BY c.customer_segment
    ''')

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]}: 平均订单价值 ¥{row[1]:.2f}, 总收入 ¥{row[2]:,.2f}")
    print()

def main():
    """主函数"""
    print("星型模型创建与OLAP查询演示")
    print("=" * 40)

    # 创建内存数据库
    conn = sqlite3.connect(':memory:')

    # 创建星型模型
    create_star_schema(conn)
    print("✓ 星型模型创建完成")

    # 填充维度数据
    populate_dimensions(conn)
    print("✓ 维度表数据填充完成")

    # 填充事实数据
    populate_facts(conn)
    print("✓ 事实表数据填充完成")

    # 执行OLAP查询
    run_olap_queries(conn)

    # 关闭连接
    conn.close()

    print("\n星型模型优势总结:")
    print("- 查询简单直观，易于理解")
    print("- 性能优化：维度表小，事实表大但查询高效")
    print("- 支持复杂的多维分析")

if __name__ == "__main__":
    main()