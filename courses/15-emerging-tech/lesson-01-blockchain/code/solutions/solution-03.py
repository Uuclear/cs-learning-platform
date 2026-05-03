#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：简易智能合约解释器
实现基本的键值存储和规则引擎
"""

import hashlib
import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime


class SimpleSmartContract:
    """简易智能合约解释器"""

    def __init__(self):
        self.storage: Dict[str, Any] = {}  # 键值存储
        self.functions: Dict[str, Callable] = {}  # 可调用函数
        self.owner: str = "contract_creator"
        self.created_at: str = datetime.now().isoformat()

        # 注册内置函数
        self._register_builtin_functions()

    def _register_builtin_functions(self):
        """注册内置函数"""
        self.functions["set"] = self._set_value
        self.functions["get"] = self._get_value
        self.functions["delete"] = self._delete_value
        self.functions["exists"] = self._key_exists
        self.functions["keys"] = self._list_keys

    def _set_value(self, key: str, value: Any) -> bool:
        """设置键值"""
        try:
            # 尝试序列化以确保值是有效的JSON
            json.dumps(value)
            self.storage[key] = value
            return True
        except (TypeError, ValueError):
            return False

    def _get_value(self, key: str) -> Any:
        """获取键值"""
        return self.storage.get(key, None)

    def _delete_value(self, key: str) -> bool:
        """删除键值"""
        if key in self.storage:
            del self.storage[key]
            return True
        return False

    def _key_exists(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self.storage

    def _list_keys(self) -> List[str]:
        """列出所有键"""
        return list(self.storage.keys())

    def execute(self, function_name: str, *args, **kwargs) -> Any:
        """
        执行合约函数

        Args:
            function_name: 函数名
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            函数执行结果
        """
        if function_name not in self.functions:
            raise ValueError(f"函数 '{function_name}' 未定义")

        try:
            return self.functions[function_name](*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"执行函数 '{function_name}' 时出错: {str(e)}")

    def deploy_rule_based_contract(self, rules: Dict[str, Any]):
        """
        部署基于规则的合约

        Args:
            rules: 规则配置字典
        """
        # 示例规则系统
        if "access_control" in rules:
            self._setup_access_control(rules["access_control"])

        if "validation_rules" in rules:
            self._setup_validation_rules(rules["validation_rules"])

        # 存储规则配置
        self.storage["_rules"] = rules

    def _setup_access_control(self, access_rules: Dict[str, List[str]]):
        """设置访问控制规则"""
        self.storage["_access_control"] = access_rules

    def _setup_validation_rules(self, validation_rules: Dict[str, Dict[str, Any]]):
        """设置验证规则"""
        self.storage["_validation_rules"] = validation_rules

        # 动态创建带验证的setter函数
        def validated_set(key: str, value: Any) -> bool:
            if key in validation_rules:
                rule = validation_rules[key]
                if "type" in rule:
                    # 安全的类型检查，避免使用 eval
                    expected_type = rule["type"]
                    if expected_type == "int" and not isinstance(value, int):
                        raise ValueError(f"值类型错误，期望 int")
                    elif expected_type == "float" and not isinstance(value, (int, float)):
                        raise ValueError(f"值类型错误，期望 float")
                    elif expected_type == "str" and not isinstance(value, str):
                        raise ValueError(f"值类型错误，期望 str")
                    elif expected_type == "bool" and not isinstance(value, bool):
                        raise ValueError(f"值类型错误，期望 bool")

                if "min" in rule and isinstance(value, (int, float)) and value < rule["min"]:
                    raise ValueError(f"值小于最小值 {rule['min']}")
                if "max" in rule and isinstance(value, (int, float)) and value > rule["max"]:
                    raise ValueError(f"值大于最大值 {rule['max']}")
                if "pattern" in rule:
                    # 简单的模式验证，例如长度检查
                    pattern_rule = rule["pattern"]
                    if pattern_rule == "non_empty_string" and isinstance(value, str) and len(value) == 0:
                        raise ValueError(f"字符串不能为空")
                    elif pattern_rule == "positive_number" and isinstance(value, (int, float)) and value <= 0:
                        raise ValueError(f"数值必须为正数")

            return self._set_value(key, value)

        self.functions["validated_set"] = validated_set

    def get_contract_info(self) -> Dict[str, Any]:
        """获取合约信息"""
        return {
            "owner": self.owner,
            "created_at": self.created_at,
            "storage_size": len(self.storage),
            "available_functions": list(self.functions.keys()),
            "hash": self.get_contract_hash()
        }

    def get_contract_hash(self) -> str:
        """计算合约哈希（用于验证合约完整性）"""
        contract_data = json.dumps({
            "storage": self.storage,
            "functions": list(self.functions.keys()),
            "owner": self.owner,
            "created_at": self.created_at
        }, sort_keys=True, default=str)
        return hashlib.sha256(contract_data.encode()).hexdigest()[:16]


def main():
    """主函数 - 演示智能合约功能"""
    print("=== 简易智能合约演示 ===\n")

    # 创建合约实例
    contract = SimpleSmartContract()
    print("📜 创建新的智能合约...")

    # 基本键值操作
    print("\n📦 基本键值存储操作:")
    contract.execute("set", "name", "MyToken")
    contract.execute("set", "symbol", "MTK")
    contract.execute("set", "total_supply", 1000000)
    contract.execute("set", "decimals", 18)

    print(f"   名称: {contract.execute('get', 'name')}")
    print(f"   符号: {contract.execute('get', 'symbol')}")
    print(f"   总供应量: {contract.execute('get', 'total_supply')}")
    print(f"   小数位数: {contract.execute('get', 'decimals')}")

    # 列出所有键
    print(f"\n🔑 存储的键: {contract.execute('keys')}")

    # 部署带规则的合约
    print("\n🛡️  部署带验证规则的合约...")
    rules = {
        "validation_rules": {
            "price": {
                "type": "float",
                "min": 0.0,
                "max": 1000000.0
            },
            "active": {
                "type": "bool"
            },
            "product_name": {
                "type": "str",
                "pattern": "non_empty_string"
            }
        },
        "access_control": {
            "admin": ["set_price", "toggle_active"],
            "user": ["get_price", "is_active"]
        }
    }

    contract.deploy_rule_based_contract(rules)

    # 使用带验证的设置函数
    print("\n✅ 测试有效数据:")
    try:
        contract.execute("validated_set", "price", 99.99)
        contract.execute("validated_set", "active", True)
        contract.execute("validated_set", "product_name", "Premium Widget")
        print(f"   价格: {contract.execute('get', 'price')}")
        print(f"   活跃状态: {contract.execute('get', 'active')}")
        print(f"   产品名称: {contract.execute('get', 'product_name')}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

    print("\n❌ 测试无效数据:")
    try:
        contract.execute("validated_set", "price", -10)  # 负价格
    except Exception as e:
        print(f"   负价格测试: {e}")

    try:
        contract.execute("validated_set", "active", "not_a_boolean")  # 类型错误
    except Exception as e:
        print(f"   类型错误测试: {e}")

    try:
        contract.execute("validated_set", "product_name", "")  # 空字符串
    except Exception as e:
        print(f"   空字符串测试: {e}")

    # 显示合约信息
    print("\n📊 合约信息:")
    info = contract.get_contract_info()
    for key, value in info.items():
        print(f"   {key}: {value}")

    print("\n💡 智能合约要点:")
    print("   • 代码一旦部署就不可修改（immutable）")
    print("   • 自动执行，无需中介")
    print("   • 可以包含复杂的业务逻辑和验证规则")
    print("   • 安全性至关重要，漏洞可能导致资金损失")


if __name__ == "__main__":
    main()