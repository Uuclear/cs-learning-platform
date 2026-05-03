#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：WebAssembly 模块加载器模拟器

这个示例模拟了 WebAssembly 模块的加载和实例化过程。
包括以下步骤：
1. 解析模块的导入需求
2. 验证类型签名
3. 链接外部函数
4. 实例化模块
5. 执行导出的函数
"""

from typing import Dict, List, Callable, Any
import json

class WasmModule:
    """WebAssembly 模块表示"""

    def __init__(self, module_data: Dict[str, Any]):
        """
        初始化 Wasm 模块

        :param module_data: 包含模块信息的字典，包含 imports, exports, functions 等
        """
        self.imports = module_data.get("imports", [])
        self.exports = module_data.get("exports", {})
        self.functions = module_data.get("functions", {})
        self.memory = module_data.get("memory", {"initial": 1, "maximum": 16})
        self.tables = module_data.get("tables", [])

    def validate_imports(self, import_objects: Dict[str, Any]) -> bool:
        """
        验证导入对象是否满足模块需求

        :param import_objects: 提供的导入对象
        :return: 验证是否通过
        """
        print("验证模块导入需求...")

        for import_req in self.imports:
            module_name = import_req["module"]
            field_name = import_req["name"]
            expected_type = import_req["type"]

            # 检查导入对象是否存在
            if module_name not in import_objects:
                print(f"  ✗ 缺少导入模块: {module_name}")
                return False

            module_obj = import_objects[module_name]
            if field_name not in module_obj:
                print(f"  ✗ 导入模块 {module_name} 中缺少字段: {field_name}")
                return False

            actual_value = module_obj[field_name]
            actual_type = type(actual_value).__name__

            # 简单的类型检查（实际 Wasm 有更复杂的类型系统）
            if expected_type == "func" and not callable(actual_value):
                print(f"  ✗ 字段 {field_name} 应该是函数，但实际是 {actual_type}")
                return False
            elif expected_type == "memory" and not hasattr(actual_value, 'buffer'):
                print(f"  ✗ 字段 {field_name} 应该是内存对象")
                return False

            print(f"  ✓ 导入 {module_name}.{field_name} 验证通过")

        return True

    def instantiate(self, import_objects: Dict[str, Any]) -> 'WasmInstance':
        """
        实例化模块

        :param import_objects: 导入对象
        :return: Wasm 实例
        """
        if not self.validate_imports(import_objects):
            raise RuntimeError("模块导入验证失败")

        print("创建 Wasm 实例...")
        return WasmInstance(self, import_objects)

class WasmInstance:
    """WebAssembly 实例"""

    def __init__(self, module: WasmModule, import_objects: Dict[str, Any]):
        """
        初始化 Wasm 实例

        :param module: Wasm 模块
        :param import_objects: 导入对象
        """
        self.module = module
        self.imports = import_objects
        self.exports = {}
        self._setup_exports()

    def _setup_exports(self):
        """设置导出的函数和对象"""
        print("设置导出项...")

        for export_name, export_info in self.module.exports.items():
            if export_info["type"] == "func":
                func_name = export_info["name"]
                if func_name in self.module.functions:
                    # 创建包装函数
                    wrapped_func = self._create_wrapped_function(func_name)
                    self.exports[export_name] = wrapped_func
                    print(f"  ✓ 导出函数: {export_name}")
                else:
                    print(f"  ✗ 函数 {func_name} 未在模块中定义")
            elif export_info["type"] == "memory":
                # 模拟内存导出
                self.exports[export_name] = {"buffer": bytearray(65536)}  # 64KB 内存
                print(f"  ✓ 导出内存: {export_name}")

    def _create_wrapped_function(self, func_name: str) -> Callable:
        """
        创建包装函数，处理参数转换和调用

        :param func_name: 函数名称
        :return: 包装后的函数
        """
        def wrapped_function(*args):
            print(f"调用 Wasm 函数: {func_name}({args})")

            # 获取函数定义
            func_def = self.module.functions[func_name]
            expected_params = func_def.get("params", [])
            expected_returns = func_def.get("returns", [])

            # 参数验证（简化版）
            if len(args) != len(expected_params):
                raise ValueError(f"函数 {func_name} 期望 {len(expected_params)} 个参数，但提供了 {len(args)} 个")

            # 模拟函数执行
            result = self._execute_function(func_name, args)
            print(f"函数 {func_name} 返回: {result}")
            return result

        return wrapped_function

    def _execute_function(self, func_name: str, args: tuple) -> Any:
        """
        模拟函数执行（实际 Wasm 会执行字节码）

        :param func_name: 函数名称
        :param args: 参数
        :return: 执行结果
        """
        # 这里根据函数名模拟不同的行为
        if func_name == "add":
            return args[0] + args[1]
        elif func_name == "multiply":
            return args[0] * args[1]
        elif func_name == "fibonacci":
            n = args[0]
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
        elif func_name == "console_log":
            print(f"Wasm console.log: {args[0]}")
            return None
        else:
            # 默认返回参数之和作为示例
            return sum(args) if args else 0

def create_sample_module() -> Dict[str, Any]:
    """创建示例 Wasm 模块数据"""
    return {
        "imports": [
            {
                "module": "env",
                "name": "console_log",
                "type": "func"
            }
        ],
        "exports": {
            "add": {"type": "func", "name": "add"},
            "multiply": {"type": "func", "name": "multiply"},
            "fibonacci": {"type": "func", "name": "fibonacci"},
            "memory": {"type": "memory", "name": "memory"}
        },
        "functions": {
            "add": {"params": ["i32", "i32"], "returns": ["i32"]},
            "multiply": {"params": ["i32", "i32"], "returns": ["i32"]},
            "fibonacci": {"params": ["i32"], "returns": ["i32"]},
            "console_log": {"params": ["string"], "returns": []}
        },
        "memory": {"initial": 1, "maximum": 16}
    }

def main():
    """演示 Wasm 模块加载过程"""
    print("=== WebAssembly 模块加载器模拟器 ===")
    print()

    # 创建示例模块
    module_data = create_sample_module()
    wasm_module = WasmModule(module_data)

    # 定义导入对象
    import_objects = {
        "env": {
            "console_log": lambda msg: print(f"JavaScript console.log: {msg}")
        }
    }

    try:
        # 实例化模块
        instance = wasm_module.instantiate(import_objects)
        print("\n=== 测试导出的函数 ===")

        # 调用导出的函数
        result1 = instance.exports["add"](10, 20)
        print(f"add(10, 20) = {result1}")

        result2 = instance.exports["multiply"](5, 6)
        print(f"multiply(5, 6) = {result2}")

        result3 = instance.exports["fibonacci"](10)
        print(f"fibonacci(10) = {result3}")

        # 调用内部函数来演示导入函数的使用
        # 注意：console_log 是导入的，不是导出的，所以不能通过 exports 调用
        # 这里我们直接调用 _execute_function 来演示
        instance._execute_function("console_log", ("Hello from WebAssembly!",))

        # 访问导出的内存
        memory = instance.exports["memory"]
        print(f"导出的内存大小: {len(memory['buffer'])} 字节")

        print("\n✓ Wasm 模块加载和执行成功！")

    except Exception as e:
        print(f"✗ 模块加载失败: {e}")

if __name__ == "__main__":
    main()