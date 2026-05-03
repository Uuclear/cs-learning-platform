#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 JavaScript 模块打包器 (Bundler Simulation)

这个脚本模拟了前端构建工具中的模块打包过程：
1. 解析模块依赖关系
2. 递归解析所有导入的模块
3. 将所有模块代码合并成一个单独的输出文件

这展示了 Webpack、Vite 等工具的核心功能之一。
"""

import os
import json
from typing import Dict, List, Set


class ModuleBundler:
    """模块打包器类，模拟前端构建工具的打包过程"""

    def __init__(self):
        self.modules: Dict[str, str] = {}  # 存储模块内容 {文件路径: 文件内容}
        self.dependencies: Dict[str, List[str]] = {}  # 存储依赖关系 {文件路径: [依赖列表]}
        self.visited: Set[str] = set()  # 避免循环依赖

    def add_module(self, file_path: str, content: str):
        """添加模块到打包器中"""
        self.modules[file_path] = content
        # 简单解析 import 语句（模拟）
        self.dependencies[file_path] = self._parse_imports(content)

    def _parse_imports(self, content: str) -> List[str]:
        """解析模块中的 import 语句（简化版）"""
        imports = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('import ') and ' from ' in line:
                # 提取导入的模块路径
                parts = line.split(' from ')
                if len(parts) == 2:
                    module_path = parts[1].strip().strip("';\"")
                    # 假设所有模块都在当前目录下
                    if not module_path.startswith('.'):
                        module_path = f'./{module_path}'
                    if module_path.endswith('.js'):
                        imports.append(module_path)
                    else:
                        imports.append(f'{module_path}.js')
        return imports

    def bundle(self, entry_point: str) -> str:
        """从入口文件开始打包所有依赖模块"""
        if entry_point not in self.modules:
            raise FileNotFoundError(f"入口文件 {entry_point} 未找到")

        self.visited.clear()
        bundled_code = self._recursive_bundle(entry_point)
        return bundled_code

    def _recursive_bundle(self, file_path: str) -> str:
        """递归打包模块及其依赖"""
        if file_path in self.visited:
            return "// 循环依赖已跳过\n"

        self.visited.add(file_path)
        content = self.modules[file_path]

        # 递归处理所有依赖
        bundled_content = f"\n// === 模块: {file_path} ===\n"
        bundled_content += content + "\n"

        for dep in self.dependencies.get(file_path, []):
            if dep in self.modules:
                bundled_content += self._recursive_bundle(dep)
            else:
                bundled_content += f"\n// 警告: 依赖模块 {dep} 未找到\n"

        return bundled_content


def main():
    """主函数：演示模块打包过程"""
    print("=== 前端模块打包器模拟演示 ===\n")

    # 创建模拟的模块文件
    modules_data = {
        './main.js': '''
import { greet } from './utils.js';
import { calculate } from './math.js';

console.log(greet('世界'));
console.log('计算结果:', calculate(5, 3));
''',
        './utils.js': '''
export function greet(name) {
    return `你好, ${name}!`;
}

export function formatDate(date) {
    return date.toISOString();
}
''',
        './math.js': '''
import { helper } from './helper.js';

export function calculate(a, b) {
    return helper(a, b);
}

// 这个函数不会被使用（用于演示 tree-shaking）
export function unusedFunction() {
    console.log('这个函数永远不会被调用');
}
''',
        './helper.js': '''
export function helper(x, y) {
    return x * y + x - y;
}
'''
    }

    # 初始化打包器
    bundler = ModuleBundler()

    # 添加所有模块
    for file_path, content in modules_data.items():
        bundler.add_module(file_path, content)
        print(f"✓ 添加模块: {file_path}")

    print("\n--- 开始打包 ---")

    # 执行打包
    try:
        result = bundler.bundle('./main.js')
        print("\n=== 打包结果 ===")
        print(result)
        print("\n=== 打包完成 ===")
        print(f"总共打包了 {len(bundler.visited)} 个模块")
    except Exception as e:
        print(f"打包失败: {e}")


if __name__ == "__main__":
    main()