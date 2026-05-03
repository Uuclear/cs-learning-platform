#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：结构化日志记录器
完整的结构化日志实现，包含所有要求的功能
"""

import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional


class StructuredLogger:
    """结构化日志记录器，支持JSON格式输出和上下文信息"""

    LEVELS = {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50
    }

    def __init__(self, name: str, level: str = 'INFO'):
        self.name = name
        self.level = self.LEVELS.get(level.upper(), 20)
        self.context_fields: Dict[str, Any] = {}

    def add_context(self, **kwargs) -> None:
        self.context_fields.update(kwargs)

    def _should_log(self, level_name: str) -> bool:
        level_value = self.LEVELS.get(level_name, 0)
        return level_value >= self.level

    def _format_log(self, level: str, message: str, **kwargs) -> str:
        log_record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'logger': self.name,
            'message': message,
            **self.context_fields,
            **kwargs
        }
        return json.dumps(log_record, ensure_ascii=False)

    def debug(self, message: str, **kwargs) -> None:
        if self._should_log('DEBUG'):
            print(self._format_log('DEBUG', message, **kwargs), file=sys.stdout)

    def info(self, message: str, **kwargs) -> None:
        if self._should_log('INFO'):
            print(self._format_log('INFO', message, **kwargs), file=sys.stdout)

    def warning(self, message: str, **kwargs) -> None:
        if self._should_log('WARNING'):
            print(self._format_log('WARNING', message, **kwargs), file=sys.stderr)

    def error(self, message: str, **kwargs) -> None:
        if self._should_log('ERROR'):
            print(self._format_log('ERROR', message, **kwargs), file=sys.stderr)

    def critical(self, message: str, **kwargs) -> None:
        if self._should_log('CRITICAL'):
            print(self._format_log('CRITICAL', message, **kwargs), file=sys.stderr)


# 测试代码
if __name__ == '__main__':
    logger = StructuredLogger('solution_test', level='DEBUG')
    logger.add_context(service='test-service', version='1.0.0')

    logger.info('测试信息日志', test_id='solution-01')
    logger.error('测试错误日志', error_code=500)