#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: 多阶段构建演示
这个脚本展示多阶段构建的概念，通过比较构建前后的 Dockerfile 大小
来说明多阶段构建的优势。
"""

def generate_single_stage_dockerfile():
    """生成单阶段构建的 Dockerfile（较大）"""
    return """# 单阶段构建 - 包含所有构建工具和依赖
FROM node:16

# 安装构建工具
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    git \\
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装所有依赖（包括 devDependencies）
RUN npm install

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 运行应用
CMD ["node", "dist/server.js"]
"""

def generate_multi_stage_dockerfile():
    """生成多阶段构建的 Dockerfile（较小）"""
    return """# 第一阶段：构建阶段
FROM node:16 as builder

# 安装构建工具
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    git \\
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装所有依赖（包括开发依赖）
RUN npm install

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 第二阶段：运行阶段
FROM node:16-alpine

# 创建应用用户
RUN addgroup -g 1001 -S nodejs \\
 && adduser -S app -u 1001 -G nodejs

WORKDIR /app

# 从构建阶段复制生产依赖和构建产物
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# 切换到非 root 用户
USER app

# 运行应用
CMD ["node", "dist/server.js"]
"""

def estimate_image_sizes():
    """估算镜像大小（基于基础镜像大小）"""
    # 这些是近似值，实际大小会因具体依赖而异
    single_stage_size = {
        "base_image": "900MB",  # node:16
        "build_tools": "200MB",
        "dev_dependencies": "300MB",
        "source_code": "50MB",
        "total_estimated": "1450MB"
    }

    multi_stage_size = {
        "base_image": "117MB",  # node:16-alpine
        "production_deps": "150MB",
        "build_artifacts": "30MB",
        "total_estimated": "297MB"
    }

    return single_stage_size, multi_stage_size

def main():
    print("=== 示例 2: 多阶段构建演示 ===\n")

    # 显示单阶段构建 Dockerfile
    print("单阶段构建 Dockerfile（较大）：")
    print("-" * 60)
    print(generate_single_stage_dockerfile())
    print("-" * 60)

    # 显示多阶段构建 Dockerfile
    print("\n多阶段构建 Dockerfile（较小）：")
    print("-" * 60)
    print(generate_multi_stage_dockerfile())
    print("-" * 60)

    # 比较镜像大小
    single_size, multi_size = estimate_image_sizes()
    print(f"\n镜像大小对比：")
    print(f"单阶段构建: ~{single_size['total_estimated']}")
    print(f"多阶段构建: ~{multi_size['total_estimated']}")
    print(f"节省空间: ~{int(single_size['total_estimated'].replace('MB', '')) - int(multi_size['total_estimated'].replace('MB', ''))}MB")
    print(f"减少比例: ~{(1 - int(multi_size['total_estimated'].replace('MB', '')) / int(single_size['total_estimated'].replace('MB', ''))) * 100:.1f}%")

    # 解释多阶段构建的优势
    advantages = [
        "显著减小最终镜像大小",
        "提高安全性（不包含构建工具和开发依赖）",
        "加快镜像传输和部署速度",
        "减少攻击面（更少的软件包意味着更少的漏洞）"
    ]

    print(f"\n多阶段构建的优势：")
    for i, advantage in enumerate(advantages, 1):
        print(f"{i}. {advantage}")

if __name__ == "__main__":
    main()