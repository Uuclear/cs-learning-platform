#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：结构化日志记录器实现
实现一个支持JSON格式输出、多级别日志和上下文字段的结构化日志记录器
"""

import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional


class StructuredLogger:
    """结构化日志记录器，支持JSON格式输出和上下文信息"""

    # 日志级别定义
    LEVELS = {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50
    }

    def __init__(self, name: str, level: str = 'INFO'):
        """
        初始化日志记录器

        Args:
            name: 日志记录器名称
            level: 最低日志级别，默认为INFO
        """
        self.name = name
        self.level = self.LEVELS.get(level.upper(), 20)
        self.context_fields: Dict[str, Any] = {}

    def add_context(self, **kwargs) -> None:
        """
        添加上下文字段到所有后续日志中

        Args:
            **kwargs: 要添加的上下文键值对
        """
        self.context_fields.update(kwargs)

    def _should_log(self, level_name: str) -> bool:
        """
        判断是否应该记录当前级别的日志

        Args:
            level_name: 日志级别名称

        Returns:
            bool: 是否应该记录
        """
        level_value = self.LEVELS.get(level_name, 0)
        return level_value >= self.level

    def _format_log(self, level: str, message: str, **kwargs) -> str:
        """
        格式化日志为JSON字符串

        Args:
            level: 日志级别
            message: 日志消息
            **kwargs: 额外的日志字段

        Returns:
            str: JSON格式的日志字符串
        """
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
        """记录DEBUG级别日志"""
        if self._should_log('DEBUG'):
            print(self._format_log('DEBUG', message, **kwargs), file=sys.stdout)

    def info(self, message: str, **kwargs) -> None:
        """记录INFO级别日志"""
        if self._should_log('INFO'):
            print(self._format_log('INFO', message, **kwargs), file=sys.stdout)

    def warning(self, message: str, **kwargs) -> None:
        """记录WARNING级别日志"""
        if self._should_log('WARNING'):
            print(self._format_log('WARNING', message, **kwargs), file=sys.stderr)

    def error(self, message: str, **kwargs) -> None:
        """记录ERROR级别日志"""
        if self._should_log('ERROR'):
            print(self._format_log('ERROR', message, **kwargs), file=sys.stderr)

    def critical(self, message: str, **kwargs) -> None:
        """记录CRITICAL级别日志"""
        if self._should_log('CRITICAL'):
            print(self._format_log('CRITICAL', message, **kwargs), file=sys.stderr)


def main():
    """主函数，演示结构化日志记录器的使用"""
    # 创建日志记录器
    logger = StructuredLogger('web_app', level='DEBUG')

    # 添加应用级上下文
    logger.add_context(
        service='user-service',
        version='1.2.0',
        environment='production'
    )

    # 记录不同级别的日志
    logger.info('应用启动成功', startup_time='2026-05-03T10:00:00Z')

    # 模拟用户请求处理
    request_id = 'req-12345'
    user_id = 'user-67890'
    logger.info('处理用户请求',
                request_id=request_id,
                user_id=user_id,
                endpoint='/api/users/profile')

    # 模拟数据库查询
    logger.debug('执行数据库查询',
                 query='SELECT * FROM users WHERE id = ?',
                 params=[user_id],
                 duration_ms=45)

    # 模拟警告情况
    logger.warning('缓存未命中',
                   cache_key=f'user_profile:{user_id}',
                   fallback_to_db=True)

    # 模拟错误情况
    try:
        # 模拟外部API调用失败
        raise ConnectionError('第三方服务不可用')
    except ConnectionError as e:
        logger.error('外部服务调用失败',
                     error=str(e),
                     service='payment-api',
                     retry_count=3)

    # 记录关键业务事件
    logger.info('用户登录成功',
                user_id=user_id,
                ip_address='192.168.1.100',
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)')

    print("\n=== 结构化日志演示完成 ===")


if __name__ == '__main__':
    main()