#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: TCP客户端/服务器通信

演示TCP协议的面向连接特性，实现简单的客户端-服务器通信。
服务器监听指定端口，客户端连接后发送消息，服务器回复确认。
"""

import socket
import threading
import time

def tcp_server():
    """TCP服务器：监听连接并处理客户端请求"""
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置socket选项：允许重用地址（避免"Address already in use"错误）
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # 绑定到本地地址和端口
        server_address = ('localhost', 8888)
        server_socket.bind(server_address)
        print(f"服务器启动，监听 {server_address[0]}:{server_address[1]}...")

        # 开始监听连接（最大排队连接数为1）
        server_socket.listen(1)

        # 接受客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"客户端 {client_address} 已连接")

        try:
            # 接收客户端数据（最多1024字节）
            data = client_socket.recv(1024)
            if data:
                message = data.decode('utf-8')
                print(f"收到客户端消息: {message}")

                # 构造响应消息
                response = f"服务器已收到您的消息: '{message}'"
                client_socket.send(response.encode('utf-8'))
                print("已发送响应给客户端")

        finally:
            # 关闭客户端连接
            client_socket.close()

    finally:
        # 关闭服务器socket
        server_socket.close()

def tcp_client():
    """TCP客户端：连接服务器并发送消息"""
    # 等待服务器启动
    time.sleep(0.5)

    # 创建TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到服务器
        server_address = ('localhost', 8888)
        client_socket.connect(server_address)
        print(f"已连接到服务器 {server_address[0]}:{server_address[1]}")

        # 发送消息给服务器
        message = "Hello, TCP Server! 这是一个测试消息。"
        client_socket.send(message.encode('utf-8'))
        print(f"已发送消息: {message}")

        # 接收服务器响应
        response = client_socket.recv(1024)
        if response:
            response_message = response.decode('utf-8')
            print(f"收到服务器响应: {response_message}")

    finally:
        # 关闭客户端socket
        client_socket.close()

def main():
    """主函数：启动服务器线程，然后运行客户端"""
    # 在后台线程中启动服务器
    server_thread = threading.Thread(target=tcp_server)
    server_thread.daemon = True  # 设置为守护线程，主线程结束时自动结束
    server_thread.start()

    # 运行客户端
    tcp_client()

    print("\nTCP客户端/服务器通信演示完成！")

if __name__ == "__main__":
    main()