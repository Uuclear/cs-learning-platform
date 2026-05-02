#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: SQL基础CRUD操作
演示如何使用SQLite进行基本的增删改查操作
"""

import sqlite3
import os

def main():
    # 创建内存数据库（也可以使用文件数据库）
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')

    print("✅ 创建用户表成功！")

    # INSERT - 插入数据 (Create)
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        ("张三", "zhangsan@example.com", 25)
    )
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        ("李四", "lisi@example.com", 30)
    )
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        ("王五", "wangwu@example.com", 28)
    )
    conn.commit()
    print("✅ 插入3条用户数据成功！")

    # SELECT - 查询数据 (Read)
    print("\n📋 查询所有用户:")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"  ID: {user[0]}, 姓名: {user[1]}, 邮箱: {user[2]}, 年龄: {user[3]}")

    # UPDATE - 更新数据 (Update)
    cursor.execute(
        "UPDATE users SET age = ? WHERE name = ?",
        (26, "张三")
    )
    conn.commit()
    print(f"\n✅ 更新了 {cursor.rowcount} 条记录 (张三年龄从25改为26)")

    # 再次查询验证更新
    print("\n📋 更新后查询张三的信息:")
    cursor.execute("SELECT * FROM users WHERE name = ?", ("张三",))
    updated_user = cursor.fetchone()
    print(f"  ID: {updated_user[0]}, 姓名: {updated_user[1]}, 邮箱: {updated_user[2]}, 年龄: {updated_user[3]}")

    # DELETE - 删除数据 (Delete)
    cursor.execute("DELETE FROM users WHERE age < ?", (27,))
    conn.commit()
    print(f"\n✅ 删除了 {cursor.rowcount} 条记录 (年龄小于27的用户)")

    # 最终查询所有剩余用户
    print("\n📋 最终用户列表:")
    cursor.execute("SELECT * FROM users")
    final_users = cursor.fetchall()
    if final_users:
        for user in final_users:
            print(f"  ID: {user[0]}, 姓名: {user[1]}, 邮箱: {user[2]}, 年龄: {user[3]}")
    else:
        print("  📭 没有剩余用户！")

    # 关闭连接
    conn.close()
    print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()