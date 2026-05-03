# 编程挑战 2：RESTful API服务器

## 目标
创建一个简单的RESTful API服务器，能够管理用户数据并提供基本的CRUD操作。

## 要求

### 1. 服务器基础
- 使用 Node.js 的 `http` 模块创建HTTP服务器
- 服务器应该监听端口 3000
- 支持 CORS（跨域资源共享）

### 2. 路由设计
实现以下API端点：

#### GET /api/users
- 返回所有用户的JSON数组
- 每个用户对象包含：id, name, email, createdAt

#### GET /api/users/:id  
- 根据ID返回单个用户
- 如果用户不存在，返回404错误

#### POST /api/users
- 接收JSON格式的用户数据（name, email）
- 生成新的用户ID（可以使用时间戳）
- 添加createdAt字段
- 返回创建成功的响应和新用户数据

#### GET /health
- 返回服务器健康状态
- 包含状态、时间戳和运行时间信息

### 3. 数据存储
- 使用内存数组存储用户数据（不需要持久化到文件）
- 初始包含2-3个示例用户

### 4. 错误处理
- 处理无效的JSON数据
- 处理不存在的路由（404）
- 处理不支持的HTTP方法（405）

### 5. 响应格式
- 所有成功响应使用200状态码（POST创建使用201）
- 所有响应都应该是JSON格式
- 包含适当的Content-Type头

### 6. 额外功能
- 记录每个请求的日志（方法、路径、时间）
- 支持优雅关闭（监听SIGINT信号）

## 提示
- 使用 URL 类解析请求路径
- 使用 EventEmitter 模式组织代码
- 考虑使用类来封装服务器逻辑
- 确保代码有适当的中文注释

## 验证
你的服务器应该能够通过以下测试：

```bash
# 获取所有用户
curl http://localhost:3000/api/users

# 获取单个用户  
curl http://localhost:3000/api/users/1

# 创建新用户
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"新用户","email":"new@example.com"}'

# 健康检查
curl http://localhost:3000/health

# 测试404
curl http://localhost:3000/nonexistent
```

预期输出应该包含正确的JSON数据和HTTP状态码。