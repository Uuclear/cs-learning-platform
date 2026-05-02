#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 多表关联查询 - 图书馆管理系统
"""

import sqlite3

def create_library_database():
    """创建图书馆数据库"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建作者表
    cursor.execute('''
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    ''')

    # 创建图书表
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            publication_year INTEGER,
            isbn TEXT UNIQUE
        )
    ''')

    # 创建借阅记录表
    cursor.execute('''
        CREATE TABLE borrow_records (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            borrower_name TEXT NOT NULL,
            borrow_date TEXT NOT NULL,
            return_date TEXT
        )
    ''')

    # 插入作者数据
    authors_data = [
        (1, "鲁迅", "中国"),
        (2, "莫言", "中国"),
        (3, "村上春树", "日本"),
        (4, "乔治·奥威尔", "英国")
    ]
    cursor.executemany("INSERT INTO authors VALUES (?, ?, ?)", authors_data)

    # 插入图书数据
    books_data = [
        (1, "呐喊", 1, 1923, "978-7-02-000001-1"),
        (2, "彷徨", 1, 1926, "978-7-02-000002-8"),
        (3, "红高粱家族", 2, 1986, "978-7-5327-00003-5"),
        (4, "挪威的森林", 3, 1987, "978-4-06-000004-2"),
        (5, "1984", 4, 1949, "978-0-452-000005-9")
    ]
    cursor.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?)", books_data)

    # 插入借阅记录
    borrow_records_data = [
        (1, 1, "张三", "2026-04-01", "2026-04-15"),
        (2, 3, "李四", "2026-04-05", None),  # 还未归还
        (3, 4, "王五", "2026-04-10", None),  # 还未归还
        (4, 2, "赵六", "2026-04-12", "2026-04-26")
    ]
    cursor.executemany("INSERT INTO borrow_records VALUES (?, ?, ?, ?, ?)", borrow_records_data)

    conn.commit()
    return conn, cursor

def main():
    conn, cursor = create_library_database()

    print("✅ 图书馆数据库创建成功！")

    # 查询所有图书及其作者信息
    print("\n📚 所有图书及作者:")
    cursor.execute('''
        SELECT b.title, a.name AS author_name, a.country, b.publication_year
        FROM books b
        JOIN authors a ON b.author_id = a.id
        ORDER BY b.publication_year
    ''')
    books_with_authors = cursor.fetchall()
    for title, author, country, year in books_with_authors:
        print(f"  《{title}》 - {author}({country}), {year}年出版")

    # 查询当前借阅中的图书
    print("\n📖 当前借阅中的图书:")
    cursor.execute('''
        SELECT b.title, a.name AS author_name, br.borrower_name, br.borrow_date
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        JOIN authors a ON b.author_id = a.id
        WHERE br.return_date IS NULL
        ORDER BY br.borrow_date
    ''')
    current_borrows = cursor.fetchall()
    for title, author, borrower, borrow_date in current_borrows:
        print(f"  《{title}》 - {author} | 借阅人: {borrower}, 借阅日期: {borrow_date}")

    # 统计每位作者的图书数量
    print("\n📊 作者图书数量统计:")
    cursor.execute('''
        SELECT a.name, COUNT(b.id) as book_count
        FROM authors a
        LEFT JOIN books b ON a.id = b.author_id
        GROUP BY a.id, a.name
        ORDER BY book_count DESC
    ''')
    author_stats = cursor.fetchall()
    for author, count in author_stats:
        print(f"  {author}: {count}本")

    conn.close()

if __name__ == "__main__":
    main()