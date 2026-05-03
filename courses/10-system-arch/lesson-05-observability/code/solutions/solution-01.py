#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可观测性课程解决方案 1: 结构化日志

此解决方案展示了如何改进结构化日志实现，
包括更好的错误处理和更丰富的上下文信息。
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class EnhancedStructuredLogger:
    """增强的结构化日志记录器"""

    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复处理器
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _create_log_record(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """创建结构化的日志记录"""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "level": level,
            "message": message,
            "logger": self.logger.name,
        }

        # 添加额外上下文
        if kwargs:
            record.update(kwargs)

        return record

    def _log(self, level: str, level_num: int, message: str, **kwargs) -> None:
        """通用日志记录方法"""
        record = self._create_log_record(level, message, **kwargs)
        log_str = json.dumps(record, ensure_ascii=False, default=str)
        self.logger.log(level_num, log_str)

    def debug(self, message: str, **kwargs) -> None:
        self._log("DEBUG", logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        self._log("INFO", logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self._log("WARNING", logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._log("ERROR", logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        self._log("CRITICAL", logging.CRITICAL, message, **kwargs)


def main():
    """主函数演示"""
    logger = EnhancedStructuredLogger("solution-demo", logging.DEBUG)

    # 基本日志记录
    logger.info("应用启动", version="1.0.0", environment="development")

    # 带错误信息的日志
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(
            "除零错误",
            error=str(e),
            operation="division",
            operands={"dividend": 10, "divisor": 0}
        )

    # 性能日志
    logger.info(
        "数据库查询完成",
        query="SELECT * FROM users WHERE id = ?",
        duration_ms=45.2,
        rows_returned=1,
        user_id="user_123"
    )


if __name__ == "__main__":
    main()