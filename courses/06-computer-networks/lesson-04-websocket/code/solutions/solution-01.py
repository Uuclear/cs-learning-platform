#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：简单的WebSocket回显服务器

创建一个WebSocket服务器，接收客户端消息并原样返回。
"""

import asyncio
import websockets

async def echo_handler(websocket, path):
    """回显处理器：接收消息并原样返回"""
    async for message in websocket:
        print(f"收到消息: {message}")
        await websocket.send(message)

async def main():
    """启动回显服务器"""
    print("启动回显服务器 on ws://localhost:8767")
    server = await websockets.serve(echo_handler, "localhost", 8767)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())