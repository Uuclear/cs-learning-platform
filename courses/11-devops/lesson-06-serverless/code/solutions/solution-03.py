#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serverless 课程 - 练习题3 解决方案

实现一个完整的 Serverless API 路由器。
"""

import json
import re


class SimpleAPIRouter:
    """简单的 API 路由器"""

    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        """添加路由"""
        key = f"{method.upper()}:{path}"
        # 将路径参数转换为正则表达式
        pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', path)
        self.routes[key] = {
            'handler': handler,
            'pattern': re.compile(f"^{pattern}$")
        }

    def handle_request(self, method, path, body=None):
        """处理请求"""
        for route_key, route_info in self.routes.items():
            route_method, route_path = route_key.split(':', 1)
            if route_method == method.upper() and route_info['pattern'].match(path):
                # 提取路径参数
                match = route_info['pattern'].match(path)
                path_params = match.groupdict() if match else {}

                try:
                    result = route_info['handler'](path_params, body)
                    return {
                        'statusCode': 200,
                        'body': json.dumps(result, ensure_ascii=False),
                        'headers': {'Content-Type': 'application/json'}
                    }
                except Exception as e:
                    return {
                        'statusCode': 500,
                        'body': json.dumps({'error': str(e)}, ensure_ascii=False),
                        'headers': {'Content-Type': 'application/json'}
                    }

        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not found'}, ensure_ascii=False),
            'headers': {'Content-Type': 'application/json'}
        }


# 示例处理器
def get_product_handler(path_params, body):
    """获取产品信息"""
    product_id = path_params.get('id')
    return {
        'id': product_id,
        'name': f'Product {product_id}',
        'price': 99.99
    }


def create_product_handler(path_params, body):
    """创建产品"""
    if not body:
        raise ValueError('Body is required')
    return {
        'id': 'new-product-id',
        'name': body.get('name', 'Unnamed Product'),
        'price': body.get('price', 0)
    }