#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据湖模式演进解决方案

本解决方案实现了完整的模式演进处理功能。
"""

import json
from typing import Dict, List, Any, Optional


class SchemaEvolutionSimulator:
    """模式演进模拟器"""

    def __init__(self):
        self.current_schema_version = 1
        self.schema_history = {}
        self.data_samples = []

    def define_initial_schema(self, schema: Dict[str, Any]) -> None:
        """定义初始模式"""
        self.schema_history[1] = {
            "version": 1,
            "fields": schema,
            "compatibility": "backward"
        }

    def add_new_field(self, field_name: str, field_type: str,
                     default_value: Any = None) -> int:
        """添加新字段（向后兼容变更）"""
        new_version = self.current_schema_version + 1
        current_schema = self.schema_history[self.current_schema_version]["fields"]
        new_schema = current_schema.copy()
        new_schema[field_name] = field_type

        self.schema_history[new_version] = {
            "version": new_version,
            "fields": new_schema,
            "compatibility": "backward",
            "change_type": "add_field",
            "new_field": field_name
        }

        self.current_schema_version = new_version
        return new_version

    def remove_field(self, field_name: str) -> int:
        """移除字段（可能不兼容变更）"""
        new_version = self.current_schema_version + 1
        current_schema = self.schema_history[self.current_schema_version]["fields"]
        if field_name not in current_schema:
            raise ValueError(f"字段 '{field_name}' 不存在于当前模式中")

        new_schema = current_schema.copy()
        removed_field_type = new_schema.pop(field_name)

        self.schema_history[new_version] = {
            "version": new_version,
            "fields": new_schema,
            "compatibility": "forward",
            "change_type": "remove_field",
            "removed_field": field_name,
            "removed_field_type": removed_field_type
        }

        self.current_schema_version = new_version
        return new_version

    def change_field_type(self, field_name: str, new_type: str) -> int:
        """更改字段类型（通常不兼容）"""
        new_version = self.current_schema_version + 1
        current_schema = self.schema_history[self.current_schema_version]["fields"]
        if field_name not in current_schema:
            raise ValueError(f"字段 '{field_name}' 不存在于当前模式中")

        old_type = current_schema[field_name]
        new_schema = current_schema.copy()
        new_schema[field_name] = new_type

        self.schema_history[new_version] = {
            "version": new_version,
            "fields": new_schema,
            "compatibility": "none",
            "change_type": "change_type",
            "field": field_name,
            "old_type": old_type,
            "new_type": new_type
        }

        self.current_schema_version = new_version
        return new_version

    def validate_data_against_schema(self, data: Dict[str, Any],
                                   schema_version: Optional[int] = None) -> bool:
        """验证数据是否符合指定版本的模式"""
        if schema_version is None:
            schema_version = self.current_schema_version

        if schema_version not in self.schema_history:
            raise ValueError(f"模式版本 {schema_version} 不存在")

        schema = self.schema_history[schema_version]["fields"]

        for field in schema:
            if field not in data:
                return False

        for field, value in data.items():
            if field in schema:
                expected_type = schema[field]
                actual_type = self._get_python_type(value)
                if expected_type != actual_type:
                    return False

        return True

    def _get_python_type(self, value: Any) -> str:
        """获取Python值对应的类型字符串"""
        if isinstance(value, str):
            return "string"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "unknown"

    def demonstrate_backward_compatibility(self) -> None:
        """演示向后兼容性"""
        old_data = {
            "user_id": 123,
            "name": "李四",
            "email": "lisi@example.com"
        }

        if self.validate_data_against_schema(old_data, 1):
            pass

        new_version = self.add_new_field("phone", "string", "")
        enhanced_old_data = old_data.copy()
        enhanced_old_data["phone"] = ""

        if self.validate_data_against_schema(enhanced_old_data, new_version):
            pass

    def get_current_schema(self) -> Dict[str, Any]:
        """获取当前模式"""
        return self.schema_history[self.current_schema_version]["fields"]


def main():
    """主函数：演示模式演进"""
    simulator = SchemaEvolutionSimulator()

    initial_schema = {
        "user_id": "number",
        "name": "string",
        "email": "string",
        "created_at": "string"
    }
    simulator.define_initial_schema(initial_schema)

    simulator.add_new_field("last_login", "string", "1970-01-01")
    simulator.add_new_field("is_premium", "boolean", False)

    simulator.demonstrate_backward_compatibility()


if __name__ == "__main__":
    main()