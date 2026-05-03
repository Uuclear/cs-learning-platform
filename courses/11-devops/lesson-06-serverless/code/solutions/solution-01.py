#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serverless 课程 - 练习题1 解决方案

实现一个简单的 Lambda 函数，处理不同类型的事件并返回相应的响应。
"""

import json
from datetime import datetime


def lambda_handler(event, context):
    """
    处理 Lambda 事件

    Args:
        event: 触发事件
        context: 运行时上下文

    Returns:
        响应字典
    """
    # 检查事件类型
    event_type = event.get('type', 'unknown')

    if event_type == 'http':
        return handle_http_event(event)
    elif event_type == 's3':
        return handle_s3_event(event)
    elif event_type == 'sns':
        return handle_sns_event(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': '不支持的事件类型',
                'event_type': event_type
            })
        }


def handle_http_event(event):
    """处理 HTTP 事件"""
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'HTTP 事件处理成功',
            'path': event.get('path', '/'),
            'method': event.get('method', 'GET'),
            'timestamp': datetime.now().isoformat()
        })
    }


def handle_s3_event(event):
    """处理 S3 事件"""
    records = event.get('Records', [])
    bucket_names = [record.get('s3', {}).get('bucket', {}).get('name') for record in records]

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'处理了 {len(records)} 个 S3 事件',
            'buckets': bucket_names,
            'timestamp': datetime.now().isoformat()
        })
    }


def handle_sns_event(event):
    """处理 SNS 事件"""
    message = event.get('Records', [{}])[0].get('Sns', {}).get('Message', '')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'SNS 事件处理成功',
            'received_message': message[:100] + '...' if len(message) > 100 else message,
            'timestamp': datetime.now().isoformat()
        })
    }