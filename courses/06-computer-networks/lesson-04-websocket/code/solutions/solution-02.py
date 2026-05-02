#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：带心跳机制的WebSocket客户端

创建一个WebSocket客户端，定期发送心跳消息以保持连接活跃。
"""

import asyncio
import websockets
import json

class HeartbeatClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.heartbeat_interval = 30  # 30秒发送一次心跳

    async def connect(self):
        """连接到服务器"""
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"✅ 已连接到 {self.uri}")
            return True
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

    async def send_heartbeat(self):
        """发送心跳消息"""
        while self.websocket and not self.websocket.closed:
            try:
                heartbeat_msg = {'type': 'ping', 'timestamp': asyncio.get_event_loop().time()}
                await self.websocket.send(json.dumps(heartbeat_msg))
                print("💓 发送心跳")
                await asyncio.sleep(self.heartbeat_interval)
            except Exception as e:
                print(f"❌ 心跳发送失败: {e}")
                break

    async def receive_messages(self):
        """接收消息"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                if data.get('type') == 'pong':
                    print("✅ 收到心跳响应")
                else:
                    print(f"📥 消息: {message}")
        except Exception as e:
            print(f"❌ 接收消息失败: {e}")

    async def run(self):
        """运行客户端"""
        if not await self.connect():
            return

        # 同时运行心跳和消息接收
        await asyncio.gather(
            self.send_heartbeat(),
            self.receive_messages()
        )

async def main():
    client = HeartbeatClient("ws://localhost:8765")
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())