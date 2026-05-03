#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试示例：模拟API和数据库集成测试

本文件展示了：
1. 如何模拟数据库操作进行集成测试
2. API端点的集成测试模式
3. 测试数据准备和清理策略
4. 事务回滚确保测试隔离性
"""

import unittest
from datetime import datetime


class MockDatabase:
    """模拟数据库，用于集成测试"""

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.next_user_id = 1
        self.next_post_id = 1

    def create_user(self, username, email):
        """创建用户"""
        user_id = self.next_user_id
        self.next_user_id += 1

        user = {
            'id': user_id,
            'username': username,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        self.users[user_id] = user
        return user

    def get_user(self, user_id):
        """获取用户"""
        return self.users.get(user_id)

    def create_post(self, user_id, title, content):
        """创建文章"""
        if user_id not in self.users:
            raise ValueError("用户不存在")

        post_id = self.next_post_id
        self.next_post_id += 1

        post = {
            'id': post_id,
            'user_id': user_id,
            'title': title,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'status': 'published'
        }
        self.posts[post_id] = post
        return post

    def get_user_posts(self, user_id):
        """获取用户的所有文章"""
        return [post for post in self.posts.values() if post['user_id'] == user_id]

    def cleanup(self):
        """清理测试数据"""
        self.users.clear()
        self.posts.clear()
        self.next_user_id = 1
        self.next_post_id = 1


class BlogAPI:
    """博客API服务"""

    def __init__(self, database):
        self.db = database

    def register_user(self, username, email):
        """注册用户API"""
        if not username or not email:
            return {'error': '用户名和邮箱不能为空', 'code': 400}

        if '@' not in email:
            return {'error': '邮箱格式无效', 'code': 400}

        try:
            user = self.db.create_user(username, email)
            return {'user': user, 'code': 201}
        except Exception as e:
            return {'error': f'注册失败: {str(e)}', 'code': 500}

    def create_blog_post(self, user_id, title, content):
        """创建博客文章API"""
        if not user_id or not title or not content:
            return {'error': '用户ID、标题和内容都不能为空', 'code': 400}

        if len(title) > 100:
            return {'error': '标题不能超过100个字符', 'code': 400}

        try:
            post = self.db.create_post(user_id, title, content)
            return {'post': post, 'code': 201}
        except ValueError as e:
            return {'error': str(e), 'code': 404}
        except Exception as e:
            return {'error': f'创建文章失败: {str(e)}', 'code': 500}

    def get_user_feed(self, user_id):
        """获取用户动态API"""
        try:
            posts = self.db.get_user_posts(user_id)
            return {'posts': posts, 'code': 200}
        except Exception as e:
            return {'error': f'获取动态失败: {str(e)}', 'code': 500}


class TestBlogAPIIntegration(unittest.TestCase):
    """博客API集成测试"""

    def setUp(self):
        """每个测试前初始化新的数据库"""
        self.db = MockDatabase()
        self.api = BlogAPI(self.db)

    def tearDown(self):
        """每个测试后清理数据"""
        self.db.cleanup()

    def test_user_registration_success(self):
        """测试用户注册成功场景"""
        # 执行API调用
        response = self.api.register_user("alice", "alice@example.com")

        # 验证响应
        self.assertEqual(response['code'], 201)
        self.assertIn('user', response)
        self.assertEqual(response['user']['username'], "alice")
        self.assertEqual(response['user']['email'], "alice@example.com")

        # 验证数据确实存储在数据库中
        stored_user = self.db.get_user(response['user']['id'])
        self.assertIsNotNone(stored_user)
        self.assertEqual(stored_user['username'], "alice")

    def test_user_registration_invalid_email(self):
        """测试无效邮箱注册"""
        response = self.api.register_user("bob", "invalid-email")
        self.assertEqual(response['code'], 400)
        self.assertIn('邮箱格式无效', response['error'])

    def test_user_registration_empty_fields(self):
        """测试空字段注册"""
        response = self.api.register_user("", "test@example.com")
        self.assertEqual(response['code'], 400)
        self.assertIn('不能为空', response['error'])

    def test_create_post_success(self):
        """测试成功创建文章"""
        # 先创建用户
        user_response = self.api.register_user("charlie", "charlie@example.com")
        user_id = user_response['user']['id']

        # 创建文章
        post_response = self.api.create_blog_post(user_id, "我的第一篇文章", "这是文章内容")

        # 验证响应
        self.assertEqual(post_response['code'], 201)
        self.assertIn('post', post_response)
        self.assertEqual(post_response['post']['title'], "我的第一篇文章")
        self.assertEqual(post_response['post']['user_id'], user_id)

        # 验证文章存储在数据库中
        posts = self.db.get_user_posts(user_id)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], "我的第一篇文章")

    def test_create_post_nonexistent_user(self):
        """测试为不存在的用户创建文章"""
        response = self.api.create_blog_post(999, "标题", "内容")
        self.assertEqual(response['code'], 404)
        self.assertIn('用户不存在', response['error'])

    def test_create_post_title_too_long(self):
        """测试标题过长"""
        user_response = self.api.register_user("david", "david@example.com")
        user_id = user_response['user']['id']

        long_title = "A" * 101  # 101个字符
        response = self.api.create_blog_post(user_id, long_title, "内容")
        self.assertEqual(response['code'], 400)
        self.assertIn('不能超过100个字符', response['error'])

    def test_user_feed_retrieval(self):
        """测试用户动态获取"""
        # 创建用户
        user_response = self.api.register_user("eve", "eve@example.com")
        user_id = user_response['user']['id']

        # 创建多篇文章
        self.api.create_blog_post(user_id, "文章1", "内容1")
        self.api.create_blog_post(user_id, "文章2", "内容2")

        # 获取动态
        feed_response = self.api.get_user_feed(user_id)

        # 验证结果
        self.assertEqual(feed_response['code'], 200)
        self.assertEqual(len(feed_response['posts']), 2)
        titles = [post['title'] for post in feed_response['posts']]
        self.assertIn("文章1", titles)
        self.assertIn("文章2", titles)

    def test_isolation_between_tests(self):
        """测试测试之间的隔离性"""
        # 这个测试验证每个测试都有独立的数据库状态
        users = list(self.db.users.values())
        posts = list(self.db.posts.values())
        self.assertEqual(len(users), 0)
        self.assertEqual(len(posts), 0)


if __name__ == '__main__':
    # 运行集成测试
    unittest.main(verbosity=2)