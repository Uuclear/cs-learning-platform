#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 创建简易HTTP服务器

这个脚本演示如何使用Python内置的http.server模块
创建一个支持GET和POST请求的简易HTTP服务器。
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """简易HTTP请求处理器"""

    def do_GET(self):
        """处理GET请求"""
        # 设置响应状态码和头部
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # 准备响应数据
        response_data = {
            'message': '你好，这是我的第一个HTTP服务器！',
            'path': self.path,
            'method': 'GET'
        }

        # 发送响应体
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        """处理POST请求"""
        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # 设置响应
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # 返回接收到的数据
        response_data = {
            'received': post_data,
            'message': '数据接收成功！'
        }
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))


def main():
    """主函数：启动HTTP服务器"""
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("服务器启动在 http://localhost:8080")
    print("按 Ctrl+C 停止服务器")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close()


if __name__ == '__main__':
    main()