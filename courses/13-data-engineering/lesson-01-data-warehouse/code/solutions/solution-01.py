#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：电商数据仓库星型模型设计

设计一个完整的电商数据分析星型模型，包含事实表和维度表。
"""

import sqlite3

def create_ecommerce_star_schema(conn):
    """创建电商星型模型"""
    cursor = conn.cursor()

    # 时间维度表
    cursor.execute('''
        CREATE TABLE dim_date (
            date_id INTEGER PRIMARY KEY,
            date_value DATE NOT NULL,
            year INTEGER NOT NULL,
            quarter INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            day_name TEXT NOT NULL,
            month_name TEXT NOT NULL,
            is_weekend BOOLEAN NOT NULL,
            is_holiday BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # 产品维度表
    cursor.execute('''
        CREATE TABLE dim_product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            brand TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1
        )
    ''')

    # 客户维度表
    cursor.execute('''
        CREATE TABLE dim_customer (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            country TEXT NOT NULL,
            customer_segment TEXT NOT NULL,
            registration_date DATE NOT NULL
        )
    ''')

    # 店铺维度表
    cursor.execute('''
        CREATE TABLE dim_store (
            store_id INTEGER PRIMARY KEY,
            store_name TEXT NOT NULL,
            store_type TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            country TEXT NOT NULL,
            is_online BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # 销售事实表
    cursor.execute('''
        CREATE TABLE fact_sales (
            sale_id INTEGER PRIMARY KEY,
            date_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            discount_amount REAL NOT NULL DEFAULT 0,
            total_amount REAL NOT NULL,
            profit REAL NOT NULL,
            FOREIGN KEY (date_id) REFERENCES dim_date (date_id),
            FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
            FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id),
            FOREIGN KEY (store_id) REFERENCES dim_store (store_id)
        )
    ''')

    # 创建索引以优化查询性能
    cursor.execute('CREATE INDEX idx_fact_sales_date ON fact_sales(date_id)')
    cursor.execute('CREATE INDEX idx_fact_sales_product ON fact_sales(product_id)')
    cursor.execute('CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id)')
    cursor.execute('CREATE INDEX idx_fact_sales_store ON fact_sales(store_id)')

    conn.commit()

def populate_sample_data(conn):
    """填充示例数据"""
    cursor = conn.cursor()

    # 填充时间维度（2023年）
    import datetime
    start_date = datetime.date(2023, 1, 1)
    for i in range(365):
        current_date = start_date + datetime.timedelta(days=i)
        date_id = int(current_date.strftime('%Y%m%d'))
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][current_date.weekday()]
        month_name = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ][current_date.month - 1]
        is_weekend = current_date.weekday() >= 5

        cursor.execute('''
            INSERT INTO dim_date VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            date_id, current_date, current_date.year, (current_date.month - 1) // 3 + 1,
            current_date.month, current_date.day, day_name, month_name, is_weekend, False
        ))

    # 填充产品维度
    products = [
        (1, 'iPhone 14 Pro', 'Electronics', 'Smartphones', 'Apple', 999.00, 700.00, True),
        (2, 'Samsung Galaxy S23', 'Electronics', 'Smartphones', 'Samsung', 899.00, 650.00, True),
        (3, 'MacBook Air M2', 'Electronics', 'Laptops', 'Apple', 1199.00, 850.00, True),
        (4, 'Nike Air Max', 'Clothing', 'Shoes', 'Nike', 159.00, 80.00, True),
        (5, 'Adidas Ultraboost', 'Clothing', 'Shoes', 'Adidas', 179.00, 90.00, True),
        (6, 'Levi\'s 501 Jeans', 'Clothing', 'Pants', 'Levi\'s', 98.00, 45.00, True),
    ]

    cursor.executemany('''
        INSERT INTO dim_product VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)

    # 填充客户维度
    customers = [
        (1, '张三', 'zhangsan@email.com', 'Beijing', 'Beijing', 'China', 'Premium', '2022-01-15'),
        (2, '李四', 'lisi@email.com', 'Shanghai', 'Shanghai', 'China', 'Regular', '2022-03-20'),
        (3, '王五', 'wangwu@email.com', 'Guangzhou', 'Guangdong', 'China', 'Premium', '2022-02-10'),
        (4, '赵六', 'zhaoliu@email.com', 'Shenzhen', 'Guangdong', 'China', 'Regular', '2022-05-05'),
    ]

    cursor.executemany('''
        INSERT INTO dim_customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', customers)

    # 填充店铺维度
    stores = [
        (1, 'Online Store', 'Online', 'N/A', 'N/A', 'Global', True),
        (2, 'Beijing Flagship', 'Physical', 'Beijing', 'Beijing', 'China', False),
        (3, 'Shanghai Mall', 'Physical', 'Shanghai', 'Shanghai', 'China', False),
    ]

    cursor.executemany('''
        INSERT INTO dim_store VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', stores)

    conn.commit()

def demonstrate_olap_queries(conn):
    """演示OLAP查询"""
    cursor = conn.cursor()

    print("=== 电商星型模型 OLAP 查询示例 ===\n")

    # 1. 按产品类别和月份分析销售额
    print("1. 按产品类别和月份分析销售额:")
    cursor.execute('''
        SELECT
            p.category,
            d.month,
            SUM(f.total_amount) as sales_amount,
            SUM(f.quantity) as units_sold
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE d.year = 2023 AND d.month <= 3
        GROUP BY p.category, d.month
        ORDER BY p.category, d.month
    ''')

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]} - 2023年{row[1]}月: 销售额 ${row[2]:,.2f}, 销量 {row[3]}件")
    print()

    # 2. 客户细分分析
    print("2. 客户细分分析:")
    cursor.execute('''
        SELECT
            c.customer_segment,
            COUNT(DISTINCT f.customer_id) as unique_customers,
            SUM(f.total_amount) as total_revenue,
            AVG(f.total_amount) as avg_order_value
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        GROUP BY c.customer_segment
    ''')

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]}: {row[1]}位客户, 总收入 ${row[2]:,.2f}, 平均订单价值 ${row[3]:.2f}")
    print()

    # 3. 利润分析
    print("3. 按品牌利润分析:")
    cursor.execute('''
        SELECT
            p.brand,
            SUM(f.profit) as total_profit,
            SUM(f.total_amount) as total_revenue,
            ROUND(SUM(f.profit) * 100.0 / SUM(f.total_amount), 2) as profit_margin
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY p.brand
        ORDER BY total_profit DESC
    ''')

    results = cursor.fetchall()
    for row in results:
        print(f"   {row[0]}: 利润 ${row[1]:,.2f}, 收入 ${row[2]:,.2f}, 利润率 {row[3]}%")
    print()

def main():
    """主函数"""
    print("电商数据仓库星型模型设计")
    print("=" * 35)

    # 创建内存数据库
    conn = sqlite3.connect(':memory:')

    # 创建星型模型
    create_ecommerce_star_schema(conn)
    print("✓ 电商星型模型创建完成")

    # 填充实例数据
    populate_sample_data(conn)
    print("✓ 示例数据填充完成")

    # 演示OLAP查询
    demonstrate_olap_queries(conn)

    # 关闭连接
    conn.close()

    print("星型模型设计要点总结:")
    print("- 维度表包含描述性属性，支持钻取分析")
    print("- 事实表包含度量值和外键，支持聚合计算")
    print("- 索引优化查询性能")
    print("- 支持多维分析：时间、产品、客户、店铺等维度")

if __name__ == "__main__":
    main()