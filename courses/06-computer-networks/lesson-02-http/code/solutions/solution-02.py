#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 简易HTTP客户端

创建一个简易的HTTP客户端类，支持GET和POST请求。
"""

import urllib.request
import urllib.parse
import json


class SimpleHttpClient:
    """简易HTTP客户端"""

    def __init__(self):
        """初始化客户端"""
        self.user_agent = 'SimpleHttpClient/1.0'

    def get(self, url):
        """
        发送GET请求

        Args:
            url (str): 请求URL

        Returns:
            dict: 包含状态码、响应头和响应体的字典
        """
        try:
            # 创建请求对象
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.user_agent)

            # 发送请求并获取响应
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                headers = dict(response.headers)
                body = response.read().decode('utf-8')

            return {
                'status_code': status_code,
                'headers': headers,
                'body': body
            }

        except urllib.error.HTTPError as e:
            return {
                'status_code': e.code,
                'headers': dict(e.headers),
                'body': e.read().decode('utf-8') if e.fp else ''
            }
        except Exception as e:
            return {
                'status_code': 0,
                'headers': {},
                'body': f'请求失败: {str(e)}'
            }

    def post(self, url, data=None):
        """
        发送POST请求

        Args:
            url (str): 请求URL
            data (dict, optional): POST数据

        Returns:
            dict: 包含状态码、响应头和响应体的字典
        """
        try:
            # 准备POST数据
            if data is None:
                data = {}

            # 如果是字典，转换为JSON格式
            if isinstance(data, dict):
                post_data = json.dumps(data).encode('utf-8')
                content_type = 'application/json'
            else:
                post_data = str(data).encode('utf-8')
                content_type = 'text/plain'

            # 创建请求对象
            req = urllib.request.Request(url, data=post_data)
            req.add_header('User-Agent', self.user_agent)
            req.add_header('Content-Type', content_type)
            req.add_header('Content-Length', str(len(post_data)))

            # 发送请求并获取响应
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                headers = dict(response.headers)
                body = response.read().decode('utf-8')

            return {
                'status_code': status_code,
                'headers': headers,
                'body': body
            }

        except urllib.error.HTTPError as e:
            return {
                'status_code': e.code,
                'headers': dict(e.headers),
                'body': e.read().decode('utf-8') if e.fp else ''
            }
        except Exception as e:
            return {
                'status_code': 0,
                'headers': {},
                'body': f'请求失败: {str(e)}'
            }


def main():
    """测试函数"""
    client = SimpleHttpClient()

    # 测试GET请求
    print("=== 测试GET请求 ===")
    result = client.get('https://httpbin.org/get')
    print(f"状态码: {result['status_code']}")
    print(f"响应长度: {len(result['body'])}")

    # 测试POST请求
    print("\n=== 测试POST请求 ===")
    post_data = {'name': '张三', 'age': 25}
    result = client.post('https://httpbin.org/post', post_data)
    print(f"状态码: {result['status_code']}")
    print(f"响应长度: {len(result['body'])}")


if __name__ == '__main__':
    main()