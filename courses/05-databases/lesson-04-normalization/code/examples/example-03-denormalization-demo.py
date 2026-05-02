#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反规范化演示：性能权衡分析
比较规范化和反规范化设计的查询性能差异
"""

import sqlite3
import time
import random
from contextlib import contextmanager

@contextmanager
def timer():
    """计时器上下文管理器"""
    start = time.time()
    yield
    end = time.time()
    print(f"⏱️  执行时间: {(end - start) * 1000:.2f} 毫秒")

def create_normalized_schema(conn):
    """创建规范化的数据库模式"""
    cursor = conn.cursor()

    # 创建规范化的表结构
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')

    conn.commit()

def create_denormalized_schema(conn):
    """创建反规范化的数据库模式"""
    cursor = conn.cursor()

    # 创建反规范化的宽表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders_denormalized (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_city TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            product_category TEXT NOT NULL,
            product_price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL
        )
    ''')

    conn.commit()

def generate_sample_data(conn, num_orders=1000):
    """生成示例数据"""
    cursor = conn.cursor()

    # 客户数据
    customers = [
        (1, '张三', 'zhang@example.com', '北京'),
        (2, '李四', 'li@example.com', '上海'),
        (3, '王五', 'wang@example.com', '广州'),
        (4, '赵六', 'zhao@example.com', '深圳'),
        (5, '钱七', 'qian@example.com', '杭州')
    ]

    # 产品数据
    products = [
        (1, 'iPhone', '手机', 8999.0),
        (2, 'MacBook', '电脑', 12999.0),
        (3, 'iPad', '平板', 3999.0),
        (4, 'AirPods', '耳机', 1299.0),
        (5, 'Apple Watch', '手表', 2999.0)
    ]

    # 插入客户和产品数据
    cursor.executemany("INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?)", customers)
    cursor.executemany("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)", products)

    # 生成订单数据
    orders_data = []
    order_items_data = []
    denormalized_data = []

    for i in range(1, num_orders + 1):
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        order_date = f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

        # 规范化数据
        orders_data.append((i, customer[0], order_date))
        order_items_data.append((i, product[0], quantity))

        # 反规范化数据
        denormalized_data.append((
            i, customer[0], customer[1], customer[2], customer[3],
            product[0], product[1], product[2], product[3], quantity, order_date
        ))

    cursor.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?)", orders_data)
    cursor.executemany("INSERT OR IGNORE INTO order_items VALUES (?, ?, ?)", order_items_data)
    cursor.executemany("INSERT OR IGNORE INTO orders_denormalized VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", denormalized_data)

    conn.commit()

def run_normalized_query(conn):
    """执行规范化查询：获取订单详情"""
    cursor = conn.cursor()
    query = '''
        SELECT
            o.order_id,
            c.name as customer_name,
            c.city as customer_city,
            p.name as product_name,
            p.category as product_category,
            oi.quantity,
            p.price * oi.quantity as total_amount,
            o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE c.city = '北京'
        ORDER BY o.order_date DESC
        LIMIT 100
    '''
    cursor.execute(query)
    return cursor.fetchall()

def run_denormalized_query(conn):
    """执行反规范化查询：获取订单详情"""
    cursor = conn.cursor()
    query = '''
        SELECT
            order_id,
            customer_name,
            customer_city,
            product_name,
            product_category,
            quantity,
            product_price * quantity as total_amount,
            order_date
        FROM orders_denormalized
        WHERE customer_city = '北京'
        ORDER BY order_date DESC
        LIMIT 100
    '''
    cursor.execute(query)
    return cursor.fetchall()

def demonstrate_performance_comparison():
    """演示性能对比"""
    print("🔍 反规范化性能对比演示")
    print("=" * 60)

    # 创建两个数据库连接
    normalized_conn = sqlite3.connect(':memory:')
    denormalized_conn = sqlite3.connect(':memory:')

    try:
        # 设置规范化数据库
        print("\n🔧 设置规范化数据库...")
        create_normalized_schema(normalized_conn)
        generate_sample_data(normalized_conn, 5000)

        # 设置反规范化数据库
        print("🔧 设置反规范化数据库...")
        create_denormalized_schema(denormalized_conn)
        generate_sample_data(denormalized_conn, 5000)

        # 性能测试
        print("\n⚡ 性能测试：查询北京客户的订单详情（前100条）")
        print("-" * 50)

        print("📊 规范化查询 (多表JOIN):")
        with timer():
            normalized_results = run_normalized_query(normalized_conn)
        print(f"   返回 {len(normalized_results)} 条记录")

        print("\n📊 反规范化查询 (单表):")
        with timer():
            denormalized_results = run_denormalized_query(denormalized_conn)
        print(f"   返回 {len(denormalized_results)} 条记录")

        # 数据一致性检查
        print("\n✅ 数据一致性验证:")
        if len(normalized_results) == len(denormalized_results):
            print("   ✅ 查询结果数量一致")
        else:
            print("   ⚠️  查询结果数量不一致")

        # 显示存储空间对比（估算）
        normalized_cursor = normalized_conn.cursor()
        denormalized_cursor = denormalized_conn.cursor()

        normalized_cursor.execute("SELECT COUNT(*) FROM orders")
        normalized_orders = normalized_cursor.fetchone()[0]
        normalized_cursor.execute("SELECT COUNT(*) FROM order_items")
        normalized_items = normalized_cursor.fetchone()[0]

        denormalized_cursor.execute("SELECT COUNT(*) FROM orders_denormalized")
        denormalized_total = denormalized_cursor.fetchone()[0]

        print(f"\n💾 存储空间对比 (估算):")
        print(f"   规范化: 订单表({normalized_orders}) + 订单项表({normalized_items}) = {normalized_orders + normalized_items} 行")
        print(f"   反规范化: 单表 {denormalized_total} 行")
        print(f"   冗余率: {(denormalized_total - normalized_items) / normalized_items * 100:.1f}%")

        print("\n💡 分析结论:")
        print("✅ 反规范化优势：")
        print("   - 查询性能更好（避免JOIN操作）")
        print("   - 查询逻辑更简单")
        print("❌ 反规范化劣势：")
        print("   - 数据冗余增加存储空间")
        print("   - 更新异常风险（需要同步更新多处）")
        print("   - 插入/删除操作更复杂")

        print("\n🎯 最佳实践建议:")
        print("   - OLTP系统：优先规范化，保证数据一致性")
        print("   - OLAP系统：可适度反规范化，优化查询性能")
        print("   - 混合场景：核心事务用规范化，报表用物化视图")

    finally:
        normalized_conn.close()
        denormalized_conn.close()

if __name__ == "__main__":
    demonstrate_performance_comparison()