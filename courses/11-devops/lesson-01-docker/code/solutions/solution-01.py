#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: Dockerfile 生成器
根据应用需求创建优化的 Dockerfile
"""

import os
from typing import List, Optional

class DockerfileGenerator:
    """Dockerfile 生成器类"""

    def __init__(self, app_type: str = "python", base_image: Optional[str] = None):
        self.app_type = app_type.lower()
        self.base_image = base_image or self._get_default_base_image()
        self.instructions = []

    def _get_default_base_image(self) -> str:
        """根据应用类型获取默认基础镜像"""
        base_images = {
            "python": "python:3.9-slim",
            "node": "node:16-alpine",
            "go": "golang:1.19-alpine",
            "java": "openjdk:11-jre-slim"
        }
        return base_images.get(self.app_type, "alpine:latest")

    def add_workdir(self, workdir: str = "/app"):
        """添加工作目录指令"""
        self.instructions.append(f"WORKDIR {workdir}")
        return self

    def add_copy_dependencies(self, deps_file: str):
        """添加复制依赖文件指令"""
        self.instructions.append(f"COPY {deps_file} .")
        return self

    def add_install_dependencies(self, install_cmd: Optional[str] = None):
        """添加安装依赖指令"""
        if install_cmd is None:
            install_commands = {
                "python": "pip install --no-cache-dir -r requirements.txt",
                "node": "npm ci --only=production",
                "go": "go mod download",
                "java": "mvn dependency:resolve"
            }
            install_cmd = install_commands.get(self.app_type, "echo 'No install command defined'")

        self.instructions.append(f"RUN {install_cmd}")
        return self

    def add_copy_source(self, source: str = ".", dest: str = "."):
        """添加复制源代码指令"""
        self.instructions.append(f"COPY {source} {dest}")
        return self

    def add_expose_port(self, port: int):
        """添加暴露端口指令"""
        self.instructions.append(f"EXPOSE {port}")
        return self

    def add_non_root_user(self, username: str = "app"):
        """添加非 root 用户指令（安全最佳实践）"""
        if "alpine" in self.base_image:
            user_cmd = f"addgroup -g 1001 -S {username} && adduser -S {username} -u 1001 -G {username}"
        else:
            user_cmd = f"useradd --create-home --shell /bin/bash {username} && chown -R {username}:{username} /app"

        self.instructions.append(f"RUN {user_cmd}")
        self.instructions.append(f"USER {username}")
        return self

    def add_cmd(self, cmd: List[str]):
        """添加 CMD 指令"""
        cmd_str = ", ".join([f'"{c}"' for c in cmd])
        self.instructions.append(f"CMD [{cmd_str}]")
        return self

    def generate(self) -> str:
        """生成完整的 Dockerfile 内容"""
        dockerfile_lines = [f"FROM {self.base_image}"]
        dockerfile_lines.extend(self.instructions)
        return "\n".join(dockerfile_lines)

def create_python_flask_dockerfile():
    """创建 Python Flask 应用的优化 Dockerfile"""
    generator = DockerfileGenerator("python", "python:3.9-slim")
    dockerfile = (generator
                  .add_workdir("/app")
                  .add_copy_dependencies("requirements.txt")
                  .add_install_dependencies()
                  .add_copy_source()
                  .add_expose_port(5000)
                  .add_non_root_user("app")
                  .add_cmd(["python", "app.py"])
                  .generate())
    return dockerfile

def create_nodejs_dockerfile():
    """创建 Node.js 应用的优化 Dockerfile"""
    generator = DockerfileGenerator("node", "node:16-alpine")
    dockerfile = (generator
                  .add_workdir("/app")
                  .add_copy_dependencies("package*.json")
                  .add_install_dependencies()
                  .add_copy_source()
                  .add_expose_port(3000)
                  .add_non_root_user("app")
                  .add_cmd(["node", "server.js"])
                  .generate())
    return dockerfile

def main():
    print("=== 解决方案 1: Dockerfile 生成器 ===\n")

    # 生成 Python Flask Dockerfile
    print("Python Flask 应用的优化 Dockerfile：")
    print("-" * 50)
    print(create_python_flask_dockerfile())
    print("-" * 50)

    print("\nNode.js 应用的优化 Dockerfile：")
    print("-" * 50)
    print(create_nodejs_dockerfile())
    print("-" * 50)

    # 演示自定义生成器
    print("\n自定义 Go 应用 Dockerfile：")
    print("-" * 50)
    go_generator = DockerfileGenerator("go", "golang:1.19-alpine")
    go_dockerfile = (go_generator
                     .add_workdir("/app")
                     .add_copy_source()
                     .add_cmd(["go", "run", "main.go"])
                     .generate())
    print(go_dockerfile)
    print("-" * 50)

if __name__ == "__main__":
    main()