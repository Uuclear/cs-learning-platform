# 编程挑战1: 多线程Web服务器

## 难度：⭐⭐

### 背景
在示例2中，我们实现了一个简单的单线程TCP服务器，它只能处理一个客户端连接。在实际应用中，服务器需要同时处理多个客户端请求。

### 任务
扩展示例2的代码，实现一个多线程的Web服务器，能够：
1. 同时处理多个客户端连接
2. 支持基本的HTTP GET请求
3. 返回简单的HTML页面或JSON响应

### 要求
- 使用Python的`threading`模块实现并发处理
- 服务器应该监听8080端口
- 对于根路径`/`，返回一个包含"Hello, World!"的HTML页面
- 对于`/api/hello`路径，返回JSON格式的响应：`{"message": "Hello, World!"}`
- 对于其他路径，返回404错误页面
- 每个客户端连接都应该在独立的线程中处理
- 正确处理异常和资源清理

### 提示
- 可以参考示例2的TCP服务器代码作为基础
- HTTP响应格式：状态行 + 响应头 + 空行 + 响应体
- 记得设置正确的Content-Type头部（text/html 或 application/json）
- 使用try-finally确保socket被正确关闭

### 测试方法
```bash
# 启动服务器
python challenge-01-solution.py

# 在另一个终端测试
curl http://localhost:8080/
curl http://localhost:8080/api/hello
curl http://localhost:8080/nonexistent
```