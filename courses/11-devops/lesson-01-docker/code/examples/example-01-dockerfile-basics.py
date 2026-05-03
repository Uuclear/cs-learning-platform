#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: Dockerfile 基础生成器
这个脚本演示如何为 Flask 应用生成一个结构良好的 Dockerfile
并解释每个指令的作用。
"""

def generate_flask_dockerfile():
    """生成 Flask 应用的 Dockerfile"""
    dockerfile_content = """# 使用官方 Python 运行时作为基础镜像
# 使用 slim 版本减少镜像大小
FROM python:3.9-slim

# 设置工作目录，所有后续命令都在此目录下执行
WORKDIR /app

# 复制依赖文件到容器中
# 先复制 requirements.txt 可以利用 Docker 的层缓存机制
COPY requirements.txt .

# 安装应用依赖
# --no-cache-dir 参数避免缓存 pip 包，减小镜像大小
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用源代码到容器中
COPY . .

# 暴露应用端口（这只是文档作用，实际需要在运行时映射端口）
EXPOSE 5000

# 设置非 root 用户运行应用（安全最佳实践）
RUN useradd --create-home --shell /bin/bash app \\
 && chown -R app:app /app
USER app

# 容器启动时运行的命令
CMD ["python", "app.py"]
"""
    return dockerfile_content

def explain_dockerfile_instructions():
    """解释 Dockerfile 中的关键指令"""
    explanations = {
        "FROM": "指定基础镜像，所有 Dockerfile 都必须以 FROM 开始",
        "WORKDIR": "设置工作目录，相当于 cd 命令",
        "COPY": "将主机文件复制到容器中",
        "RUN": "在容器中执行命令，每个 RUN 创建一个新的镜像层",
        "EXPOSE": "声明容器监听的端口（文档作用，不影响实际端口映射）",
        "USER": "切换到指定用户运行后续命令（安全考虑）",
        "CMD": "容器启动时默认执行的命令"
    }
    return explanations

def main():
    print("=== 示例 1: Dockerfile 基础 ===\n")

    # 生成 Dockerfile
    dockerfile = generate_flask_dockerfile()
    print("生成的 Dockerfile 内容：")
    print("=" * 50)
    print(dockerfile)
    print("=" * 50)

    # 解释关键指令
    print("\n关键指令解释：")
    explanations = explain_dockerfile_instructions()
    for instruction, explanation in explanations.items():
        print(f"{instruction}: {explanation}")

    # 生成对应的 requirements.txt 示例
    requirements_content = """flask==2.0.3
redis==4.3.4
"""
    print(f"\n对应的 requirements.txt 示例：")
    print(requirements_content)

if __name__ == "__main__":
    main()