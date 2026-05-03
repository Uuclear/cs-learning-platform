#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可观测性课程示例 1: 结构化日志

本示例演示如何使用 Python 标准库实现结构化日志记录，
包括不同日志级别、上下文信息和 JSON 格式输出。
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, Any


class StructuredLogger:
    """结构化日志记录器类"""

    def __init__(self, name: str):
        """
        初始化结构化日志记录器

        Args:
            name: 日志记录器名称
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 创建控制台处理器
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def _format_log_entry(self, level: str, message: str, **kwargs) -> str:
        """
        格式化日志条目为 JSON 格式

        Args:
            level: 日志级别
            message: 日志消息
            **kwargs: 额外的上下文信息

        Returns:
            JSON 格式的日志字符串
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
            "logger": self.logger.name,
            **kwargs
        }
        return json.dumps(log_entry, ensure_ascii=False)

    def debug(self, message: str, **kwargs) -> None:
        """记录调试级别日志"""
        log_str = self._format_log_entry("DEBUG", message, **kwargs)
        self.logger.debug(log_str)

    def info(self, message: str, **kwargs) -> None:
        """记录信息级别日志"""
        log_str = self._format_log_entry("INFO", message, **kwargs)
        self.logger.info(log_str)

    def warning(self, message: str, **kwargs) -> None:
        """记录警告级别日志"""
        log_str = self._format_log_entry("WARNING", message, **kwargs)
        self.logger.warning(log_str)

    def error(self, message: str, **kwargs) -> None:
        """记录错误级别日志"""
        log_str = self._format_log_entry("ERROR", message, **kwargs)
        self.logger.error(log_str)


def simulate_user_activity():
    """模拟用户活动日志"""
    logger = StructuredLogger("user-service")

    # 模拟用户登录
    user_id = "user_12345"
    session_id = "sess_67890"

    logger.info(
        "用户登录成功",
        user_id=user_id,
        session_id=session_id,
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    )

    # 模拟 API 调用
    logger.info(
        "处理用户请求",
        user_id=user_id,
        endpoint="/api/v1/profile",
        method="GET",
        duration_ms=125,
        status_code=200
    )

    # 模拟警告情况
    logger.warning(
        "用户登录尝试次数过多",
        user_id="user_99999",
        attempts=5,
        ip_address="10.0.0.50",
        blocked=True
    )

    # 模拟错误情况
    try:
        # 模拟数据库连接失败
        raise ConnectionError("数据库连接超时")
    except ConnectionError as e:
        logger.error(
            "数据库连接失败",
            error=str(e),
            service="database",
            retry_count=3,
            stack_trace="ConnectionError: 数据库连接超时"
        )


def main():
    """主函数"""
    print("=== 可观测性课程：结构化日志示例 ===\n")
    simulate_user_activity()
    print("\n=== 日志示例结束 ===")


if __name__ == "__main__":
    main()