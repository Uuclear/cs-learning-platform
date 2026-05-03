# 挑战 1：为微服务应用编写 Kubernetes Manifests

## 难度：⭐⭐⭐⭐

### 背景
你正在开发一个现代化的微服务应用，包含以下组件：
- **Frontend**: React 前端应用，监听端口 3000
- **Backend API**: Node.js 后端服务，监听端口 8080
- **Database**: PostgreSQL 数据库，监听端口 5432
- **Cache**: Redis 缓存服务，监听端口 6379

### 要求

#### 1. 基础要求
- 为每个服务创建独立的 Deployment
- 为每个服务创建对应的 Service
- 使用 ConfigMap 管理非敏感配置
- 使用 Secret 管理数据库密码和 API 密钥
- 设置合理的资源请求和限制
- 配置适当的健康检查探针

#### 2. 高级要求
- 为 Frontend 和 Backend 创建 Ingress 规则
  - `frontend.example.com` → Frontend Service
  - `api.example.com` → Backend Service
- 实现数据库初始化脚本（使用 Init Container）
- 配置持久化存储给数据库（使用 PersistentVolumeClaim）
- 设置合适的部署策略（滚动更新）

#### 3. 安全要求
- 限制容器权限（使用 securityContext）
- 不使用 root 用户运行容器
- 设置网络策略（NetworkPolicy）限制服务间通信
- 数据库 Secret 必须使用 stringData 或正确编码

### 提交内容
创建一个完整的 YAML 文件，包含所有必需的 Kubernetes 资源。文件应该能够直接应用到集群中（假设已安装 Ingress Controller）。

### 评估标准
- ✅ 功能完整性（所有组件正常工作）
- ✅ 最佳实践遵循（资源管理、安全配置）
- ✅ 配置组织（合理使用标签、命名空间）
- ✅ 可维护性（清晰的注释和结构）

### 提示
- 使用 `kubectl explain` 命令查看资源字段说明
- 参考官方文档中的最佳实践
- 考虑使用 kustomize 或 helm 进行更复杂的配置管理（可选）

---

**记住：在生产环境中，永远不要使用 `latest` 标签，始终使用明确的版本号！**