#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 AWS Lambda 函数执行 - 事件驱动架构示例

这个脚本演示了 Serverless 函数如何响应不同类型的事件触发器，
包括 HTTP 请求、S3 事件和定时任务。
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Union


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    模拟 AWS Lambda 处理函数

    Args:
        event: 触发事件，包含事件源信息
        context: 运行时上下文，包含函数元数据

    Returns:
        包含响应数据的字典
    """
    print(f"开始处理事件: {json.dumps(event, ensure_ascii=False)}")

    # 根据事件类型执行不同的逻辑
    if event.get('source') == 'http':
        return handle_http_request(event)
    elif event.get('source') == 's3':
        return handle_s3_event(event)
    elif event.get('source') == 'schedule':
        return handle_scheduled_event(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': '不支持的事件类型',
                'received_event': event
            }, ensure_ascii=False)
        }


def handle_http_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """处理 HTTP 请求事件"""
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')

    # 模拟业务逻辑处理时间
    time.sleep(0.1)

    response_body = {
        'message': f'成功处理 {method} 请求到 {path}',
        'timestamp': datetime.now().isoformat(),
        'headers': event.get('headers', {}),
        'queryStringParameters': event.get('queryStringParameters', {})
    }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response_body, ensure_ascii=False)
    }


def handle_s3_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """处理 S3 对象创建事件"""
    records = event.get('Records', [])

    processed_files = []
    for record in records:
        bucket_name = record.get('s3', {}).get('bucket', {}).get('name')
        object_key = record.get('s3', {}).get('object', {}).get('key')

        if bucket_name and object_key:
            # 模拟文件处理逻辑
            time.sleep(0.05)
            processed_files.append({
                'bucket': bucket_name,
                'key': object_key,
                'size': record.get('s3', {}).get('object', {}).get('size', 0),
                'processed_at': datetime.now().isoformat()
            })

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'成功处理 {len(processed_files)} 个 S3 对象',
            'processed_files': processed_files
        }, ensure_ascii=False)
    }


def handle_scheduled_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """处理定时调度事件"""
    schedule_name = event.get('schedule_name', 'unknown')

    # 模拟定时任务逻辑
    time.sleep(0.02)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'定时任务 {schedule_name} 执行完成',
            'execution_time': datetime.now().isoformat(),
            'event_data': event
        }, ensure_ascii=False)
    }


if __name__ == '__main__':
    """演示不同类型的事件触发"""
    print("=== Serverless Lambda 函数模拟演示 ===\n")

    # HTTP 请求事件示例
    http_event = {
        'source': 'http',
        'httpMethod': 'POST',
        'path': '/api/users',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': {'debug': 'true'}
    }

    print("1. 处理 HTTP 请求事件:")
    result = lambda_handler(http_event, {})
    print(f"响应: {result['body']}\n")

    # S3 事件示例
    s3_event = {
        'source': 's3',
        'Records': [
            {
                's3': {
                    'bucket': {'name': 'my-bucket'},
                    'object': {'key': 'uploads/image.jpg', 'size': 1024}
                }
            },
            {
                's3': {
                    'bucket': {'name': 'my-bucket'},
                    'object': {'key': 'uploads/document.pdf', 'size': 2048}
                }
            }
        ]
    }

    print("2. 处理 S3 事件:")
    result = lambda_handler(s3_event, {})
    print(f"响应: {result['body']}\n")

    # 定时事件示例
    schedule_event = {
        'source': 'schedule',
        'schedule_name': 'daily-cleanup'
    }

    print("3. 处理定时事件:")
    result = lambda_handler(schedule_event, {})
    print(f"响应: {result['body']}\n")

    print("=== 演示完成 ===")