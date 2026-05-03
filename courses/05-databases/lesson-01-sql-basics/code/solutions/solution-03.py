#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL注入防护演示

本脚本演示了SQL注入攻击的危险性以及如何通过参数化查询来防止它。
"""

import sqlite3
import os


def create_test_database():
    """创建测试数据库和用户表"""
    # 删除已存在的数据库文件
    if os.path.exists('users.db'):
        os.remove('users.db')

    # 连接数据库（如果不存在会自动创建）
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 插入一些测试数据
    test_users = [
        ('alice', 'alice@example.com', 'password123'),
        ('bob', 'bob@example.com', 'secure456'),
        ('charlie', 'charlie@example.com', 'mypassword789')
    ]

    cursor.executemany(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        test_users
    )

    conn.commit()
    conn.close()
    print("✅ 测试数据库创建成功！包含3个用户：alice, bob, charlie")


def vulnerable_login(username, password):
    """存在SQL注入漏洞的登录函数（危险示例）"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # ❌ 危险！直接拼接用户输入到SQL语句中
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"❌ 执行的SQL语句: {query}")

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    return result


def secure_login(username, password):
    """安全的登录函数（使用参数化查询）"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # ✅ 安全！使用参数化查询，用户输入被当作纯数据处理
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"✅ 执行的SQL语句: {query}")
    print(f"   参数: username='{username}', password='{password}'")

    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()

    return result


def demonstrate_sql_injection():
    """演示SQL注入攻击"""
    print("\n" + "="*60)
    print("🔍 SQL注入攻击演示")
    print("="*60)

    # 正常登录尝试
    print("\n1️⃣ 正常登录尝试:")
    normal_result = vulnerable_login('alice', 'password123')
    if normal_result:
        print(f"   ✅ 登录成功！用户: {normal_result[1]}")
    else:
        print("   ❌ 登录失败")

    # SQL注入攻击 - 绕过密码验证
    print("\n2️⃣ SQL注入攻击（绕过密码验证）:")
    malicious_username = "alice' --"  # 注释掉密码检查部分
    malicious_password = "任意密码"

    injection_result = vulnerable_login(malicious_username, malicious_password)
    if injection_result:
        print(f"   🚨 攻击成功！用户: {injection_result[1]} 被非法登录！")
    else:
        print("   ✅ 攻击失败（但这种情况很少见）")

    # 更危险的SQL注入 - 获取所有用户
    print("\n3️⃣ 更危险的SQL注入（获取所有用户）:")
    dangerous_input = "' OR '1'='1"
    all_users_result = vulnerable_login(dangerous_input, dangerous_input)
    if all_users_result:
        print(f"   🚨 灾难性攻击成功！获取到第一个用户: {all_users_result[1]}")
        print("   💥 实际上可能返回所有用户数据！")
    else:
        print("   ✅ 攻击失败")


def demonstrate_secure_approach():
    """演示安全的参数化查询方法"""
    print("\n" + "="*60)
    print("🛡️ 安全防护演示（参数化查询）")
    print("="*60)

    # 正常登录
    print("\n1️⃣ 正常登录尝试:")
    normal_result = secure_login('alice', 'password123')
    if normal_result:
        print(f"   ✅ 登录成功！用户: {normal_result[1]}")
    else:
        print("   ❌ 登录失败")

    # 尝试SQL注入攻击（应该失败）
    print("\n2️⃣ SQL注入攻击尝试（应该失败）:")
    malicious_username = "alice' --"
    malicious_password = "任意密码"

    injection_result = secure_login(malicious_username, malicious_password)
    if injection_result:
        print(f"   🚨 攻击意外成功！用户: {injection_result[1]}")
    else:
        print("   ✅ 攻击被成功阻止！")

    # 恶意输入被当作普通字符串处理
    print("\n3️⃣ 恶意输入被安全处理:")
    dangerous_input = "' OR '1'='1"
    safe_result = secure_login(dangerous_input, dangerous_input)
    if safe_result:
        print(f"   🚨 意外找到匹配用户: {safe_result[1]}")
    else:
        print("   ✅ 没有找到匹配用户（恶意输入被当作普通用户名/密码）")


def main():
    """主函数"""
    print("🔒 SQL注入防护演示")
    print("本脚本演示SQL注入的危险性和防护方法\n")

    # 创建测试数据库
    create_test_database()

    # 演示SQL注入攻击
    demonstrate_sql_injection()

    # 演示安全防护
    demonstrate_secure_approach()

    # 清理
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("\n🧹 清理完成：删除测试数据库文件")

    print("\n📚 关键要点:")
    print("• 永远不要直接拼接用户输入到SQL语句中")
    print("• 始终使用参数化查询（?占位符）")
    print("• 参数化查询将用户输入作为纯数据处理，不会被解释为SQL代码")
    print("• 这是防止SQL注入攻击的最有效方法")


if __name__ == "__main__":
    main()