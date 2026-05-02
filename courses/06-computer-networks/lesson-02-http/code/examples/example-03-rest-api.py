#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 调用REST API

这个脚本演示如何使用HTTP的不同方法（GET、POST、PUT）
来操作RESTful API，实现对用户资源的CRUD操作。
"""

import requests


def get_users():
    """获取用户列表 (GET)"""
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取用户失败: {response.status_code}")
        return []


def create_user(user_data):
    """创建新用户 (POST)"""
    response = requests.post(
        'https://jsonplaceholder.typicode.com/users',
        json=user_data,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code == 201:
        return response.json()
    else:
        print(f"创建用户失败: {response.status_code}")
        return None


def update_user(user_id, user_data):
    """更新用户 (PUT)"""
    response = requests.put(
        f'https://jsonplaceholder.typicode.com/users/{user_id}',
        json=user_data
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"更新用户失败: {response.status_code}")
        return None


def main():
    """主函数：演示REST API调用"""
    # 获取所有用户
    users = get_users()
    print(f"找到 {len(users)} 个用户")

    # 创建新用户
    new_user = {
        'name': '李四',
        'username': 'lisi',
        'email': 'lisi@example.com'
    }
    created_user = create_user(new_user)
    if created_user:
        print(f"创建用户成功: {created_user['name']}")

    # 更新用户（如果创建成功）
    if created_user:
        updated_data = {**created_user, 'name': '李四（已更新）'}
        updated_user = update_user(created_user['id'], updated_data)
        if updated_user:
            print(f"更新用户成功: {updated_user['name']}")


if __name__ == '__main__':
    main()