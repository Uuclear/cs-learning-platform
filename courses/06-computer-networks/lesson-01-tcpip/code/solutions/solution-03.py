#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: HTTP客户端实现

使用socket库实现简单的HTTP客户端，发送GET请求并解析响应。
"""

import socket
import sys
from urllib.parse import urlparse

def parse_url(url):
    """解析URL，提取主机、端口、路径等信息"""
    # 如果URL没有协议前缀，添加http://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    path = parsed.path or '/'
    if parsed.query:
        path += '?' + parsed.query

    return host, port, path, parsed.scheme

def create_http_request(host, path):
    """构造HTTP/1.1 GET请求"""
    request = f"GET {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += "Connection: close\r\n"  # 请求后关闭连接
    request += "User-Agent: SimpleHTTPClient/1.0\r\n"
    request += "\r\n"  # 空行表示请求头结束
    return request

def parse_http_response(response_data):
    """解析HTTP响应"""
    # 将字节数据转换为字符串
    response_text = response_data.decode('utf-8', errors='ignore')

    # 按行分割
    lines = response_text.split('\r\n')
    if not lines:
        return None, None, None

    # 解析状态行
    status_line = lines[0]
    parts = status_line.split(' ', 2)
    if len(parts) < 2:
        return None, None, None

    http_version = parts[0]
    status_code = parts[1]
    status_message = parts[2] if len(parts) > 2 else ""

    # 找到空行位置（头部和体的分界）
    try:
        empty_line_index = lines.index('')
        headers = lines[1:empty_line_index]
        body = '\r\n'.join(lines[empty_line_index + 1:])
    except ValueError:
        # 没有找到空行，可能只有头部
        headers = lines[1:]
        body = ""

    return (http_version, status_code, status_message), headers, body

def http_get(url, timeout=10):
    """
    发送HTTP GET请求

    Args:
        url: 目标URL
        timeout: 超时时间（秒）

    Returns:
        tuple: (status_info, headers, body)
    """
    try:
        # 解析URL
        host, port, path, scheme = parse_url(url)

        if scheme == 'https':
            print("错误：此简单客户端不支持HTTPS，请使用HTTP URL")
            return None, None, None

        # 创建socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        print(f"连接到 {host}:{port}...")
        sock.connect((host, port))

        # 构造并发送HTTP请求
        request = create_http_request(host, path)
        print(f"发送请求: GET {path}")
        sock.send(request.encode('utf-8'))

        # 接收响应
        print("接收响应...")
        response_data = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            except socket.timeout:
                print("警告：接收超时，但已收到部分数据")
                break

        sock.close()

        # 解析响应
        status_info, headers, body = parse_http_response(response_data)
        return status_info, headers, body

    except socket.error as e:
        print(f"网络错误: {e}")
        return None, None, None
    except Exception as e:
        print(f"错误: {e}")
        return None, None, None

def main():
    # 默认URL
    default_url = "http://httpbin.org/get"

    # 获取目标URL（从命令行参数或使用默认值）
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = default_url

    print(f"=== HTTP客户端 ===")
    print(f"请求URL: {target_url}")
    print()

    # 发送请求
    status_info, headers, body = http_get(target_url)

    if status_info is None:
        print("请求失败！")
        return

    # 显示响应信息
    http_version, status_code, status_message = status_info
    print(f"=== 响应状态 ===")
    print(f"{http_version} {status_code} {status_message}")
    print()

    print(f"=== 响应头 ===")
    for header in headers:
        print(header)
    print()

    print(f"=== 响应体 ===")
    print(body[:500] + "..." if len(body) > 500 else body)
    print()

    # 处理重定向
    if status_code in ['301', '302', '307', '308']:
        for header in headers:
            if header.lower().startswith('location:'):
                redirect_url = header.split(':', 1)[1].strip()
                print(f"注意：这是一个重定向响应，目标URL是: {redirect_url}")

if __name__ == "__main__":
    main()