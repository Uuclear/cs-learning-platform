#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 简单的端口扫描器

检测指定主机的常用端口是否开放。
"""

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# 常用端口列表
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    993: "IMAPS"
}

def check_port(host, port, timeout=3):
    """
    检查指定主机的端口是否开放

    Args:
        host: 主机地址
        port: 端口号
        timeout: 超时时间（秒）

    Returns:
        tuple: (port, is_open, service_name)
    """
    try:
        # 创建socket并设置超时
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # 尝试连接
        result = sock.connect_ex((host, port))
        is_open = (result == 0)

        sock.close()
        service_name = COMMON_PORTS.get(port, "未知服务")
        return port, is_open, service_name

    except Exception as e:
        return port, False, f"错误: {e}"

def scan_ports(host, ports=None, max_workers=10):
    """
    扫描多个端口

    Args:
        host: 目标主机
        ports: 要扫描的端口列表，默认为COMMON_PORTS的键
        max_workers: 最大并发线程数
    """
    if ports is None:
        ports = list(COMMON_PORTS.keys())

    print(f"开始扫描主机: {host}")
    print(f"扫描端口: {ports}")
    print("-" * 50)

    open_ports = []

    # 使用线程池并发扫描
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有扫描任务
        future_to_port = {
            executor.submit(check_port, host, port): port
            for port in ports
        }

        # 收集结果
        results = []
        for future in future_to_port:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                port = future_to_port[future]
                results.append((port, False, f"异常: {e}"))

    # 按端口号排序并显示结果
    results.sort(key=lambda x: x[0])
    for port, is_open, service_name in results:
        status = "开放" if is_open else "关闭"
        print(f"端口 {port:3d} ({service_name:8s}): {status}")
        if is_open:
            open_ports.append(port)

    print("-" * 50)
    print(f"扫描完成！共发现 {len(open_ports)} 个开放端口: {open_ports}")

def main():
    # 默认扫描本地主机
    target_host = "localhost"

    # 如果提供了命令行参数，则使用该参数作为目标主机
    import sys
    if len(sys.argv) > 1:
        target_host = sys.argv[1]

    scan_ports(target_host)

if __name__ == "__main__":
    main()