#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: SQL聚合函数和分组查询
演示COUNT、SUM、AVG、MAX、MIN等聚合函数的使用，以及GROUP BY分组
"""

import sqlite3

def main():
    # 创建内存数据库
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建订单表
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            product_category TEXT NOT NULL,
            amount REAL NOT NULL,
            order_date TEXT NOT NULL
        )
    ''')

    # 插入订单数据
    orders_data = [
        (1, "张三", "电子产品", 2500.0, "2026-01-15"),
        (2, "李四", "电子产品", 3200.0, "2026-01-20"),
        (3, "王五", "服装", 800.0, "2026-01-22"),
        (4, "赵六", "电子产品", 1800.0, "2026-02-01"),
        (5, "钱七", "图书", 120.0, "2026-02-05"),
        (6, "孙八", "服装", 1200.0, "2026-02-10"),
        (7, "周九", "电子产品", 4500.0, "2026-02-15"),
        (8, "吴十", "图书", 95.0, "2026-02-18"),
        (9, "郑一", "服装", 650.0, "2026-03-01"),
        (10, "王二", "电子产品", 2800.0, "2026-03-05")
    ]
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders_data)
    conn.commit()

    print("✅ 订单表创建成功！")

    # 基本聚合函数
    print("\n📊 基本聚合统计:")

    # COUNT - 计算总订单数
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    print(f"  📦 总订单数: {total_orders}")

    # SUM - 计算总销售额
    cursor.execute("SELECT SUM(amount) FROM orders")
    total_sales = cursor.fetchone()[0]
    print(f"  💰 总销售额: ¥{total_sales:,.2f}")

    # AVG - 计算平均订单金额
    cursor.execute("SELECT AVG(amount) FROM orders")
    avg_order_amount = cursor.fetchone()[0]
    print(f"  📊 平均订单金额: ¥{avg_order_amount:.2f}")

    # MAX/MIN - 最高和最低订单金额
    cursor.execute("SELECT MAX(amount), MIN(amount) FROM orders")
    max_amount, min_amount = cursor.fetchone()
    print(f"  📈 最高订单金额: ¥{max_amount:.2f}")
    print(f"  📉 最低订单金额: ¥{min_amount:.2f}")

    # GROUP BY 分组聚合
    print("\n📊 按产品类别分组统计:")
    cursor.execute('''
        SELECT product_category,
               COUNT(*) as order_count,
               SUM(amount) as total_sales,
               AVG(amount) as avg_amount,
               MAX(amount) as max_amount
        FROM orders
        GROUP BY product_category
        ORDER BY total_sales DESC
    ''')
    category_stats = cursor.fetchall()
    for category, count, sales, avg_amt, max_amt in category_stats:
        print(f"  🏷️  {category}:")
        print(f"    订单数: {count}, 总销售额: ¥{sales:,.2f}")
        print(f"    平均金额: ¥{avg_amt:.2f}, 最高金额: ¥{max_amt:.2f}")

    # HAVING 子句 - 对分组结果进行筛选
    print("\n📊 筛选销售额超过2000的产品类别:")
    cursor.execute('''
        SELECT product_category,
               SUM(amount) as total_sales
        FROM orders
        GROUP BY product_category
        HAVING SUM(amount) > 2000
        ORDER BY total_sales DESC
    ''')
    high_value_categories = cursor.fetchall()
    for category, sales in high_value_categories:
        print(f"  🏆 {category}: ¥{sales:,.2f}")

    # 多列分组
    print("\n📊 按月份和产品类别分组统计:")
    cursor.execute('''
        SELECT
            strftime('%Y-%m', order_date) as month,
            product_category,
            COUNT(*) as order_count,
            SUM(amount) as total_sales
        FROM orders
        GROUP BY month, product_category
        ORDER BY month, total_sales DESC
    ''')
    monthly_category_stats = cursor.fetchall()
    current_month = ""
    for month, category, count, sales in monthly_category_stats:
        if month != current_month:
            current_month = month
            print(f"\n  📅 {month}:")
        print(f"    {category} - 订单数: {count}, 销售额: ¥{sales:,.2f}")

    # 关闭连接
    conn.close()
    print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()