#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 进程创建

演示如何使用os.fork()创建子进程，展示父子进程的关系。
注意：此代码仅在Unix/Linux/macOS系统上运行，在Windows上需要使用其他方法。
"""

import os
import time

def main():
    """主函数：演示进程创建"""
    # 获取并打印父进程的PID
    print(f"父进程PID: {os.getpid()}")

    # 创建子进程 - fork()会返回两次：
    # 在父进程中返回子进程的PID（正数）
    # 在子进程中返回0
    pid = os.fork()

    if pid == 0:
        # 这是子进程的代码路径
        print(f"子进程PID: {os.getpid()}, 父进程PID: {os.getppid()}")
        # 子进程执行一些工作
        time.sleep(2)
        print("子进程结束")
    else:
        # 这是父进程的代码路径
        print(f"父进程创建了子进程，子进程PID: {pid}")
        # 父进程等待一段时间
        time.sleep(3)
        print("父进程结束")

if __name__ == "__main__":
    main()