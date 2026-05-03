#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: Docker Compose 演示
这个脚本生成一个完整的 docker-compose.yml 文件，
用于编排 Web 应用、数据库和缓存服务。
"""

def generate_docker_compose():
    """生成 docker-compose.yml 文件内容"""
    return """version: '3.8'

services:
  # Web 应用服务
  web:
    # 使用当前目录的 Dockerfile 构建
    build:
      context: .
      dockerfile: Dockerfile
    # 映射端口：主机端口:容器端口
    ports:
      - "8000:8000"
    # 环境变量
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
    # 依赖的服务，确保这些服务先启动
    depends_on:
      - db
      - redis
    # 重启策略
    restart: unless-stopped
    # 健康检查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL 数据库服务
  db:
    # 使用官方 PostgreSQL 镜像
    image: postgres:13-alpine
    # 环境变量配置
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    # 数据卷挂载，持久化数据
    volumes:
      - postgres_data:/var/lib/postgresql/data
    # 重启策略
    restart: unless-stopped
    # 健康检查
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis 缓存服务
  redis:
    # 使用官方 Redis 镜像
    image: redis:6-alpine
    # 端口映射（可选，如果只在内部网络使用可以不映射）
    ports:
      - "6379:6379"
    # 重启策略
    restart: unless-stopped
    # 健康检查
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 可选：Nginx 反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    restart: unless-stopped

# 定义数据卷
volumes:
  postgres_data:
"""

def explain_compose_concepts():
    """解释 docker-compose.yml 中的关键概念"""
    concepts = {
        "version": "指定 Compose 文件格式版本",
        "services": "定义要运行的服务",
        "build": "从 Dockerfile 构建镜像",
        "image": "使用预构建的镜像",
        "ports": "端口映射（主机:容器）",
        "environment": "设置环境变量",
        "depends_on": "服务依赖关系",
        "volumes": "数据卷挂载",
        "restart": "容器重启策略",
        "healthcheck": "健康检查配置"
    }
    return concepts

def generate_usage_commands():
    """生成常用的 docker-compose 命令"""
    commands = [
        "docker-compose up --build          # 构建并启动所有服务",
        "docker-compose down                # 停止并删除所有容器",
        "docker-compose logs -f web         # 查看 web 服务日志",
        "docker-compose exec db psql -U user myapp  # 进入数据库",
        "docker-compose ps                  # 查看服务状态"
    ]
    return commands

def main():
    print("=== 示例 3: Docker Compose 演示 ===\n")

    # 生成 docker-compose.yml
    compose_content = generate_docker_compose()
    print("生成的 docker-compose.yml 内容：")
    print("=" * 60)
    print(compose_content)
    print("=" * 60)

    # 解释关键概念
    print("\n关键概念解释：")
    concepts = explain_compose_concepts()
    for concept, explanation in concepts.items():
        print(f"{concept}: {explanation}")

    # 显示常用命令
    print(f"\n常用 docker-compose 命令：")
    commands = generate_usage_commands()
    for command in commands:
        print(f"  {command}")

    # 说明架构优势
    advantages = [
        "一键启动整个应用栈",
        "服务间自动网络连接",
        "统一的日志管理和监控",
        "简化开发和测试环境搭建",
        "与生产环境配置保持一致"
    ]

    print(f"\nDocker Compose 的优势：")
    for i, advantage in enumerate(advantages, 1):
        print(f"{i}. {advantage}")

if __name__ == "__main__":
    main()