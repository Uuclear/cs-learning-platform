#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 Serverless API 网关 + Lambda 架构

这个脚本演示了如何构建基于 API Gateway 和 Lambda 函数的 Serverless API，
包括路由、参数验证、错误处理和响应格式化。
"""

import json
import re
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass


@dataclass
class APIRequest:
    """API 请求对象"""
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Optional[Dict[str, Any]] = None


@dataclass
class APIResponse:
    """API 响应对象"""
    status_code: int
    body: Dict[str, Any]
    headers: Dict[str, str]


class ServerlessAPIRouter:
    """Serverless API 路由器，模拟 API Gateway 功能"""

    def __init__(self):
        self.routes = {}

    def add_route(self, method: str, path: str, handler: Callable) -> None:
        """
        添加路由规则

        Args:
            method: HTTP 方法 (GET, POST, PUT, DELETE)
            path: 路径模式，支持路径参数如 /users/{id}
            handler: 处理函数
        """
        key = f"{method.upper()}:{path}"
        self.routes[key] = {
            'handler': handler,
            'pattern': self._compile_path_pattern(path)
        }

    def _compile_path_pattern(self, path: str) -> re.Pattern:
        """编译路径模式，支持路径参数"""
        # 将 /users/{id} 转换为正则表达式 /users/(?P<id>[^/]+)
        pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', path)
        return re.compile(f"^{pattern}$")

    def handle_request(self, request: APIRequest) -> APIResponse:
        """
        处理 API 请求

        Args:
            request: API 请求对象

        Returns:
            API 响应对象
        """
        # 查找匹配的路由
        for route_key, route_info in self.routes.items():
            method, path = route_key.split(':', 1)
            if method == request.method.upper() and route_info['pattern'].match(request.path):
                # 提取路径参数
                match = route_info['pattern'].match(request.path)
                path_params = match.groupdict() if match else {}

                try:
                    # 调用处理函数
                    result = route_info['handler'](
                        request=request,
                        path_params=path_params
                    )

                    # 确保返回正确的响应格式
                    if isinstance(result, dict):
                        return APIResponse(
                            status_code=result.get('statusCode', 200),
                            body=result.get('body', {}),
                            headers=result.get('headers', {'Content-Type': 'application/json'})
                        )
                    else:
                        return APIResponse(200, {'result': str(result)}, {'Content-Type': 'application/json'})

                except Exception as e:
                    return self._create_error_response(500, f"内部服务器错误: {str(e)}")

        # 未找到路由
        return self._create_error_response(404, f"未找到 {request.method} {request.path}")

    def _create_error_response(self, status_code: int, message: str) -> APIResponse:
        """创建错误响应"""
        return APIResponse(
            status_code=status_code,
            body={'error': message},
            headers={'Content-Type': 'application/json'}
        )


# 示例处理函数
def get_user_handler(request: APIRequest, path_params: Dict[str, str]) -> Dict[str, Any]:
    """获取用户信息的处理函数"""
    user_id = path_params.get('id')

    # 模拟数据库查询
    users = {
        '1': {'id': '1', 'name': '张三', 'email': 'zhangsan@example.com'},
        '2': {'id': '2', 'name': '李四', 'email': 'lisi@example.com'}
    }

    if user_id in users:
        return {
            'statusCode': 200,
            'body': users[user_id],
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 404,
            'body': {'error': f'用户 {user_id} 不存在'},
            'headers': {'Content-Type': 'application/json'}
        }


def create_user_handler(request: APIRequest, path_params: Dict[str, str]) -> Dict[str, Any]:
    """创建用户的处理函数"""
    if not request.body:
        return {
            'statusCode': 400,
            'body': {'error': '请求体不能为空'},
            'headers': {'Content-Type': 'application/json'}
        }

    # 验证必需字段
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in request.body:
            return {
                'statusCode': 400,
                'body': {'error': f'缺少必需字段: {field}'},
                'headers': {'Content-Type': 'application/json'}
            }

    # 模拟创建用户
    new_user = {
        'id': '3',  # 简单模拟自动生成ID
        'name': request.body['name'],
        'email': request.body['email']
    }

    return {
        'statusCode': 201,
        'body': new_user,
        'headers': {'Content-Type': 'application/json'}
    }


def health_check_handler(request: APIRequest, path_params: Dict[str, str]) -> Dict[str, Any]:
    """健康检查处理函数"""
    return {
        'statusCode': 200,
        'body': {'status': 'healthy', 'timestamp': '2026-05-03T12:00:00Z'},
        'headers': {'Content-Type': 'application/json'}
    }


def main():
    """主函数 - 演示 Serverless API 的使用"""
    print("=== Serverless API 网关 + Lambda 模拟演示 ===\n")

    # 创建 API 路由器
    router = ServerlessAPIRouter()

    # 注册路由
    router.add_route('GET', '/health', health_check_handler)
    router.add_route('GET', '/users/{id}', get_user_handler)
    router.add_route('POST', '/users', create_user_handler)

    # 测试请求1: 健康检查
    print("1. 健康检查请求:")
    health_request = APIRequest(
        method='GET',
        path='/health',
        headers={'Accept': 'application/json'},
        query_params={}
    )
    health_response = router.handle_request(health_request)
    print(f"   状态码: {health_response.status_code}")
    print(f"   响应: {json.dumps(health_response.body, ensure_ascii=False)}\n")

    # 测试请求2: 获取存在的用户
    print("2. 获取用户信息 (存在):")
    user_request = APIRequest(
        method='GET',
        path='/users/1',
        headers={'Accept': 'application/json'},
        query_params={}
    )
    user_response = router.handle_request(user_request)
    print(f"   状态码: {user_response.status_code}")
    print(f"   响应: {json.dumps(user_response.body, ensure_ascii=False)}\n")

    # 测试请求3: 获取不存在的用户
    print("3. 获取用户信息 (不存在):")
    not_found_request = APIRequest(
        method='GET',
        path='/users/999',
        headers={'Accept': 'application/json'},
        query_params={}
    )
    not_found_response = router.handle_request(not_found_request)
    print(f"   状态码: {not_found_response.status_code}")
    print(f"   响应: {json.dumps(not_found_response.body, ensure_ascii=False)}\n")

    # 测试请求4: 创建新用户
    print("4. 创建新用户:")
    create_request = APIRequest(
        method='POST',
        path='/users',
        headers={'Content-Type': 'application/json'},
        query_params={},
        body={'name': '王五', 'email': 'wangwu@example.com'}
    )
    create_response = router.handle_request(create_request)
    print(f"   状态码: {create_response.status_code}")
    print(f"   响应: {json.dumps(create_response.body, ensure_ascii=False)}\n")

    # 测试请求5: 错误的请求 (缺少必需字段)
    print("5. 创建用户失败 (缺少字段):")
    bad_request = APIRequest(
        method='POST',
        path='/users',
        headers={'Content-Type': 'application/json'},
        query_params={},
        body={'name': '赵六'}  # 缺少 email 字段
    )
    bad_response = router.handle_request(bad_request)
    print(f"   状态码: {bad_response.status_code}")
    print(f"   响应: {json.dumps(bad_response.body, ensure_ascii=False)}\n")

    # 测试请求6: 404 路由
    print("6. 未找到的路由:")
    not_found_route = APIRequest(
        method='GET',
        path='/nonexistent',
        headers={'Accept': 'application/json'},
        query_params={}
    )
    not_found_route_response = router.handle_request(not_found_route)
    print(f"   状态码: {not_found_route_response.status_code}")
    print(f"   响应: {json.dumps(not_found_route_response.body, ensure_ascii=False)}\n")

    print("=== 演示完成 ===")


if __name__ == '__main__':
    main()