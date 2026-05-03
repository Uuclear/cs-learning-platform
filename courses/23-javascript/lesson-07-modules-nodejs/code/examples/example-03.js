// example-03.js - 简单HTTP服务器
// 这个示例展示了如何使用Node.js创建一个简单的HTTP服务器

import http from 'http';
import { URL } from 'url';

// 创建HTTP服务器
const server = http.createServer((req, res) => {
  // 解析URL
  const url = new URL(req.url, `http://${req.headers.host}`);

  console.log(`📥 收到 ${req.method} 请求: ${url.pathname}`);

  // 设置CORS头（允许跨域请求）
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // 处理OPTIONS预检请求
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // 路由处理
  if (req.method === 'GET') {
    if (url.pathname === '/') {
      // 主页
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <title>Node.js 服务器示例</title>
        </head>
        <body>
          <h1>🎉 欢迎使用 Node.js 服务器！</h1>
          <p>这是一个简单的HTTP服务器示例。</p>
          <ul>
            <li><a href="/api/hello">获取问候信息</a></li>
            <li><a href="/api/time">获取当前时间</a></li>
            <li><a href="/api/user/123">获取用户信息</a></li>
          </ul>
        </body>
        </html>
      `);
    } else if (url.pathname === '/api/hello') {
      // API端点 - 问候
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        message: '你好！这是来自Node.js服务器的问候！',
        timestamp: new Date().toISOString()
      }));
    } else if (url.pathname === '/api/time') {
      // API端点 - 当前时间
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        currentTime: new Date().toLocaleString('zh-CN'),
        timezone: 'Asia/Shanghai'
      }));
    } else if (url.pathname.startsWith('/api/user/')) {
      // API端点 - 用户信息（带参数）
      const userId = url.pathname.split('/')[3];
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        id: userId,
        name: `用户${userId}`,
        email: `user${userId}@example.com`,
        createdAt: new Date().toISOString()
      }));
    } else {
      // 404 Not Found
      res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        error: '页面未找到',
        path: url.pathname
      }));
    }
  } else if (req.method === 'POST' && url.pathname === '/api/echo') {
    // 处理POST请求
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
          message: '收到你的数据！',
          received: data,
          timestamp: new Date().toISOString()
        }));
      } catch (error) {
        res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
          error: '无效的JSON格式'
        }));
      }
    });
  } else {
    // 不支持的HTTP方法
    res.writeHead(405, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      error: '不支持的HTTP方法',
      allowedMethods: ['GET', 'POST', 'OPTIONS']
    }));
  }
});

// 错误处理
server.on('error', (error) => {
  console.error('❌ 服务器错误:', error.message);
});

// 启动服务器
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log('✅ HTTP服务器启动成功！');
  console.log(`🌐 访问地址: http://localhost:${PORT}`);
  console.log('💡 按 Ctrl+C 停止服务器');
});