#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：单元测试重构

重构后的代码使用依赖注入，使单元测试更容易编写。
"""

import unittest
from unittest.mock import Mock


class Database:
    """数据库接口"""
    def get_user(self, user_id):
        # 实际实现会查询数据库
        pass


class ApiClient:
    """API客户端接口"""
    def get_user_info(self, email):
        # 实际实现会调用外部API
        pass


class Cache:
    """缓存接口"""
    def set(self, key, value):
        # 实际实现会设置缓存
        pass


def process_user_data(user_id, database, api_client, cache):
    """
    处理用户数据的函数，使用依赖注入

    Args:
        user_id: 用户ID
        database: 数据库实例
        api_client: API客户端实例
        cache: 缓存实例
    """
    # 从数据库获取用户
    user = database.get_user(user_id)
    # 调用外部API获取额外信息
    extra_info = api_client.get_user_info(user.email)
    # 处理数据
    result = {
        'name': user.name,
        'email': user.email,
        'score': extra_info['reputation_score']
    }
    # 保存到缓存
    cache.set(f"user:{user_id}", result)
    return result


class TestProcessUserData(unittest.TestCase):
    """重构后的单元测试"""

    def test_process_user_data_success(self):
        # 创建模拟对象
        mock_db = Mock()
        mock_api = Mock()
        mock_cache = Mock()

        # 设置模拟行为
        mock_user = Mock()
        mock_user.name = "张三"
        mock_user.email = "zhangsan@example.com"
        mock_db.get_user.return_value = mock_user

        mock_api.get_user_info.return_value = {'reputation_score': 95}

        # 执行测试
        result = process_user_data(123, mock_db, mock_api, mock_cache)

        # 验证结果
        self.assertEqual(result['name'], "张三")
        self.assertEqual(result['email'], "zhangsan@example.com")
        self.assertEqual(result['score'], 95)

        # 验证依赖被正确调用
        mock_db.get_user.assert_called_once_with(123)
        mock_api.get_user_info.assert_called_once_with("zhangsan@example.com")
        mock_cache.set.assert_called_once_with("user:123", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)