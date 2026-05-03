# 挑战 2: 设计多容器应用的docker-compose

## 难度：⭐⭐⭐

## 目标
为一个完整的 Web 应用栈设计 docker-compose.yml 文件，包含 Web 应用、数据库和缓存服务。

## 应用架构
你需要编排以下三个服务：

1. **Web 应用** (`web`)
   - 基于你之前创建的 Flask Dockerfile
   - 需要连接到 PostgreSQL 和 Redis
   - 监听端口 8000

2. **PostgreSQL 数据库** (`db`)
   - 使用官方 postgres:13-alpine 镜像
   - 需要持久化数据
   - 数据库名：myapp，用户名：user，密码：password

3. **Redis 缓存** (`redis`)
   - 使用官方 redis:6-alpine 镜像
   - 用于会话存储和缓存

## 要求

### 基本要求
1. 正确定义三个服务及其依赖关系
2. 配置适当的环境变量使服务能够互相通信
3. 为 PostgreSQL 配置数据卷以持久化数据
4. 映射 Web 应用端口到主机（8000:8000）

### 高级要求
1. 添加健康检查（healthcheck）确保服务正常运行
2. 配置重启策略（restart policy）
3. 使用自定义网络（可选，但推荐）
4. 为 Web 服务添加构建配置（从当前目录构建）

### 安全要求
1. 不要在 docker-compose.yml 中硬编码敏感信息（在实际项目中应使用 secrets 或环境文件）
2. 确保服务间通信仅在内部网络进行

## 提示
- Web 应用应该通过服务名称连接其他服务（如 `postgresql://user:password@db:5432/myapp`）
- 使用 `depends_on` 确保依赖服务先启动
- 考虑添加 `.env` 文件来管理环境变量

## 验证步骤
1. 创建 docker-compose.yml 文件
2. 运行：`docker-compose up --build`
3. 访问 `http://localhost:8000` 确认 Web 应用正常运行
4. 检查服务状态：`docker-compose ps`
5. 查看日志：`docker-compose logs -f`

## 扩展挑战
- 添加 Nginx 作为反向代理
- 配置 HTTPS（使用自签名证书）
- 添加监控服务（如 Prometheus + Grafana）
- 实现 CI/CD 流水线自动部署

这个挑战将帮助你理解如何在生产环境中编排复杂的多服务应用。加油！🚀