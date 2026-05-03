#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：API文档生成器 - OpenAPI规范生成

这个脚本演示了如何从Python函数定义生成OpenAPI（Swagger）规范。
OpenAPI是一种用于描述RESTful API的标准格式，可以用于生成交互式文档、
客户端SDK和服务器存根代码。
"""

from typing import Any, Dict, List, Optional


def generate_openapi_spec(
    endpoints: List[Dict[str, Any]],
    title: str = "自动生成的API文档",
    version: str = "1.0.0"
) -> Dict[str, Any]:
    """
    根据端点定义生成OpenAPI规范

    参数:
        endpoints: API端点列表，每个端点包含path、method、summary等信息
        title: API文档标题
        version: API版本号

    返回:
        OpenAPI 3.0.0规范的字典表示
    """
    # 初始化OpenAPI规范基础结构
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": version,
            "description": "基于Python函数定义生成的OpenAPI规范"
        },
        "paths": {}
    }

    # 处理每个端点
    for endpoint in endpoints:
        path = endpoint["path"]
        method = endpoint["method"].lower()

        # 构建操作对象
        operation = {
            "summary": endpoint.get("summary", ""),
            "description": endpoint.get("description", ""),
            "responses": {
                "200": {
                    "description": "成功响应"
                }
            }
        }

        # 添加请求体（如果存在）
        if "request_body" in endpoint:
            operation["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": endpoint["request_body"]
                    }
                }
            }

        # 添加参数（如果存在）
        if "parameters" in endpoint:
            operation["parameters"] = endpoint["parameters"]

        # 将操作添加到路径中
        if path not in spec["paths"]:
            spec["paths"][path] = {}
        spec["paths"][path][method] = operation

    return spec


def create_endpoint_definition(
    path: str,
    method: str,
    summary: str,
    description: str = "",
    parameters: Optional[List[Dict[str, Any]]] = None,
    request_body: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    创建端点定义的辅助函数

    参数:
        path: API路径
        method: HTTP方法（GET、POST、PUT、DELETE等）
        summary: 简短摘要
        description: 详细描述
        parameters: 路径/查询参数列表
        request_body: 请求体模式定义

    返回:
        端点定义字典
    """
    endpoint = {
        "path": path,
        "method": method.upper(),
        "summary": summary,
        "description": description
    }

    if parameters:
        endpoint["parameters"] = parameters
    if request_body:
        endpoint["request_body"] = request_body

    return endpoint


def generate_yaml_output(spec: Dict[str, Any]) -> str:
    """
    将OpenAPI规范转换为YAML格式字符串（简化版）

    注意：这只是一个简化的YAML生成器，实际项目应使用pyyaml库。

    参数:
        spec: OpenAPI规范字典

    返回:
        YAML格式的字符串
    """
    def dict_to_yaml(d: Dict[str, Any], indent: int = 0) -> str:
        yaml_str = ""
        spaces = "  " * indent

        for key, value in d.items():
            if isinstance(value, dict):
                yaml_str += f"{spaces}{key}:\n"
                yaml_str += dict_to_yaml(value, indent + 1)
            elif isinstance(value, list):
                yaml_str += f"{spaces}{key}:\n"
                for item in value:
                    if isinstance(item, dict):
                        yaml_str += f"{spaces}  -\n"
                        yaml_str += dict_to_yaml(item, indent + 2)
                    else:
                        yaml_str += f"{spaces}  - {item}\n"
            else:
                yaml_str += f"{spaces}{key}: {value}\n"

        return yaml_str

    return f"openapi: {spec['openapi']}\n" + dict_to_yaml(spec["info"], 0) + "paths:\n" + dict_to_yaml(spec["paths"], 1)


if __name__ == "__main__":
    # 定义API端点
    endpoints = [
        create_endpoint_definition(
            path="/users",
            method="GET",
            summary="获取用户列表",
            description="返回所有用户的列表",
            parameters=[
                {
                    "name": "limit",
                    "in": "query",
                    "description": "返回结果的最大数量",
                    "required": False,
                    "schema": {"type": "integer", "default": 10}
                }
            ]
        ),
        create_endpoint_definition(
            path="/users/{id}",
            method="GET",
            summary="获取单个用户",
            description="根据ID获取特定用户的信息",
            parameters=[
                {
                    "name": "id",
                    "in": "path",
                    "description": "用户ID",
                    "required": True,
                    "schema": {"type": "string"}
                }
            ]
        ),
        create_endpoint_definition(
            path="/users",
            method="POST",
            summary="创建新用户",
            description="创建一个新的用户记录",
            request_body={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["name", "email"]
            }
        )
    ]

    # 生成OpenAPI规范
    openapi_spec = generate_openapi_spec(endpoints, "用户管理API", "1.0.0")

    print("OpenAPI规范 (JSON格式):")
    import json
    print(json.dumps(openapi_spec, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    print("OpenAPI规范 (YAML格式 - 简化版):")
    print(generate_yaml_output(openapi_spec))