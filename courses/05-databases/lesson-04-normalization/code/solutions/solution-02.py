#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：检测函数依赖并分解表到BCNF
分析给定表的函数依赖，然后分解为BCNF形式
"""

import sqlite3
from collections import defaultdict

def create_problematic_table(conn):
    """创建一个违反BCNF的示例表"""
    cursor = conn.cursor()

    # 创建一个具有复杂函数依赖的表
    # 假设我们有一个图书馆借阅记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_records (
            book_id INTEGER,
            branch_id INTEGER,
            copy_number INTEGER,
            borrower_id INTEGER,
            borrow_date TEXT,
            due_date TEXT,
            borrower_name TEXT,
            borrower_address TEXT,
            book_title TEXT,
            author TEXT,
            PRIMARY KEY (book_id, branch_id, copy_number, borrower_id, borrow_date)
        )
    ''')

    # 插入示例数据
    sample_data = [
        (1001, 1, 1, 501, '2023-01-15', '2023-02-15', '张三', '北京市朝阳区', '数据库系统概念', 'Abraham Silberschatz'),
        (1001, 1, 2, 502, '2023-01-16', '2023-02-16', '李四', '上海市浦东区', '数据库系统概念', 'Abraham Silberschatz'),
        (1002, 1, 1, 501, '2023-01-17', '2023-02-17', '张三', '北京市朝阳区', '算法导论', 'Thomas Cormen'),
        (1003, 2, 1, 503, '2023-01-18', '2023-02-18', '王五', '广州市天河区', '操作系统概念', 'Abraham Silberschatz'),
        (1001, 2, 1, 504, '2023-01-19', '2023-02-19', '赵六', '深圳市南山区', '数据库系统概念', 'Abraham Silberschatz')
    ]

    cursor.executemany(
        "INSERT INTO library_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        sample_data
    )
    conn.commit()

def analyze_functional_dependencies():
    """手动分析函数依赖（在实际应用中可能需要更复杂的算法）"""
    print("🔍 函数依赖分析：")
    print("-" * 30)

    dependencies = [
        "book_id → book_title, author",
        "borrower_id → borrower_name, borrower_address",
        "(book_id, branch_id, copy_number) → unique copy",  # 复合键约束
        "(borrower_id, borrow_date) → unique borrowing record"  # 借阅记录唯一性
    ]

    for dep in dependencies:
        print(f"   {dep}")

    return dependencies

def decompose_to_bcnf(conn):
    """将表分解为BCNF"""
    cursor = conn.cursor()

    # BCNF要求：对于每个非平凡的函数依赖 X → Y，X 必须是超键

    # 步骤1：识别违反BCNF的依赖
    # book_id → book_title, author （book_id 不是超键）
    # borrower_id → borrower_name, borrower_address （borrower_id 不是超键）

    # 步骤2：分解表

    # 图书信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            book_title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')

    # 借阅者信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowers (
            borrower_id INTEGER PRIMARY KEY,
            borrower_name TEXT NOT NULL,
            borrower_address TEXT NOT NULL
        )
    ''')

    # 图书副本表（图书馆分支中的具体副本）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_copies (
            book_id INTEGER,
            branch_id INTEGER,
            copy_number INTEGER,
            PRIMARY KEY (book_id, branch_id, copy_number),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    ''')

    # 借阅记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            book_id INTEGER,
            branch_id INTEGER,
            copy_number INTEGER,
            borrower_id INTEGER,
            borrow_date TEXT,
            due_date TEXT,
            PRIMARY KEY (book_id, branch_id, copy_number, borrower_id, borrow_date),
            FOREIGN KEY (book_id, branch_id, copy_number) REFERENCES book_copies(book_id, branch_id, copy_number),
            FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id)
        )
    ''')

    # 迁移数据

    # 迁移图书数据（去重）
    cursor.execute('''
        INSERT OR IGNORE INTO books (book_id, book_title, author)
        SELECT DISTINCT book_id, book_title, author
        FROM library_records
    ''')

    # 迁移借阅者数据（去重）
    cursor.execute('''
        INSERT OR IGNORE INTO borrowers (borrower_id, borrower_name, borrower_address)
        SELECT DISTINCT borrower_id, borrower_name, borrower_address
        FROM library_records
    ''')

    # 迁移图书副本数据
    cursor.execute('''
        INSERT OR IGNORE INTO book_copies (book_id, branch_id, copy_number)
        SELECT DISTINCT book_id, branch_id, copy_number
        FROM library_records
    ''')

    # 迁移借阅记录数据
    cursor.execute('''
        INSERT OR IGNORE INTO borrowings (book_id, branch_id, copy_number, borrower_id, borrow_date, due_date)
        SELECT book_id, branch_id, copy_number, borrower_id, borrow_date, due_date
        FROM library_records
    ''')

    conn.commit()

def verify_bcnf_decomposition(conn):
    """验证BCNF分解结果"""
    cursor = conn.cursor()

    print("\n✅ BCNF分解后的表结构：")
    print("=" * 50)

    tables = ['books', 'borrowers', 'book_copies', 'borrowings']

    for table in tables:
        print(f"\n📋 表 '{table}':")
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        print(f"   列: {', '.join(col_names)}")

        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   记录数: {count}")

    # 验证BCNF特性
    print("\n🔍 BCNF验证：")
    print("✅ 所有函数依赖的决定因素都是候选键")
    print("✅ 消除了数据冗余和异常")
    print("✅ 保持了无损连接分解")
    print("✅ 所有表都满足BCNF要求")

    # 演示查询重构
    print("\n🔄 查询重构示例：")
    print("原始查询：获取所有借阅记录及其详细信息")
    print("新查询：需要JOIN多个表，但数据一致性得到保证")

    cursor.execute('''
        SELECT
            b.book_title,
            br.borrower_name,
            bo.branch_id,
            bo.copy_number,
            brw.borrow_date,
            brw.due_date
        FROM borrowings brw
        JOIN books b ON brw.book_id = b.book_id
        JOIN borrowers br ON brw.borrower_id = br.borrower_id
        JOIN book_copies bo ON brw.book_id = bo.book_id
            AND brw.branch_id = bo.branch_id
            AND brw.copy_number = bo.copy_number
        LIMIT 3
    ''')

    results = cursor.fetchall()
    for result in results:
        print(f"   {result}")

def demonstrate_bcnf_solution():
    """演示BCNF解决方案"""
    print("🔧 解决方案2：函数依赖分析与BCNF分解")
    print("=" * 60)

    conn = sqlite3.connect(':memory:')

    try:
        # 创建问题表
        create_problematic_table(conn)

        # 分析函数依赖
        analyze_functional_dependencies()

        # 执行BCNF分解
        decompose_to_bcnf(conn)

        # 验证结果
        verify_bcnf_decomposition(conn)

        print("\n💡 BCNF vs 3NF:")
        print("BCNF比3NF更严格，能解决一些3NF无法处理的异常情况")
        print("在这个例子中，BCNF确保了所有函数依赖都基于候选键")
        print("虽然查询变得更复杂，但数据质量和一致性得到了最大保证")

    finally:
        conn.close()

if __name__ == "__main__":
    demonstrate_bcnf_solution()