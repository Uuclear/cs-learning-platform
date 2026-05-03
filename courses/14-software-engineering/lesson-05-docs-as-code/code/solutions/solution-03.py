#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：完整的OpenAPI生成器

这个解决方案扩展了示例3的功能，支持请求/响应体的详细定义、
参数验证规则、安全方案定义，并可以输出为YAML格式。
"""

import json
from typing import Any, Dict, List, Optional, Union
import yaml


class OpenAPIGenerator:
    """OpenAPI规范生成器类"""

    def __init__(self, title: str = "API文档", version: str = "1.0.0"):
        self.title = title
        self.version = version
        self.spec = self._create_base_spec()

    def _create_base_spec(self) -> Dict[str, Any]:
        """创建OpenAPI规范的基础结构"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": ""
            },
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {}
            }
        }

    def add_endpoint(
        self,
        path: str,
        method: str,
        summary: str,
        description: str = "",
        parameters: Optional[List[Dict[str, Any]]] = None,
        request_body: Optional[Dict[str, Any]] = None,
        responses: Optional[Dict[str, Any]] = None,
        security: Optional[List[Dict[str, List[str]]]] = None
    ) -> None:
        """
        添加API端点到规范中

        参数:
            path: API路径（例如: /users/{id}）
            method: HTTP方法（GET、POST、PUT、DELETE等）
            summary: 简短摘要
            description: 详细描述
            parameters: 路径/查询/头部参数列表
            request_body: 请求体定义
            responses: 响应定义
            security: 安全方案
        """
        method = method.lower()
        if method not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
            raise ValueError(f"无效的HTTP方法: {method}")

        operation = {
            "summary": summary,
            "description": description
        }

        if parameters:
            operation["parameters"] = self._validate_parameters(parameters)

        if request_body:
            operation["requestBody"] = self._validate_request_body(request_body)

        if responses:
            operation["responses"] = responses
        else:
            operation["responses"] = {"200": {"description": "成功响应"}}

        if security:
            operation["security"] = security

        if path not in self.spec["paths"]:
            self.spec["paths"][path] = {}

        self.spec["paths"][path][method] = operation

    def add_schema(self, name: str, schema: Dict[str, Any]) -> None:
        """
        添加组件模式到规范中

        参数:
            name: 模式名称
            schema: 模式定义
        """
        self.spec["components"]["schemas"][name] = schema

    def add_security_scheme(
        self,
        name: str,
        scheme_type: str,
        description: str = "",
        **kwargs
    ) -> None:
        """
        添加安全方案到规范中

        参数:
            name: 安全方案名称
            scheme_type: 方案类型（http、apiKey、oauth2、openIdConnect）
            description: 描述
            **kwargs: 方案特定参数
        """
        security_scheme = {
            "type": scheme_type,
            "description": description
        }

        if scheme_type == "http":
            if "scheme" not in kwargs:
                raise ValueError("HTTP安全方案需要'scheme'参数")
            security_scheme["scheme"] = kwargs["scheme"]
        elif scheme_type == "apiKey":
            if "in" not in kwargs or "name" not in kwargs:
                raise ValueError("API Key安全方案需要'in'和'name'参数")
            security_scheme["in"] = kwargs["in"]
            security_scheme["name"] = kwargs["name"]
        elif scheme_type == "oauth2":
            if "flows" not in kwargs:
                raise ValueError("OAuth2安全方案需要'flows'参数")
            security_scheme["flows"] = kwargs["flows"]

        self.spec["components"]["securitySchemes"][name] = security_scheme

    def set_api_info(
        self,
        title: Optional[str] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
        terms_of_service: Optional[str] = None,
        contact: Optional[Dict[str, str]] = None,
        license_info: Optional[Dict[str, str]] = None
    ) -> None:
        """
        设置API信息

        参数:
            title: API标题
            version: API版本
            description: API描述
            terms_of_service: 服务条款URL
            contact: 联系信息
            license_info: 许可证信息
        """
        if title is not None:
            self.spec["info"]["title"] = title
        if version is not None:
            self.spec["info"]["version"] = version
        if description is not None:
            self.spec["info"]["description"] = description
        if terms_of_service is not None:
            self.spec["info"]["termsOfService"] = terms_of_service
        if contact is not None:
            self.spec["info"]["contact"] = contact
        if license_info is not None:
            self.spec["info"]["license"] = license_info

    def _validate_parameters(self, parameters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """验证参数定义"""
        validated = []
        for param in parameters:
            if "name" not in param or "in" not in param:
                raise ValueError("参数必须包含'name'和'in'字段")
            if param["in"] not in ["path", "query", "header", "cookie"]:
                raise ValueError(f"无效的参数位置: {param['in']}")
            validated.append(param)
        return validated

    def _validate_request_body(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """验证请求体定义"""
        if "content" not in request_body:
            raise ValueError("请求体必须包含'content'字段")
        return request_body

    def to_dict(self) -> Dict[str, Any]:
        """返回OpenAPI规范字典"""
        return self.spec

    def to_json(self, indent: int = 2) -> str:
        """返回JSON格式的OpenAPI规范"""
        return json.dumps(self.spec, indent=indent, ensure_ascii=False)

    def to_yaml(self) -> str:
        """返回YAML格式的OpenAPI规范"""
        try:
            return yaml.dump(self.spec, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except ImportError:
            # 如果没有安装pyyaml，使用简化的方法
            return self._to_yaml_simple()

    def _to_yaml_simple(self) -> str:
        """简化版YAML生成（不依赖外部库）"""
        def dict_to_yaml(d, indent=0):
            yaml_str = ""
            spaces = "  " * indent

            if isinstance(d, dict):
                for key, value in d.items():
                    if isinstance(value, (dict, list)):
                        yaml_str += f"{spaces}{key}:\n"
                        yaml_str += dict_to_yaml(value, indent + 1)
                    else:
                        yaml_str += f"{spaces}{key}: {value}\n"
            elif isinstance(d, list):
                for item in d:
                    if isinstance(item, (dict, list)):
                        yaml_str += f"{spaces}-\n"
                        yaml_str += dict_to_yaml(item, indent + 1)
                    else:
                        yaml_str += f"{spaces}- {item}\n"

            return yaml_str

        return f"openapi: {self.spec['openapi']}\n" + dict_to_yaml(self.spec["info"], 0) + "paths:\n" + dict_to_yaml(self.spec["paths"], 1)


def create_user_api_example() -> OpenAPIGenerator:
    """创建用户管理API的示例"""
    generator = OpenAPIGenerator("用户管理API", "1.0.0")

    # 设置API信息
    generator.set_api_info(
        description="用户管理RESTful API",
        contact={"name": "API支持团队", "email": "api-support@example.com"},
        license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
    )

    # 添加安全方案
    generator.add_security_scheme(
        "bearerAuth",
        "http",
        "JWT Bearer Token认证",
        scheme="bearer",
        bearerFormat="JWT"
    )

    # 添加用户模式
    user_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "format": "uuid"},
            "name": {"type": "string", "minLength": 1},
            "email": {"type": "string", "format": "email"},
            "createdAt": {"type": "string", "format": "date-time"}
        },
        "required": ["name", "email"]
    }
    generator.add_schema("User", user_schema)

    # GET /users - 获取用户列表
    generator.add_endpoint(
        "/users",
        "GET",
        "获取用户列表",
        "返回所有用户的列表，支持分页和过滤",
        parameters=[
            {
                "name": "limit",
                "in": "query",
                "description": "返回结果的最大数量",
                "required": False,
                "schema": {"type": "integer", "default": 10, "minimum": 1, "maximum": 100}
            },
            {
                "name": "offset",
                "in": "query",
                "description": "跳过的记录数量",
                "required": False,
                "schema": {"type": "integer", "default": 0, "minimum": 0}
            }
        ],
        responses={
            "200": {
                "description": "用户列表",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "users": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"}
                                },
                                "total": {"type": "integer"}
                            }
                        }
                    }
                }
            }
        },
        security=[{"bearerAuth": []}]
    )

    # POST /users - 创建用户
    generator.add_endpoint(
        "/users",
        "POST",
        "创建新用户",
        "创建一个新的用户记录",
        request_body={
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/User"}
                }
            }
        },
        responses={
            "201": {
                "description": "用户创建成功",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/User"}
                    }
                }
            },
            "400": {
                "description": "请求数据无效"
            }
        },
        security=[{"bearerAuth": []}]
    )

    # GET /users/{id} - 获取单个用户
    generator.add_endpoint(
        "/users/{id}",
        "GET",
        "获取单个用户",
        "根据ID获取特定用户的信息",
        parameters=[
            {
                "name": "id",
                "in": "path",
                "description": "用户ID",
                "required": True,
                "schema": {"type": "string", "format": "uuid"}
            }
        ],
        responses={
            "200": {
                "description": "用户信息",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/User"}
                    }
                }
            },
            "404": {
                "description": "用户不存在"
            }
        },
        security=[{"bearerAuth": []}]
    )

    return generator


if __name__ == "__main__":
    # 创建示例API
    api_generator = create_user_api_example()

    print("OpenAPI规范 (JSON格式):")
    print(api_generator.to_json())

    print("\n" + "="*60 + "\n")

    print("OpenAPI规范 (YAML格式):")
    print(api_generator.to_yaml())

    # 保存到文件
    with open("user_api_openapi.json", "w", encoding="utf-8") as f:
        f.write(api_generator.to_json())

    with open("user_api_openapi.yaml", "w", encoding="utf-8") as f:
        f.write(api_generator.to_yaml())

    print(f"\n规范已保存到:")
    print("- user_api_openapi.json")
    print("- user_api_openapi.yaml")