#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket 客户端示例

这个客户端演示了如何连接到 WebSocket 服务器，
发送消息，并接收服务器的响应。
"""

import asyncio
import websockets
import json
import sys

async def websocket_client():
    """
    WebSocket 客户端主函数
    """
    uri = "ws://localhost:8765"

    try:
        # 连接到 WebSocket 服务器
        async with websockets.connect(uri) as websocket:
            print(f"✅ 已连接到 WebSocket 服务器: {uri}")
            print("📝 输入消息并按回车发送（输入 'quit' 退出）\n")

            # 创建两个任务：一个用于接收消息，一个用于发送消息
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket))

            # 等待任一任务完成
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # 取消未完成的任务
            for task in pending:
                task.cancel()

    except ConnectionRefusedError:
        print("❌ 无法连接到服务器！请确保服务器正在运行。")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 客户端已停止")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

async def receive_messages(websocket):
    """
    接收来自服务器的消息

    Args:
        websocket: WebSocket 连接对象
    """
    try:
        async for message in websocket:
            print(f"📥 服务器消息: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("❌ 与服务器的连接已关闭")

async def send_messages(websocket):
    """
    向服务器发送消息

    Args:
        websocket: WebSocket 连接对象
    """
    while True:
        # 从用户获取输入
        user_input = await asyncio.get_event_loop().run_in_executor(
            None, input, "💬 你的消息: "
        )

        if user_input.lower() == 'quit':
            break

        # 创建消息对象
        message = {
            'type': 'message',
            'content': user_input
        }

        # 发送消息到服务器
        await websocket.send(json.dumps(message))

if __name__ == "__main__":
    asyncio.run(websocket_client())