#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: 容器编排模拟器
使用 Python 模拟容器隔离概念，展示进程隔离和资源限制的基本原理
"""

import subprocess
import threading
import time
import os
import signal
from typing import Dict, List, Optional
import json

class ContainerSimulator:
    """容器模拟器类"""

    def __init__(self):
        self.containers: Dict[str, subprocess.Popen] = {}
        self.container_info: Dict[str, dict] = {}

    def run_container(self, name: str, command: List[str],
                     env_vars: Optional[Dict[str, str]] = None,
                     working_dir: Optional[str] = None) -> bool:
        """
        运行一个模拟容器

        Args:
            name: 容器名称
            command: 要执行的命令列表
            env_vars: 环境变量字典
            working_dir: 工作目录
        """
        try:
            # 创建环境变量
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)

            # 启动子进程（模拟容器）
            process = subprocess.Popen(
                command,
                env=env,
                cwd=working_dir or os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # 创建新的进程组
            )

            # 记录容器信息
            self.containers[name] = process
            self.container_info[name] = {
                'pid': process.pid,
                'command': command,
                'status': 'running',
                'created_at': time.time(),
                'env_vars': env_vars or {},
                'working_dir': working_dir or os.getcwd()
            }

            print(f"容器 '{name}' 启动成功 (PID: {process.pid})")
            return True

        except Exception as e:
            print(f"启动容器 '{name}' 失败: {e}")
            return False

    def stop_container(self, name: str) -> bool:
        """停止指定容器"""
        if name not in self.containers:
            print(f"容器 '{name}' 不存在")
            return False

        try:
            process = self.containers[name]
            # 发送 SIGTERM 信号（优雅停止）
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

            # 等待进程结束（最多5秒）
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # 如果超时，强制杀死
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()

            # 更新状态
            self.container_info[name]['status'] = 'stopped'
            self.container_info[name]['stopped_at'] = time.time()

            del self.containers[name]
            print(f"容器 '{name}' 停止成功")
            return True

        except Exception as e:
            print(f"停止容器 '{name}' 失败: {e}")
            return False

    def list_containers(self) -> List[dict]:
        """列出所有容器"""
        containers_list = []

        # 更新运行中容器的状态
        for name, process in list(self.containers.items()):
            if process.poll() is not None:  # 进程已结束
                self.container_info[name]['status'] = 'exited'
                self.container_info[name]['exit_code'] = process.returncode
                del self.containers[name]

        # 收集所有容器信息
        for name, info in self.container_info.items():
            container_data = {
                'name': name,
                'status': info['status'],
                'pid': info.get('pid', 'N/A'),
                'command': ' '.join(info['command']),
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.localtime(info['created_at']))
            }
            containers_list.append(container_data)

        return containers_list

    def get_container_logs(self, name: str) -> str:
        """获取容器日志"""
        if name not in self.container_info:
            return f"容器 '{name}' 不存在"

        if name in self.containers:
            # 容器还在运行
            process = self.containers[name]
            stdout, stderr = process.communicate(timeout=1)
            return (stdout.decode() + stderr.decode()) if stdout or stderr else "无日志输出"
        else:
            # 容器已停止，返回最后的日志
            return "容器已停止，无法获取实时日志"

    def inspect_container(self, name: str) -> dict:
        """检查容器详细信息"""
        if name not in self.container_info:
            return {"error": f"容器 '{name}' 不存在"}

        return self.container_info[name]

def simulate_docker_commands():
    """模拟常见的 Docker 命令"""
    simulator = ContainerSimulator()

    print("=== 解决方案 2: 容器编排模拟器 ===\n")

    # 模拟 docker run
    print("1. 模拟 'docker run' - 启动 Web 服务器容器")
    simulator.run_container(
        "web-server",
        ["python3", "-m", "http.server", "8080"],
        env_vars={"APP_ENV": "development"},
        working_dir="/tmp"
    )

    time.sleep(2)  # 等待容器启动

    # 模拟 docker ps
    print("\n2. 模拟 'docker ps' - 列出运行中的容器")
    containers = simulator.list_containers()
    for container in containers:
        print(f"  {container['name']} | {container['status']} | {container['command']}")

    # 模拟 docker logs
    print("\n3. 模拟 'docker logs' - 查看容器日志")
    logs = simulator.get_container_logs("web-server")
    print(f"  Web 服务器日志: {logs[:100]}..." if len(logs) > 100 else f"  Web 服务器日志: {logs}")

    # 模拟 docker inspect
    print("\n4. 模拟 'docker inspect' - 检查容器详情")
    inspect_info = simulator.inspect_container("web-server")
    print(f"  PID: {inspect_info.get('pid')}")
    print(f"  状态: {inspect_info.get('status')}")
    print(f"  环境变量: {inspect_info.get('env_vars')}")

    # 模拟 docker stop
    print("\n5. 模拟 'docker stop' - 停止容器")
    simulator.stop_container("web-server")

    # 再次列出容器
    print("\n6. 再次列出所有容器（包括已停止的）")
    all_containers = simulator.list_containers()
    for container in all_containers:
        print(f"  {container['name']} | {container['status']} | {container['command']}")

    return simulator

def demonstrate_isolation_concept():
    """演示容器隔离概念"""
    print("\n=== 容器隔离概念演示 ===")
    print("在这个模拟器中，每个 '容器' 实际上是一个独立的子进程：")
    print("- 每个进程有自己的 PID（进程隔离）")
    print("- 可以设置独立的环境变量（环境隔离）")
    print("- 可以指定不同的工作目录（文件系统隔离）")
    print("- 进程组管理确保可以单独停止每个 '容器'")
    print("\n真实的 Docker 容器使用 Linux namespaces 和 cgroups 提供更强的隔离：")
    print("- Mount namespace: 文件系统隔离")
    print("- PID namespace: 进程隔离")
    print("- Network namespace: 网络隔离")
    print("- User namespace: 用户隔离")
    print("- Cgroups: 资源限制（CPU、内存等）")

def main():
    # 运行模拟器演示
    simulator = simulate_docker_commands()

    # 演示隔离概念
    demonstrate_isolation_concept()

if __name__ == "__main__":
    main()