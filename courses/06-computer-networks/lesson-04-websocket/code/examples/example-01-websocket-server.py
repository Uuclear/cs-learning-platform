#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket 服务器示例

这个简单的 WebSocket 服务器演示了如何建立 WebSocket 连接，
处理客户端消息，并向所有连接的客户端广播消息。
"""

import asyncio
import websockets
import json
from datetime import datetime

# 存储所有连接的客户端
connected_clients = set()

async def handle_client(websocket, path):
    """
    处理单个客户端连接

    Args:
        websocket: WebSocket 连接对象
        path: 请求路径
    """
    # 将新客户端添加到连接集合中
    connected_clients.add(websocket)
    print(f"✅ 新客户端已连接！当前连接数: {len(connected_clients)}")

    try:
        # 持续接收客户端消息
        async for message in websocket:
            print(f"📥 收到消息: {message}")

            # 解析消息（假设是JSON格式）
            try:
                data = json.loads(message)
                msg_type = data.get('type', 'message')
                content = data.get('content', '')

                # 创建响应消息
                response = {
                    'type': 'response',
                    'content': f"服务器收到: {content}",
                    'timestamp': datetime.now().isoformat(),
                    'from_server': True
                }

                # 广播消息给所有客户端（包括发送者）
                await broadcast(json.dumps(response))

            except json.JSONDecodeError:
                # 如果不是JSON格式，直接回显
                await websocket.send(f"回显: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("❌ 客户端断开连接")
    finally:
        # 从连接集合中移除客户端
        connected_clients.remove(websocket)
        print(f"🔌 客户端已断开！剩余连接数: {len(connected_clients)}")

async def broadcast(message):
    """
    向所有连接的客户端广播消息

    Args:
        message: 要广播的消息字符串
    """
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

async def main():
    """主函数：启动WebSocket服务器"""
    print("🚀 启动 WebSocket 服务器...")
    print("📡 监听地址: ws://localhost:8765")
    print("📝 使用 Ctrl+C 停止服务器\n")

    # 启动WebSocket服务器
    server = await websockets.serve(handle_client, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")