#!/usr/bin/env bash
# deploy.sh — 一键部署脚本
# 用法: ./deploy.sh
# 功能: 安装依赖 -> 构建 -> 可选启动生产服务器

set -e

PLATFORM_DIR="$(cd "$(dirname "$0")/platform" && pwd)"
cd "$PLATFORM_DIR"

echo "========================================="
echo "  CS 知识学习平台 - 部署脚本"
echo "========================================="

# 1. 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js >= 18"
    echo "  https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | sed 's/v//;s/\..*//')
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "错误: Node.js 版本过低 (需要 >= 18)，当前版本: $(node -v)"
    exit 1
fi
echo "✓ Node.js $(node -v) 已就绪"

# 2. 安装依赖
if [ ! -d "node_modules" ]; then
    echo "→ 安装依赖..."
    npm install
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已存在"
fi

# 3. 构建
echo "→ 构建生产版本..."
npm run build
echo "✓ 构建完成"

# 4. 启动提示
echo ""
echo "========================================="
echo "  构建成功！"
echo "========================================="
echo ""
echo "启动生产服务器:"
echo "  cd platform && npm run start"
echo ""
echo "本地开发:"
echo "  cd platform && npm run dev"
echo ""

# 5. 询问是否启动生产服务器
read -p "是否立即启动生产服务器? (y/N): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    npm run start
fi
