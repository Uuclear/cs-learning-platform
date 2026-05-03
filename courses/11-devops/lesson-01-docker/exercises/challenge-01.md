# 挑战 1: 为Python Web应用编写Dockerfile

## 难度：⭐⭐

## 目标
为一个简单的 Python Web 应用创建一个优化的 Dockerfile。

## 应用描述
你有一个使用 Flask 框架的简单 Web 应用，包含以下文件：

- `app.py` - 主应用文件
- `requirements.txt` - 依赖文件
- `static/` - 静态文件目录
- `templates/` - 模板文件目录

## 要求

### 基本要求
1. 使用合适的 Python 基础镜像（考虑大小和安全性）
2. 正确设置工作目录
3. 复制依赖文件并安装依赖
4. 复制应用源代码
5. 暴露正确的端口（8000）
6. 使用非 root 用户运行应用

### 优化要求
1. 利用 Docker 层缓存机制（先复制 requirements.txt）
2. 清理 pip 缓存以减小镜像大小
3. 使用 .dockerignore 文件排除不必要的文件（如 __pycache__, .git, etc.）

## 提示
- 考虑使用 `python:3.9-slim` 或 `python:3.9-alpine` 作为基础镜像
- 使用 `--no-cache-dir` 参数安装 pip 包
- 创建专门的应用用户（如 `app`）来运行应用

## 验证步骤
1. 构建镜像：`docker build -t my-flask-app .`
2. 运行容器：`docker run -p 8000:8000 my-flask-app`
3. 访问 `http://localhost:8000` 确认应用正常运行
4. 检查镜像大小：`docker images | grep my-flask-app`

## 扩展思考
- 如何进一步优化这个 Dockerfile？
- 如果应用需要编译 C 扩展，应该如何调整？
- 如何处理应用配置（如数据库连接字符串）？

祝你好运！🎯