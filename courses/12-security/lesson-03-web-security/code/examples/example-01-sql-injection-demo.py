#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL注入演示与防御

本示例展示了SQL注入攻击的原理以及如何使用参数化查询进行防御。
注意：此代码仅用于教育目的，切勿在生产环境中使用不安全的查询方式。
"""

import sqlite3
import os


def setup_database():
    """创建示例数据库"""
    conn = sqlite3.connect(':memory:')  # 使用内存数据库
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')

    # 插入示例数据
    cursor.executemany('''
        INSERT INTO users (username, password, email) VALUES (?, ?, ?)
    ''', [
        ('alice', 'password123', 'alice@example.com'),
        ('bob', 'securepass', 'bob@example.com'),
        ('admin', 'supersecret', 'admin@example.com')
    ])

    conn.commit()
    return conn


def unsafe_query(conn, username):
    """
    不安全的查询方式 - 易受SQL注入攻击

    攻击示例：
    - 正常输入: 'alice'
    - 注入攻击: "admin'--" (注释掉密码检查)
    - 注入攻击: "x' OR '1'='1" (绕过所有条件)
    """
    cursor = conn.cursor()
    # 危险！直接拼接用户输入到SQL查询中
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"执行的SQL语句: {query}")
    cursor.execute(query)
    return cursor.fetchall()


def safe_query(conn, username):
    """
    安全的查询方式 - 使用参数化查询

    参数化查询会自动转义用户输入，防止SQL注入攻击
    """
    cursor = conn.cursor()
    # 安全！使用参数占位符
    query = "SELECT * FROM users WHERE username = ?"
    print(f"执行的SQL语句: {query} (参数: {username})")
    cursor.execute(query, (username,))
    return cursor.fetchall()


def main():
    """主函数 - 演示SQL注入攻击与防御"""
    print("=== SQL注入演示与防御 ===\n")

    # 设置数据库
    conn = setup_database()

    try:
        # 测试正常查询
        print("1. 正常查询测试:")
        print("查询用户: alice")
        result = safe_query(conn, 'alice')
        print(f"结果: {result}\n")

        # 演示SQL注入攻击
        print("2. SQL注入攻击演示 (不安全查询):")
        malicious_input = "admin'--"
        print(f"恶意输入: {malicious_input}")
        result = unsafe_query(conn, malicious_input)
        print(f"攻击结果: {result}")
        print("注意：攻击者成功绕过了认证！\n")

        # 演示安全查询的防护效果
        print("3. 安全查询防护演示:")
        print(f"同样的恶意输入: {malicious_input}")
        result = safe_query(conn, malicious_input)
        print(f"防护结果: {result}")
        print("注意：安全查询正确处理了恶意输入，没有返回任何用户！\n")

        # 另一个注入示例
        print("4. 另一个注入攻击示例:")
        malicious_input2 = "x' OR '1'='1"
        print(f"恶意输入: {malicious_input2}")
        print("不安全查询结果:")
        result_unsafe = unsafe_query(conn, malicious_input2)
        print(f"返回了所有用户: {len(result_unsafe)} 条记录")

        print("安全查询结果:")
        result_safe = safe_query(conn, malicious_input2)
        print(f"正确处理: {result_safe}\n")

    finally:
        conn.close()


if __name__ == "__main__":
    main()