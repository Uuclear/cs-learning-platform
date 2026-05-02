#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 简单进程管理器

实现一个简单的进程管理器，能够列出所有进程、根据名称查找进程、终止指定进程。
"""

import psutil
import sys

class SimpleProcessManager:
    """简单的进程管理器类"""

    def __init__(self):
        self.processes = []

    def list_all_processes(self):
        """列出所有进程"""
        print("\n=== 所有进程列表 ===")
        print(f"{'PID':<8} {'名称':<20} {'状态':<10} {'内存(MB)':<10}")
        print("-" * 50)

        try:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name'][:18] + ".." if len(proc.info['name']) > 20 else proc.info['name']
                    status = proc.info['status']
                    memory_mb = proc.info['memory_info'].rss / 1024 / 1024 if proc.info['memory_info'] else 0

                    print(f"{pid:<8} {name:<20} {status:<10} {memory_mb:<10.2f}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # 跳过已终止或无权限的进程
                    continue
        except psutil.AccessDenied:
            print("错误: 无权限访问进程信息")

    def find_processes_by_name(self, name):
        """根据名称查找进程"""
        print(f"\n=== 查找进程: {name} ===")
        found = False

        try:
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    if name.lower() in proc.info['name'].lower():
                        print(f"PID: {proc.info['pid']}, 名称: {proc.info['name']}, 状态: {proc.info['status']}")
                        found = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if not found:
                print(f"未找到包含 '{name}' 的进程")
        except psutil.AccessDenied:
            print("错误: 无权限访问进程信息")

    def terminate_process(self, pid):
        """终止指定PID的进程"""
        try:
            process = psutil.Process(pid)
            print(f"准备终止进程: PID {pid}, 名称: {process.name()}")

            # 确认操作
            confirm = input("确定要终止此进程吗? (y/N): ")
            if confirm.lower() == 'y':
                process.terminate()  # 发送SIGTERM信号
                print(f"已发送终止信号给进程 {pid}")

                # 等待进程终止（最多3秒）
                try:
                    process.wait(timeout=3)
                    print("进程已成功终止")
                except psutil.TimeoutExpired:
                    print("进程未在3秒内终止，可能需要强制终止")
                    force = input("是否强制终止? (y/N): ")
                    if force.lower() == 'y':
                        process.kill()  # 发送SIGKILL信号
                        print("进程已被强制终止")
            else:
                print("操作已取消")

        except psutil.NoSuchProcess:
            print(f"错误: 进程 PID {pid} 不存在")
        except psutil.AccessDenied:
            print(f"错误: 无权限终止进程 PID {pid}")
        except Exception as e:
            print(f"错误: {e}")

    def show_menu(self):
        """显示菜单"""
        print("\n=== 简单进程管理器 ===")
        print("1. 列出所有进程")
        print("2. 按名称查找进程")
        print("3. 终止进程")
        print("4. 退出")
        return input("请选择操作 (1-4): ")

    def run(self):
        """运行主循环"""
        while True:
            try:
                choice = self.show_menu()

                if choice == '1':
                    self.list_all_processes()
                elif choice == '2':
                    name = input("请输入进程名称: ")
                    self.find_processes_by_name(name)
                elif choice == '3':
                    try:
                        pid = int(input("请输入要终止的进程PID: "))
                        self.terminate_process(pid)
                    except ValueError:
                        print("错误: PID必须是数字")
                elif choice == '4':
                    print("再见！")
                    break
                else:
                    print("无效选择，请输入1-4")

            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                print(f"发生错误: {e}")

def main():
    """主函数"""
    manager = SimpleProcessManager()
    manager.run()

if __name__ == "__main__":
    main()