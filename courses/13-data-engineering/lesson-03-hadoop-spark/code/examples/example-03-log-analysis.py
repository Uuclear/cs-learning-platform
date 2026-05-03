#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: 日志分析管道模拟

这个脚本模拟了大数据日志处理管道，展示了如何使用类似 Spark 的操作
来处理大规模日志数据。实际生产环境中，这类任务通常在 Spark 或 Flink 上运行。
"""

from datetime import datetime, timedelta
import random
import json
from typing import List, Dict, Any, Tuple


class LogEntry:
    """日志条目类"""

    def __init__(self, timestamp: str, user_id: str, action: str,
                 page: str, ip_address: str, status_code: int):
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.page = page
        self.ip_address = ip_address
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'action': self.action,
            'page': self.page,
            'ip_address': self.ip_address,
            'status_code': self.status_code
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LogEntry':
        """从字典创建实例"""
        return cls(
            data['timestamp'],
            data['user_id'],
            data['action'],
            data['page'],
            data['ip_address'],
            data['status_code']
        )


def generate_sample_logs(num_logs: int = 1000) -> List[LogEntry]:
    """
    生成示例日志数据

    Args:
        num_logs: 要生成的日志数量

    Returns:
        LogEntry 对象列表
    """
    actions = ['view', 'click', 'search', 'purchase', 'login', 'logout']
    pages = ['/home', '/products', '/cart', '/checkout', '/profile', '/search']
    ip_prefixes = ['192.168.1.', '10.0.0.', '172.16.0.', '203.0.113.']

    logs = []
    base_time = datetime.now() - timedelta(hours=24)

    for i in range(num_logs):
        # 生成时间戳（过去24小时内）
        time_offset = random.randint(0, 86400)  # 24小时的秒数
        timestamp = (base_time + timedelta(seconds=time_offset)).isoformat()

        # 生成用户ID
        user_id = f"user_{random.randint(1000, 9999)}"

        # 随机选择动作和页面
        action = random.choice(actions)
        page = random.choice(pages)

        # 生成IP地址
        ip_address = f"{random.choice(ip_prefixes)}{random.randint(1, 254)}"

        # 生成状态码（大部分是200，少数是404或500）
        if random.random() < 0.95:
            status_code = 200
        elif random.random() < 0.8:
            status_code = 404
        else:
            status_code = 500

        log_entry = LogEntry(timestamp, user_id, action, page, ip_address, status_code)
        logs.append(log_entry)

    return logs


def parse_log_line(log_line: str) -> LogEntry:
    """
    解析单行日志（JSON格式）

    Args:
        log_line: JSON格式的日志字符串

    Returns:
        LogEntry 对象
    """
    data = json.loads(log_line)
    return LogEntry.from_dict(data)


def filter_by_status_code(logs: List[LogEntry], status_code: int) -> List[LogEntry]:
    """
    过滤指定状态码的日志

    Args:
        logs: 日志列表
        status_code: 状态码

    Returns:
        过滤后的日志列表
    """
    return [log for log in logs if log.status_code == status_code]


def group_by_action(logs: List[LogEntry]) -> Dict[str, int]:
    """
    按动作分组统计

    Args:
        logs: 日志列表

    Returns:
        动作计数字典
    """
    action_counts = {}
    for log in logs:
        action_counts[log.action] = action_counts.get(log.action, 0) + 1
    return action_counts


def find_top_pages(logs: List[LogEntry], top_n: int = 5) -> List[Tuple[str, int]]:
    """
    找出访问量最高的页面

    Args:
        logs: 日志列表
        top_n: 返回前N个页面

    Returns:
        页面和访问次数的元组列表
    """
    page_counts = {}
    for log in logs:
        page_counts[log.page] = page_counts.get(log.page, 0) + 1

    sorted_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_pages[:top_n]


def calculate_error_rate(logs: List[LogEntry]) -> float:
    """
    计算错误率（非200状态码的比例）

    Args:
        logs: 日志列表

    Returns:
        错误率（0-1之间的浮点数）
    """
    total_logs = len(logs)
    if total_logs == 0:
        return 0.0

    error_logs = sum(1 for log in logs if log.status_code != 200)
    return error_logs / total_logs


def simulate_log_processing_pipeline():
    """
    模拟完整的日志处理管道
    """
    print("=== 大数据日志分析管道模拟 ===")

    # Step 1: 生成示例日志数据
    print("1. 生成示例日志数据...")
    raw_logs = generate_sample_logs(1000)
    print(f"   生成了 {len(raw_logs)} 条日志记录")

    # Step 2: 数据清洗和过滤
    print("2. 数据清洗和过滤...")
    valid_logs = [log for log in raw_logs if log.status_code in [200, 404, 500]]
    print(f"   清洗后剩余 {len(valid_logs)} 条有效日志")

    # Step 3: 分析用户行为
    print("3. 分析用户行为...")
    action_stats = group_by_action(valid_logs)
    print("   用户行为统计:")
    for action, count in sorted(action_stats.items()):
        print(f"     {action}: {count} 次")

    # Step 4: 页面访问分析
    print("4. 页面访问分析...")
    top_pages = find_top_pages(valid_logs, 3)
    print("   访问量最高的页面:")
    for page, count in top_pages:
        print(f"     {page}: {count} 次访问")

    # Step 5: 错误分析
    print("5. 错误分析...")
    error_rate = calculate_error_rate(valid_logs)
    print(f"   总体错误率: {error_rate:.2%}")

    # Step 6: 错误日志详情
    error_logs = filter_by_status_code(valid_logs, 404) + filter_by_status_code(valid_logs, 500)
    print(f"   错误日志数量: {len(error_logs)}")
    if error_logs:
        print("   前3个错误日志:")
        for i, log in enumerate(error_logs[:3]):
            print(f"     [{i+1}] {log.page} - {log.status_code}")

    return {
        'total_logs': len(valid_logs),
        'action_stats': action_stats,
        'top_pages': top_pages,
        'error_rate': error_rate,
        'error_count': len(error_logs)
    }


def main():
    """主函数"""
    results = simulate_log_processing_pipeline()

    print("\n=== 处理结果摘要 ===")
    print(f"总日志数: {results['total_logs']}")
    print(f"错误率: {results['error_rate']:.2%}")
    print(f"错误日志数: {results['error_count']}")


if __name__ == "__main__":
    main()