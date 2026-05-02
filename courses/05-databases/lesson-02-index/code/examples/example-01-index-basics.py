#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: SQLite索引基础操作

演示如何在SQLite中创建和使用索引，以及索引对查询性能的影响。
"""

import sqlite3
import time

def main():
    # 创建数据库连接（使用内存数据库避免磁盘I/O影响）
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            age INTEGER
        )
    ''')

    # 插入大量测试数据（10000条记录）
    print("正在插入10000条测试数据...")
    users_data = [(i, f"user{i}", f"user{i}@example.com", i % 100)
                  for i in range(1, 10001)]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users_data)
    conn.commit()
    print("数据插入完成！\n")

    # 测试无索引查询性能
    print("=== 无索引查询性能测试 ===")
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE email = 'user5000@example.com'")
    result = cursor.fetchone()
    end_time = time.time()
    print(f"查询结果: {result}")
    print(f"无索引查询耗时: {(end_time - start_time) * 1000:.2f} 毫秒\n")

    # 创建索引
    print("=== 创建索引 ===")
    cursor.execute('CREATE INDEX idx_email ON users(email)')
    print("索引 idx_email 创建成功！\n")

    # 测试有索引查询性能
    print("=== 有索引查询性能测试 ===")
    start_time = time.time()
    cursor.execute("SELECT * FROM users WHERE email = 'user5000@example.com'")
    result = cursor.fetchone()
    end_time = time.time()
    print(f"查询结果: {result}")
    print(f"有索引查询耗时: {(end_time - start_time) * 1000:.2f} 毫秒\n")

    # 关闭数据库连接
    conn.close()
    print("🎉 索引性能对比实验完成！")

if __name__ == "__main__":
    main()