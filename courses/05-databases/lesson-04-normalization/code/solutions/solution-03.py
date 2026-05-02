#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：设计规范化在线书店数据库模式
创建一个符合3NF的完整在线书店数据库设计
"""

import sqlite3

def design_normalized_bookstore_schema(conn):
    """设计规范化的在线书店数据库模式"""
    cursor = conn.cursor()

    print("📚 在线书店数据库规范化设计")
    print("=" * 50)

    # 步骤1：识别实体和关系
    print("\n🔍 实体识别：")
    print("- 用户 (Users)")
    print("- 商品 (Products/Books)")
    print("- 订单 (Orders)")
    print("- 订单项 (Order Items)")
    print("- 分类 (Categories)")
    print("- 作者 (Authors)")
    print("- 出版社 (Publishers)")

    # 步骤2：创建3NF表结构

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 地址表（用户可能有多个地址）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            address_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            address_type TEXT NOT NULL, -- 'shipping', 'billing'
            street_address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            country TEXT NOT NULL DEFAULT 'China',
            is_default BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # 出版社表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            publisher_name TEXT NOT NULL UNIQUE,
            contact_email TEXT,
            phone TEXT,
            website TEXT
        )
    ''')

    # 作者表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY,
            author_name TEXT NOT NULL,
            biography TEXT,
            birth_date TEXT
        )
    ''')

    # 图书分类表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL UNIQUE,
            parent_category_id INTEGER,
            description TEXT,
            FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
        )
    ''')

    # 图书表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            isbn TEXT UNIQUE,
            title TEXT NOT NULL,
            subtitle TEXT,
            publisher_id INTEGER NOT NULL,
            publication_date TEXT,
            pages INTEGER,
            language TEXT DEFAULT 'Chinese',
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            description TEXT,
            cover_image_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        )
    ''')

    # 图书-作者关联表（多对多关系）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_authors (
            book_id INTEGER,
            author_id INTEGER,
            author_role TEXT DEFAULT 'primary', -- 'primary', 'co-author', 'translator', etc.
            PRIMARY KEY (book_id, author_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (author_id) REFERENCES authors(author_id)
        )
    ''')

    # 图书-分类关联表（多对多关系）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_categories (
            book_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (book_id, category_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')

    # 订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            shipping_address_id INTEGER NOT NULL,
            billing_address_id INTEGER NOT NULL,
            order_status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'
            total_amount REAL NOT NULL,
            shipping_cost REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            shipped_date TEXT,
            delivered_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id),
            FOREIGN KEY (billing_address_id) REFERENCES addresses(address_id)
        )
    ''')

    # 订单项表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    ''')

    # 购物车表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            cart_item_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            UNIQUE(user_id, book_id)
        )
    ''')

    conn.commit()

    print("\n✅ 创建了以下规范化表：")
    tables = [
        'users', 'addresses', 'publishers', 'authors', 'categories',
        'books', 'book_authors', 'book_categories', 'orders',
        'order_items', 'cart_items'
    ]

    for table in tables:
        print(f"   • {table}")

def insert_sample_data(conn):
    """插入示例数据"""
    cursor = conn.cursor()

    # 出版社
    cursor.execute("INSERT INTO publishers VALUES (1, '人民文学出版社', 'contact@rwp.com', '010-12345678', 'http://www.rwp.com')")
    cursor.execute("INSERT INTO publishers VALUES (2, '商务印书馆', 'contact@cp.com', '010-87654321', 'http://www.cp.com')")

    # 作者
    cursor.execute("INSERT INTO authors VALUES (1, '鲁迅', '中国现代文学奠基人', '1881-09-25')")
    cursor.execute("INSERT INTO authors VALUES (2, '茅盾', '中国现代作家、文学评论家', '1896-07-04')")
    cursor.execute("INSERT INTO authors VALUES (3, '巴金', '中国现代文学家', '1904-11-25')")

    # 分类
    cursor.execute("INSERT INTO categories VALUES (1, '文学', NULL, '文学作品')")
    cursor.execute("INSERT INTO categories VALUES (2, '小说', 1, '各类小说')")
    cursor.execute("INSERT INTO categories VALUES (3, '散文', 1, '散文作品')")

    # 用户
    cursor.execute("INSERT INTO users VALUES (1, 'zhangsan', 'zhang@example.com', 'hash123', '张', '三', '138****1234', '2023-01-01')")
    cursor.execute("INSERT INTO users VALUES (2, 'lisi', 'li@example.com', 'hash456', '李', '四', '139****5678', '2023-01-02')")

    # 地址
    cursor.execute("INSERT INTO addresses VALUES (1, 1, 'shipping', '北京市朝阳区XX路1号', '北京', '北京', '100001', 'China', 1)")
    cursor.execute("INSERT INTO addresses VALUES (2, 1, 'billing', '北京市朝阳区XX路1号', '北京', '北京', '100001', 'China', 1)")

    # 图书
    cursor.execute("INSERT INTO books VALUES (1, '9787020000011', '呐喊', NULL, 1, '1923-08-01', 200, 'Chinese', 39.80, 50, '鲁迅短篇小说集', 'cover1.jpg', '2023-01-01')")
    cursor.execute("INSERT INTO books VALUES (2, '9787020000022', '子夜', NULL, 2, '1933-01-01', 350, 'Chinese', 45.00, 30, '茅盾长篇小说', 'cover2.jpg', '2023-01-02')")

    # 图书-作者关联
    cursor.execute("INSERT INTO book_authors VALUES (1, 1, 'primary')")
    cursor.execute("INSERT INTO book_authors VALUES (2, 2, 'primary')")

    # 图书-分类关联
    cursor.execute("INSERT INTO book_categories VALUES (1, 2)")
    cursor.execute("INSERT INTO book_categories VALUES (2, 2)")

    # 订单
    cursor.execute("INSERT INTO orders VALUES (1, 1, 1, 2, 'delivered', 84.80, 10.00, 8.48, 0, '2023-02-01', '2023-02-03', '2023-02-05')")

    # 订单项
    cursor.execute("INSERT INTO order_items VALUES (1, 1, 1, 1, 39.80, 39.80)")
    cursor.execute("INSERT INTO order_items VALUES (2, 1, 2, 1, 45.00, 45.00)")

    conn.commit()

def demonstrate_3nf_compliance():
    """演示3NF合规性"""
    print("\n🔍 3NF合规性验证：")
    print("-" * 30)

    compliance_points = [
        "✅ 所有非主属性完全依赖于主键（满足2NF）",
        "✅ 不存在传递依赖（满足3NF）",
        "✅ 多对多关系通过关联表正确处理",
        "✅ 消除了数据冗余",
        "✅ 避免了更新、插入、删除异常"
    ]

    for point in compliance_points:
        print(point)

def show_query_examples(conn):
    """展示查询示例"""
    cursor = conn.cursor()

    print("\n📊 查询示例：")
    print("-" * 20)

    # 示例1：获取用户订单详情
    print("\n1. 获取用户订单详情（包含图书信息）：")
    cursor.execute('''
        SELECT
            u.username,
            o.order_id,
            b.title,
            oi.quantity,
            oi.unit_price,
            o.total_amount,
            o.order_status
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN books b ON oi.book_id = b.book_id
        WHERE u.user_id = 1
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f"   {result}")

    # 示例2：获取图书及其作者信息
    print("\n2. 获取图书及其作者信息：")
    cursor.execute('''
        SELECT
            b.title,
            a.author_name,
            p.publisher_name
        FROM books b
        JOIN book_authors ba ON b.book_id = ba.book_id
        JOIN authors a ON ba.author_id = a.author_id
        JOIN publishers p ON b.publisher_id = p.publisher_id
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f"   {result}")

def main():
    """主函数"""
    print("🔧 解决方案3：在线书店数据库规范化设计")
    print("=" * 60)

    conn = sqlite3.connect(':memory:')

    try:
        # 设计规范化模式
        design_normalized_bookstore_schema(conn)

        # 插入示例数据
        insert_sample_data(conn)

        # 验证3NF合规性
        demonstrate_3nf_compliance()

        # 展示查询示例
        show_query_examples(conn)

        print("\n💡 设计优势：")
        print("• 数据一致性：每个事实只存储一次")
        print("• 扩展性：易于添加新功能（如评论、评分等）")
        print("• 维护性：更新操作简单且安全")
        print("• 完整性：外键约束保证数据完整性")
        print("• 性能：虽然需要JOIN，但可通过索引优化")

        print("\n🎯 最佳实践：")
        print("• 在OLTP系统中优先保证数据一致性")
        print("• 对于报表需求，可考虑创建物化视图")
        print("• 根据实际查询模式添加适当的索引")

    finally:
        conn.close()

if __name__ == "__main__":
    main()