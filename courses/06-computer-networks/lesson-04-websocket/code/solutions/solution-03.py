#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：WebSocket聊天室带用户列表

扩展聊天应用，显示当前在线用户列表，并在用户加入/离开时更新列表。
"""

import asyncio
import websockets
import json
from datetime import datetime
import uuid

class AdvancedChatServer:
    def __init__(self):
        self.clients = {}  # websocket -> user_info

    async def get_user_list(self):
        """获取当前在线用户列表"""
        return [info['username'] for info in self.clients.values()]

    async def broadcast_user_list(self):
        """广播更新后的用户列表"""
        user_list = await self.get_user_list()
        message = {
            'type': 'user_list',
            'users': user_list,
            'count': len(user_list)
        }
        await self.broadcast(json.dumps(message))

    async def register(self, websocket, username):
        """注册新用户"""
        user_id = str(uuid.uuid4())
        self.clients[websocket] = {
            'id': user_id,
            'username': username,
            'connected_at': datetime.now()
        }
        print(f"✅ 用户 {username} 已加入")

        # 发送欢迎消息给新用户
        welcome_msg = {
            'type': 'welcome',
            'message': f'欢迎 {username} 加入聊天室！',
            'user_list': await self.get_user_list()
        }
        await websocket.send(json.dumps(welcome_msg))

        # 通知其他用户
        await self.send_system_message(f"{username} 加入了聊天室")
        await self.broadcast_user_list()

    async def unregister(self, websocket):
        """注销用户"""
        if websocket in self.clients:
            username = self.clients[websocket]['username']
            del self.clients[websocket]
            print(f"❌ 用户 {username} 已离开")
            await self.send_system_message(f"{username} 离开了聊天室")
            await self.broadcast_user_list()

    async def send_system_message(self, message):
        """发送系统消息"""
        system_msg = {
            'type': 'system',
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(system_msg))

    async def broadcast(self, message, sender=None):
        """广播消息"""
        if self.clients:
            active_clients = []
            for client in list(self.clients.keys()):
                try:
                    if sender != client:
                        await client.send(message)
                        active_clients.append(client)
                except websockets.exceptions.ConnectionClosed:
                    pass

            # 清理已关闭的连接
            for client in list(self.clients.keys()):
                if client not in active_clients:
                    await self.unregister(client)

    async def handle_message(self, websocket, message_data):
        """处理聊天消息"""
        if websocket not in self.clients:
            return

        username = self.clients[websocket]['username']
        content = message_data.get('content', '')

        chat_message = {
            'type': 'chat',
            'username': username,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }

        await self.broadcast(json.dumps(chat_message), sender=websocket)

    async def handle_client(self, websocket, path):
        """处理客户端连接"""
        try:
            # 请求用户名
            await websocket.send(json.dumps({
                'type': 'request_username',
                'message': '请输入用户名:'
            }))

            username_message = await websocket.recv()
            username_data = json.loads(username_message)
            username = username_data.get('username', '匿名用户')

            await self.register(websocket, username)

            async for message in websocket:
                try:
                    message_data = json.loads(message)
                    msg_type = message_data.get('type', 'chat')

                    if msg_type == 'chat':
                        await self.handle_message(websocket, message_data)
                    elif msg_type == 'ping':
                        await websocket.send(json.dumps({'type': 'pong'}))

                except json.JSONDecodeError:
                    pass

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

async def main():
    chat_server = AdvancedChatServer()
    print("💬 启动高级聊天服务器...")
    print("📡 监听地址: ws://localhost:8768")

    server = await websockets.serve(
        chat_server.handle_client,
        "localhost",
        8768
    )
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")