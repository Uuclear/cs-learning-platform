#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: 日志分析管道

这是 example-03-log-analysis.py 的完整解决方案，
包含了更健壮的日志处理和分析功能。
"""

from datetime import datetime, timedelta
import random
import json
from typing import List, Dict, Any, Tuple, Optional


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
        return cls(
            str(data.get('timestamp', '')),
            str(data.get('user_id', '')),
            str(data.get('action', '')),
            str(data.get('page', '')),
            str(data.get('ip_address', '')),
            int(data.get('status_code', 200))
        )

    def is_error(self) -> bool:
        """检查是否为错误日志"""
        return self.status_code >= 400


def generate_sample_logs(num_logs: int = 1000) -> List[LogEntry]:
    """生成示例日志数据"""
    if num_logs <= 0:
        return []

    actions = ['view', 'click', 'search', 'purchase', 'login', 'logout']
    pages = ['/home', '/products', '/cart', '/checkout', '/profile', '/search']
    ip_prefixes = ['192.168.1.', '10.0.0.', '172.16.0.', '203.0.113.']

    logs = []
    base_time = datetime.now() - timedelta(hours=24)

    for i in range(num_logs):
        time_offset = random.randint(0, 86400)
        timestamp = (base_time + timedelta(seconds=time_offset)).isoformat()
        user_id = f"user_{random.randint(1000, 9999)}"
        action = random.choice(actions)
        page = random.choice(pages)
        ip_address = f"{random.choice(ip_prefixes)}{random.randint(1, 254)}"

        # 状态码分布：90% 200, 7% 404, 3% 500
        rand_val = random.random()
        if rand_val < 0.90:
            status_code = 200
        elif rand_val < 0.97:
            status_code = 404
        else:
            status_code = 500

        log_entry = LogEntry(timestamp, user_id, action, page, ip_address, status_code)
        logs.append(log_entry)

    return logs


def filter_by_status_code(logs: List[LogEntry], status_code: int) -> List[LogEntry]:
    """过滤指定状态码的日志"""
    return [log for log in logs if log.status_code == status_code]


def group_by_action(logs: List[LogEntry]) -> Dict[str, int]:
    """按动作分组统计"""
    action_counts = {}
    for log in logs:
        action_counts[log.action] = action_counts.get(log.action, 0) + 1
    return action_counts


def find_top_pages(logs: List[LogEntry], top_n: int = 5) -> List[Tuple[str, int]]:
    """找出访问量最高的页面"""
    if top_n <= 0:
        return []

    page_counts = {}
    for log in logs:
        page_counts[log.page] = page_counts.get(log.page, 0) + 1

    sorted_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_pages[:top_n]


def calculate_error_rate(logs: List[LogEntry]) -> float:
    """计算错误率"""
    if not logs:
        return 0.0

    error_count = sum(1 for log in logs if log.is_error())
    return error_count / len(logs)


def analyze_user_sessions(logs: List[LogEntry]) -> Dict[str, int]:
    """分析用户会话（每个用户的操作次数）"""
    user_sessions = {}
    for log in logs:
        user_sessions[log.user_id] = user_sessions.get(log.user_id, 0) + 1
    return user_sessions


def simulate_log_processing_pipeline():
    """模拟完整的日志处理管道"""
    # 生成日志
    raw_logs = generate_sample_logs(1000)

    # 数据清洗
    valid_logs = [log for log in raw_logs if log.user_id and log.action and log.page]

    # 分析
    action_stats = group_by_action(valid_logs)
    top_pages = find_top_pages(valid_logs, 3)
    error_rate = calculate_error_rate(valid_logs)
    user_sessions = analyze_user_sessions(valid_logs)

    # 找出最活跃的用户
    most_active_users = sorted(user_sessions.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        'total_logs': len(valid_logs),
        'action_stats': action_stats,
        'top_pages': top_pages,
        'error_rate': error_rate,
        'most_active_users': most_active_users
    }


def main():
    """主函数"""
    results = simulate_log_processing_pipeline()

    print("=== 日志分析结果 ===")
    print(f"总日志数: {results['total_logs']}")
    print(f"错误率: {results['error_rate']:.2%}")
    print("\n用户行为统计:")
    for action, count in sorted(results['action_stats'].items()):
        print(f"  {action}: {count}")
    print("\n热门页面:")
    for page, count in results['top_pages']:
        print(f"  {page}: {count} 次访问")
    print("\n最活跃用户:")
    for user_id, session_count in results['most_active_users']:
        print(f"  {user_id}: {session_count} 次操作")


if __name__ == "__main__":
    main()