#!/usr/bin/env bash
# deploy.sh — 一键部署脚本
# 用法:
#   ./deploy.sh              # 构建 Node.js 生产版本
#   ./deploy.sh --vercel     # 部署到 Vercel
#   ./deploy.sh --gh-pages   # 构建静态站点并推送到 gh-pages 分支

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLATFORM_DIR="$ROOT_DIR/platform"

cd "$PLATFORM_DIR"

echo "========================================="
echo "  CS 知识学习平台 - 部署脚本"
echo "========================================="

# 检查 Node.js
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

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "→ 安装依赖..."
    npm install
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已存在"
fi

# 解析参数
DEPLOY_MODE=""
case "${1:-}" in
    --vercel)
        DEPLOY_MODE="vercel"
        ;;
    --gh-pages)
        DEPLOY_MODE="gh-pages"
        ;;
    *)
        DEPLOY_MODE="node"
        ;;
esac

# 3. 构建 + 部署
case "$DEPLOY_MODE" in
    vercel)
        echo ""
        echo "→ 部署到 Vercel..."
        cd "$ROOT_DIR"
        if command -v vercel &> /dev/null; then
            vercel --prod
        else
            echo "错误: 未安装 Vercel CLI"
            echo "  运行: npm i -g vercel"
            echo "  或访问 https://vercel.com 导入项目"
            exit 1
        fi
        ;;

    gh-pages)
        echo ""
        echo "→ 构建静态站点 (GitHub Pages)..."
        export NEXT_PUBLIC_STATIC_EXPORT=true

        # 替换 API 路由为静态存根 (GitHub Pages 不支持 API 路由)
        echo "→ 替换 API 路由为静态版本..."
        mv "$PLATFORM_DIR/app/api/search/route.ts" "$PLATFORM_DIR/app/api/search/route.ts.bak"
        cat > "$PLATFORM_DIR/app/api/search/route.ts" << 'STATICROUTE'
import { NextResponse } from "next/server";
export const dynamic = "force-static";
export async function GET() {
  return NextResponse.json({ results: [] });
}
STATICROUTE

        # 构建搜索索引
        node "$PLATFORM_DIR/scripts/build-search-index.js"

        # 静态导出
        cd "$PLATFORM_DIR" && npx next build

        # 恢复原始 API 路由
        echo "→ 恢复 API 路由..."
        mv "$PLATFORM_DIR/app/api/search/route.ts.bak" "$PLATFORM_DIR/app/api/search/route.ts"

        echo "✓ 静态站点已生成到 out/"

        # 推送
        echo ""
        echo "→ 推送到 gh-pages 分支..."
        if npm ls gh-pages --depth=0 2>/dev/null | grep -q gh-pages; then
            npx gh-pages -d out -b gh-pages
        else
            echo "→ 安装 gh-pages..."
            npm install --save-dev gh-pages
            npx gh-pages -d out -b gh-pages
        fi

        echo ""
        echo "========================================="
        echo "  部署完成！"
        echo "========================================="
        echo ""
        echo "在 GitHub 仓库设置中启用 GitHub Pages:"
        echo "  Settings → Pages → Source: Deploy from actions"
        echo "  或手动推送 gh-pages 分支后选择: gh-pages branch"
        echo ""
        ;;

    *)
        # 默认 Node.js 构建
        echo "→ 构建生产版本..."
        npm run build
        echo "✓ 构建完成"

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
        echo "部署到 GitHub Pages:"
        echo "  ./deploy.sh --gh-pages"
        echo ""

        read -p "是否立即启动生产服务器? (y/N): " -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            npm run start
        fi
        ;;
esac
