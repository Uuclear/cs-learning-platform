#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据湖模式演进模拟器

本示例演示数据湖中的模式演进处理，
展示如何处理向后兼容和不兼容的模式变更。
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
        print("✅ 定义初始模式 (版本 1):")
        for field, field_type in schema.items():
            print(f"   - {field}: {field_type}")

    def add_new_field(self, field_name: str, field_type: str,
                     default_value: Any = None) -> int:
        """添加新字段（向后兼容变更）"""
        new_version = self.current_schema_version + 1

        # 复制当前模式并添加新字段
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
        print(f"✅ 添加新字段 (版本 {new_version}): {field_name} ({field_type})")
        if default_value is not None:
            print(f"   默认值: {default_value}")

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
            "compatibility": "forward",  # 移除字段通常是前向兼容
            "change_type": "remove_field",
            "removed_field": field_name,
            "removed_field_type": removed_field_type
        }

        self.current_schema_version = new_version
        print(f"⚠️  移除字段 (版本 {new_version}): {field_name} ({removed_field_type})")
        print("   注意: 这可能是不兼容变更，需要谨慎处理!")

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
            "compatibility": "none",  # 类型变更通常不兼容
            "change_type": "change_type",
            "field": field_name,
            "old_type": old_type,
            "new_type": new_type
        }

        self.current_schema_version = new_version
        print(f"❌ 更改字段类型 (版本 {new_version}): {field_name} ({old_type} → {new_type})")
        print("   警告: 这是不兼容变更，可能导致现有代码失败!")

        return new_version

    def validate_data_against_schema(self, data: Dict[str, Any],
                                   schema_version: Optional[int] = None) -> bool:
        """验证数据是否符合指定版本的模式"""
        if schema_version is None:
            schema_version = self.current_schema_version

        if schema_version not in self.schema_history:
            raise ValueError(f"模式版本 {schema_version} 不存在")

        schema = self.schema_history[schema_version]["fields"]

        # 检查必需字段是否存在
        for field in schema:
            if field not in data:
                print(f"❌ 数据缺少必需字段: {field}")
                return False

        # 检查字段类型（简化验证）
        for field, value in data.items():
            if field in schema:
                expected_type = schema[field]
                actual_type = self._get_python_type(value)
                if expected_type != actual_type:
                    print(f"❌ 字段 {field} 类型不匹配: 期望 {expected_type}, 实际 {actual_type}")
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
        print("\n🔄 演示向后兼容性:")

        # 创建旧版本数据
        old_data = {
            "user_id": 123,
            "name": "李四",
            "email": "lisi@example.com"
        }

        # 验证旧数据对旧模式
        if self.validate_data_against_schema(old_data, 1):
            print("✅ 旧数据通过旧模式验证")

        # 添加新字段后的模式应该仍然能读取旧数据（如果有默认值处理）
        new_version = self.add_new_field("phone", "string", "")

        # 在真实系统中，读取时会为缺失字段提供默认值
        enhanced_old_data = old_data.copy()
        enhanced_old_data["phone"] = ""  # 添加默认值

        if self.validate_data_against_schema(enhanced_old_data, new_version):
            print("✅ 增强的旧数据通过新模式验证")

    def get_current_schema(self) -> Dict[str, Any]:
        """获取当前模式"""
        return self.schema_history[self.current_schema_version]["fields"]

    def print_schema_evolution_history(self) -> None:
        """打印模式演进历史"""
        print(f"\n📋 模式演进历史 (共 {len(self.schema_history)} 个版本):")
        for version, schema_info in self.schema_history.items():
            print(f"版本 {version}: {list(schema_info['fields'].keys())}")


def main():
    """主函数：演示模式演进"""
    print("🔄 数据湖模式演进演示")
    print("=" * 50)

    simulator = SchemaEvolutionSimulator()

    # 1. 定义初始模式
    initial_schema = {
        "user_id": "number",
        "name": "string",
        "email": "string",
        "created_at": "string"
    }
    simulator.define_initial_schema(initial_schema)

    # 2. 添加新字段（向后兼容）
    simulator.add_new_field("last_login", "string", "1970-01-01")
    simulator.add_new_field("is_premium", "boolean", False)

    # 3. 演示向后兼容性
    simulator.demonstrate_backward_compatibility()

    # 4. 展示不兼容变更的风险
    print("\n⚠️  演示不兼容变更的风险:")
    try:
        # 这会产生警告但继续执行
        simulator.change_field_type("user_id", "string")
    except Exception as e:
        print(f"错误: {e}")

    # 5. 打印完整的演进历史
    simulator.print_schema_evolution_history()

    print("\n✅ 模式演进演示完成!")
    print("\n💡 关键要点:")
    print("   - 添加可选字段通常是向后兼容的")
    print("   - 移除字段或更改类型通常会导致不兼容")
    print("   - 现代数据湖格式（Delta Lake, Iceberg, Hudi）提供模式演进支持")
    print("   - 始终考虑现有消费者如何处理模式变更")


if __name__ == "__main__":
    main()