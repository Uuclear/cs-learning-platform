#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 进程状态监控

监控指定PID的进程状态变化，并在状态改变时输出通知。
"""

import sys
import time
import psutil

def monitor_process_state(pid):
    """
    监控指定PID的进程状态

    参数:
        pid: 要监控的进程ID
    """
    try:
        # 获取进程对象
        process = psutil.Process(pid)
        print(f"开始监控进程 PID {pid} ({process.name()})")

        # 获取初始状态
        last_status = process.status()
        print(f"初始状态: {last_status}")

        # 持续监控状态变化
        while True:
            try:
                current_status = process.status()
                if current_status != last_status:
                    print(f"[{time.strftime('%H:%M:%S')}] 状态变化: {last_status} -> {current_status}")
                    last_status = current_status

                # 检查进程是否还存在
                if not process.is_running():
                    print(f"进程 {pid} 已终止")
                    break

                time.sleep(1)  # 每秒检查一次

            except psutil.NoSuchProcess:
                print(f"进程 {pid} 已不存在")
                break

    except psutil.NoSuchProcess:
        print(f"错误: 进程 PID {pid} 不存在")
    except psutil.AccessDenied:
        print(f"错误: 无权限访问进程 PID {pid}")
    except KeyboardInterrupt:
        print("\n监控已停止")

def main():
    """主函数：处理命令行参数"""
    if len(sys.argv) != 2:
        print("用法: python solution-02.py <PID>")
        print("示例: python solution-02.py 1234")
        return

    try:
        pid = int(sys.argv[1])
        monitor_process_state(pid)
    except ValueError:
        print("错误: PID必须是数字")

if __name__ == "__main__":
    main()