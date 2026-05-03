#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：Wasm 模块加载器完整实现

这是 example-03-wasm-module-loader.py 的完整解决方案。
包含了完整的模块验证、实例化和函数调用逻辑。
"""

from typing import Dict, Any, Callable

class WasmModule:
    def __init__(self, module_data: Dict[str, Any]):
        self.imports = module_data.get("imports", [])
        self.exports = module_data.get("exports", {})
        self.functions = module_data.get("functions", {})

    def validate_imports(self, import_objects: Dict[str, Any]) -> bool:
        for import_req in self.imports:
            module_name = import_req["module"]
            field_name = import_req["name"]

            if module_name not in import_objects:
                return False

            module_obj = import_objects[module_name]
            if field_name not in module_obj:
                return False

            actual_value = module_obj[field_name]
            expected_type = import_req["type"]

            if expected_type == "func" and not callable(actual_value):
                return False

        return True

    def instantiate(self, import_objects: Dict[str, Any]) -> 'WasmInstance':
        if not self.validate_imports(import_objects):
            raise RuntimeError("导入验证失败")
        return WasmInstance(self, import_objects)

class WasmInstance:
    def __init__(self, module: WasmModule, import_objects: Dict[str, Any]):
        self.module = module
        self.imports = import_objects
        self.exports = {}
        self._setup_exports()

    def _setup_exports(self):
        for export_name, export_info in self.module.exports.items():
            if export_info["type"] == "func":
                func_name = export_info["name"]
                if func_name in self.module.functions:
                    self.exports[export_name] = self._create_wrapped_function(func_name)

    def _create_wrapped_function(self, func_name: str) -> Callable:
        def wrapped_function(*args):
            return self._execute_function(func_name, args)
        return wrapped_function

    def _execute_function(self, func_name: str, args: tuple) -> Any:
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
        else:
            return sum(args) if args else 0

def create_math_module() -> Dict[str, Any]:
    return {
        "imports": [],
        "exports": {
            "add": {"type": "func", "name": "add"},
            "multiply": {"type": "func", "name": "multiply"},
            "fibonacci": {"type": "func", "name": "fibonacci"}
        },
        "functions": {
            "add": {"params": ["i32", "i32"], "returns": ["i32"]},
            "multiply": {"params": ["i32", "i32"], "returns": ["i32"]},
            "fibonacci": {"params": ["i32"], "returns": ["i32"]}
        }
    }

def main():
    # 创建并测试模块
    module_data = create_math_module()
    wasm_module = WasmModule(module_data)
    instance = wasm_module.instantiate({})

    assert instance.exports["add"](5, 3) == 8
    assert instance.exports["multiply"](4, 6) == 24
    assert instance.exports["fibonacci"](8) == 21

    print("✓ Wasm 模块加载器测试通过！")

if __name__ == "__main__":
    main()