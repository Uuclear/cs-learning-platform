#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: REST API模拟器

创建一个REST API模拟器，支持对用户资源的CRUD操作。
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
from urllib.parse import urlparse


class UserAPIServer:
    """用户API服务器"""

    def __init__(self):
        """初始化用户存储"""
        self.users = {}
        self.next_id = 1

    def get_all_users(self):
        """获取所有用户"""
        return list(self.users.values())

    def get_user(self, user_id):
        """获取单个用户"""
        return self.users.get(user_id)

    def create_user(self, user_data):
        """创建新用户"""
        user_id = self.next_id
        self.next_id += 1

        # 确保必要的字段存在
        user = {
            'id': user_id,
            'name': user_data.get('name', f'用户{user_id}'),
            'email': user_data.get('email', ''),
            'created_at': '2026-05-03'
        }

        self.users[user_id] = user
        return user

    def update_user(self, user_id, user_data):
        """更新用户"""
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        user['name'] = user_data.get('name', user['name'])
        user['email'] = user_data.get('email', user['email'])
        return user

    def delete_user(self, user_id):
        """删除用户"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


class RESTRequestHandler(BaseHTTPRequestHandler):
    """REST API请求处理器"""

    # 类变量，共享服务器状态
    api_server = UserAPIServer()

    def _send_response(self, status_code, data=None, content_type='application/json'):
        """发送HTTP响应"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

        if data is not None:
            if isinstance(data, dict) or isinstance(data, list):
                response_body = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                response_body = str(data)
            self.wfile.write(response_body.encode('utf-8'))

    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # 路由匹配
        if path == '/users':
            # 获取所有用户
            users = self.api_server.get_all_users()
            self._send_response(200, users)
        elif re.match(r'^/users/(\d+)$', path):
            # 获取单个用户
            user_id = int(re.match(r'^/users/(\d+)$', path).group(1))
            user = self.api_server.get_user(user_id)
            if user:
                self._send_response(200, user)
            else:
                self._send_response(404, {'error': '用户不存在'})
        else:
            self._send_response(404, {'error': '路径不存在'})

    def do_POST(self):
        """处理POST请求"""
        if self.path == '/users':
            # 创建新用户
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')
                try:
                    user_data = json.loads(post_data)
                    new_user = self.api_server.create_user(user_data)
                    self._send_response(201, new_user)
                except json.JSONDecodeError:
                    self._send_response(400, {'error': '无效的JSON格式'})
            else:
                self._send_response(400, {'error': '缺少请求体'})
        else:
            self._send_response(404, {'error': '路径不存在'})

    def do_PUT(self):
        """处理PUT请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if re.match(r'^/users/(\d+)$', path):
            # 更新用户
            user_id = int(re.match(r'^/users/(\d+)$', path).group(1))
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                put_data = self.rfile.read(content_length).decode('utf-8')
                try:
                    user_data = json.loads(put_data)
                    updated_user = self.api_server.update_user(user_id, user_data)
                    if updated_user:
                        self._send_response(200, updated_user)
                    else:
                        self._send_response(404, {'error': '用户不存在'})
                except json.JSONDecodeError:
                    self._send_response(400, {'error': '无效的JSON格式'})
            else:
                self._send_response(400, {'error': '缺少请求体'})
        else:
            self._send_response(404, {'error': '路径不存在'})

    def do_DELETE(self):
        """处理DELETE请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if re.match(r'^/users/(\d+)$', path):
            # 删除用户
            user_id = int(re.match(r'^/users/(\d+)$', path).group(1))
            success = self.api_server.delete_user(user_id)
            if success:
                self._send_response(204)  # No Content
            else:
                self._send_response(404, {'error': '用户不存在'})
        else:
            self._send_response(404, {'error': '路径不存在'})


def main():
    """主函数：启动REST API服务器"""
    server_address = ('localhost', 8081)
    httpd = HTTPServer(server_address, RESTRequestHandler)
    print("REST API服务器启动在 http://localhost:8081")
    print("支持的端点:")
    print("  GET    /users          - 获取所有用户")
    print("  GET    /users/{id}     - 获取单个用户")
    print("  POST   /users          - 创建新用户")
    print("  PUT    /users/{id}     - 更新用户")
    print("  DELETE /users/{id}     - 删除用户")
    print("\n按 Ctrl+C 停止服务器")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close()


if __name__ == '__main__':
    main()