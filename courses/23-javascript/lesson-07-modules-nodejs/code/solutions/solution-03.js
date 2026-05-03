// solution-03.js - HTTP服务器解决方案
// 这是练习3的完整解决方案

import http from 'http';
import { URL } from 'url';

class APIServer {
  constructor(port = 3000) {
    this.port = port;
    this.server = null;
    this.routes = new Map();

    // 初始化路由
    this.setupRoutes();
  }

  setupRoutes() {
    // GET /api/users - 获取所有用户
    this.addRoute('GET', '/api/users', (req, res) => {
      const users = [
        { id: 1, name: '张三', email: 'zhangsan@example.com' },
        { id: 2, name: '李四', email: 'lisi@example.com' },
        { id: 3, name: '王五', email: 'wangwu@example.com' }
      ];

      this.sendJSON(res, 200, users);
    });

    // GET /api/users/:id - 获取单个用户
    this.addRoute('GET', '/api/users/', (req, res, params) => {
      const userId = parseInt(params.id);
      const users = [
        { id: 1, name: '张三', email: 'zhangsan@example.com' },
        { id: 2, name: '李四', email: 'lisi@example.com' },
        { id: 3, name: '王五', email: 'wangwu@example.com' }
      ];

      const user = users.find(u => u.id === userId);
      if (user) {
        this.sendJSON(res, 200, user);
      } else {
        this.sendJSON(res, 404, { error: '用户不存在' });
      }
    });

    // POST /api/users - 创建新用户
    this.addRoute('POST', '/api/users', async (req, res) => {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });

      req.on('end', () => {
        try {
          const userData = JSON.parse(body);
          const newUser = {
            id: Date.now(), // 简单的ID生成
            ...userData,
            createdAt: new Date().toISOString()
          };

          this.sendJSON(res, 201, {
            message: '用户创建成功',
            user: newUser
          });
        } catch (error) {
          this.sendJSON(res, 400, { error: '无效的JSON数据' });
        }
      });
    });

    // GET /health - 健康检查
    this.addRoute('GET', '/health', (req, res) => {
      this.sendJSON(res, 200, {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
      });
    });
  }

  addRoute(method, path, handler) {
    const key = `${method}:${path}`;
    this.routes.set(key, handler);
  }

  handleRequest(req, res) {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const method = req.method;

    console.log(`📥 ${method} ${url.pathname}`);

    // 设置通用响应头
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Access-Control-Allow-Origin', '*');

    // 处理OPTIONS请求
    if (method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    // 路由匹配
    let matchedHandler = null;
    let routeParams = {};

    // 精确匹配
    const exactKey = `${method}:${url.pathname}`;
    if (this.routes.has(exactKey)) {
      matchedHandler = this.routes.get(exactKey);
    } else {
      // 参数化路由匹配（如 /api/users/123）
      for (const [routeKey, handler] of this.routes.entries()) {
        const [routeMethod, routePath] = routeKey.split(':');
        if (routeMethod === method && url.pathname.startsWith(routePath) && routePath.endsWith('/')) {
          const id = url.pathname.substring(routePath.length);
          if (id) {
            routeParams = { id };
            matchedHandler = handler;
            break;
          }
        }
      }
    }

    if (matchedHandler) {
      matchedHandler(req, res, routeParams);
    } else {
      this.sendJSON(res, 404, {
        error: '路由未找到',
        path: url.pathname,
        method: method
      });
    }
  }

  sendJSON(res, statusCode, data) {
    res.writeHead(statusCode);
    res.end(JSON.stringify(data, null, 2));
  }

  start() {
    this.server = http.createServer((req, res) => {
      this.handleRequest(req, res);
    });

    this.server.on('error', (error) => {
      console.error('❌ 服务器错误:', error.message);
    });

    this.server.listen(this.port, () => {
      console.log('✅ REST API服务器启动成功！');
      console.log(`🌐 访问地址: http://localhost:${this.port}`);
      console.log('\n可用的API端点:');
      console.log('  GET  /api/users     - 获取所有用户');
      console.log('  GET  /api/users/:id - 获取单个用户');
      console.log('  POST /api/users     - 创建新用户');
      console.log('  GET  /health        - 健康检查');
    });
  }

  stop() {
    if (this.server) {
      this.server.close();
      console.log('⏹️  服务器已停止');
    }
  }
}

// 启动服务器
const server = new APIServer(3000);
server.start();

// 优雅关闭
process.on('SIGINT', () => {
  console.log('\n👋 正在关闭服务器...');
  server.stop();
  process.exit(0);
});