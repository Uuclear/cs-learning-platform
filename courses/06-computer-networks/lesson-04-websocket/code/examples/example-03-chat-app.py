#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket 简易聊天应用

这个完整的聊天应用包含服务器和客户端功能，
演示了实时聊天的基本原理。
"""

import asyncio
import websockets
import json
from datetime import datetime
import uuid

# 存储连接的客户端和用户信息
clients = {}  # websocket -> user_info

class ChatServer:
    """聊天服务器类"""

    def __init__(self):
        self.clients = {}  # websocket -> user_info

    async def register(self, websocket, username):
        """
        注册新用户

        Args:
            websocket: WebSocket 连接对象
            username: 用户名
        """
        user_id = str(uuid.uuid4())
        self.clients[websocket] = {
            'id': user_id,
            'username': username,
            'connected_at': datetime.now()
        }
        print(f"✅ 用户 {username} (ID: {user_id}) 已加入聊天室")
        await self.send_system_message(f"欢迎 {username} 加入聊天室！")

    async def unregister(self, websocket):
        """
        注销用户

        Args:
            websocket: WebSocket 连接对象
        """
        if websocket in self.clients:
            username = self.clients[websocket]['username']
            del self.clients[websocket]
            print(f"❌ 用户 {username} 已离开聊天室")
            await self.send_system_message(f"{username} 离开了聊天室")

    async def send_system_message(self, message):
        """
        发送系统消息给所有用户

        Args:
            message: 系统消息内容
        """
        system_msg = {
            'type': 'system',
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(system_msg))

    async def broadcast(self, message, sender=None):
        """
        广播消息给所有用户（可选排除发送者）

        Args:
            message: 要广播的消息
            sender: 发送者websocket（可选，如果提供则不发送给发送者）
        """
        if self.clients:
            # 过滤掉已关闭的连接
            active_clients = []
            for client in list(self.clients.keys()):
                try:
                    if sender != client:
                        await client.send(message)
                        active_clients.append(client)
                except websockets.exceptions.ConnectionClosed:
                    # 连接已关闭，稍后会清理
                    pass

            # 清理已关闭的连接
            for client in list(self.clients.keys()):
                if client not in active_clients:
                    await self.unregister(client)

    async def handle_message(self, websocket, message_data):
        """
        处理用户消息

        Args:
            websocket: WebSocket 连接对象
            message_data: 消息数据字典
        """
        if websocket not in self.clients:
            return

        username = self.clients[websocket]['username']
        content = message_data.get('content', '')

        # 创建聊天消息
        chat_message = {
            'type': 'chat',
            'username': username,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }

        # 广播给所有其他用户（不包括发送者）
        await self.broadcast(json.dumps(chat_message), sender=websocket)

    async def handle_client(self, websocket, path):
        """
        处理客户端连接

        Args:
            websocket: WebSocket 连接对象
            path: 请求路径
        """
        try:
            # 首先要求用户提供用户名
            await websocket.send(json.dumps({
                'type': 'request_username',
                'message': '请输入你的用户名:'
            }))

            # 等待用户名
            username_message = await websocket.recv()
            username_data = json.loads(username_message)
            username = username_data.get('username', '匿名用户')

            # 注册用户
            await self.register(websocket, username)

            # 处理后续消息
            async for message in websocket:
                try:
                    message_data = json.loads(message)
                    msg_type = message_data.get('type', 'chat')

                    if msg_type == 'chat':
                        await self.handle_message(websocket, message_data)
                    elif msg_type == 'ping':
                        # 心跳响应
                        await websocket.send(json.dumps({'type': 'pong'}))

                except json.JSONDecodeError:
                    # 忽略无效JSON
                    pass

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

async def main():
    """启动聊天服务器"""
    chat_server = ChatServer()
    print("💬 启动简易聊天服务器...")
    print("📡 监听地址: ws://localhost:8766")
    print("📝 使用 Ctrl+C 停止服务器\n")

    server = await websockets.serve(
        chat_server.handle_client,
        "localhost",
        8766
    )
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 聊天服务器已停止")