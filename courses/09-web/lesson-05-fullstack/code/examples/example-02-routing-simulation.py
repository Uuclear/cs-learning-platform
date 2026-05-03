#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：文件系统路由模拟
模拟Next.js风格的文件系统路由机制
"""

import os
import re
from typing import Dict, List, Optional, Tuple

class FileSystemRouter:
    """文件系统路由模拟器"""

    def __init__(self, base_path: str = "pages"):
        """
        初始化路由器
        :param base_path: 页面目录路径
        """
        self.base_path = base_path
        self.routes = {}
        self.dynamic_routes = []
        self.catch_all_routes = []

    def discover_routes(self):
        """发现并注册所有路由"""
        if not os.path.exists(self.base_path):
            print(f"⚠️  路径 {self.base_path} 不存在，创建示例结构...")
            self._create_example_structure()

        self._scan_directory(self.base_path, "")

    def _create_example_structure(self):
        """创建示例页面结构"""
        os.makedirs(self.base_path, exist_ok=True)

        # 创建静态页面
        static_pages = ["index.js", "about.js", "contact.js"]
        for page in static_pages:
            with open(os.path.join(self.base_path, page), "w") as f:
                f.write(f"// {page} - 静态页面\nexport default function Page() {{ return <div>{page.replace('.js', '')}</div>; }}")

        # 创建动态路由
        os.makedirs(os.path.join(self.base_path, "posts"), exist_ok=True)
        with open(os.path.join(self.base_path, "posts", "[id].js"), "w") as f:
            f.write("// [id].js - 动态路由\nexport default function Post({ id }) { return <div>Post {id}</div>; }")

        # 创建嵌套路由
        os.makedirs(os.path.join(self.base_path, "dashboard", "settings"), exist_ok=True)
        with open(os.path.join(self.base_path, "dashboard", "settings", "profile.js"), "w") as f:
            f.write("// profile.js - 嵌套路由\nexport default function Profile() { return <div>Profile Settings</div>; }")

        # 创建捕获所有路由
        with open(os.path.join(self.base_path, "[...slug].js"), "w") as f:
            f.write("// [...slug].js - 捕获所有路由\nexport default function CatchAll({ slug }) { return <div>Catch all: {slug}</div>; }")

    def _scan_directory(self, current_path: str, route_prefix: str):
        """递归扫描目录并注册路由"""
        if not os.path.exists(current_path):
            return

        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            route_path = f"{route_prefix}/{item}" if route_prefix else f"/{item}"

            if os.path.isfile(item_path) and item.endswith(('.js', '.jsx', '.ts', '.tsx')):
                # 处理文件路由
                route_name = item.rsplit('.', 1)[0]  # 移除扩展名

                if route_name == "index":
                    # index文件映射到父路径
                    actual_route = route_prefix if route_prefix else "/"
                elif route_name.startswith('[') and route_name.endswith(']'):
                    # 动态路由
                    if route_name.startswith('[...'):  # 捕获所有路由
                        param_name = route_name[4:-1]  # 移除 [... 和 ]
                        actual_route = f"{route_prefix}/[[...{param_name}]]"
                        self.catch_all_routes.append({
                            'route': actual_route,
                            'file': item_path,
                            'param': param_name
                        })
                    else:  # 普通动态路由
                        param_name = route_name[1:-1]  # 移除 [ 和 ]
                        actual_route = f"{route_prefix}/[{param_name}]"
                        self.dynamic_routes.append({
                            'route': actual_route,
                            'file': item_path,
                            'param': param_name
                        })
                else:
                    # 静态路由
                    actual_route = f"{route_prefix}/{route_name}" if route_prefix else f"/{route_name}"

                self.routes[actual_route] = item_path
                print(f"✅ 注册路由: {actual_route} -> {item_path}")

            elif os.path.isdir(item_path):
                # 递归处理子目录
                self._scan_directory(item_path, route_path.rstrip('/'))

    def match_route(self, path: str) -> Optional[Dict]:
        """
        匹配给定路径到对应的路由
        :param path: 请求路径
        :return: 路由信息字典或None
        """
        # 标准化路径
        path = path.rstrip('/') if path != '/' else path

        # 1. 首先检查精确匹配（静态路由）
        if path in self.routes:
            return {
                'type': 'static',
                'route': path,
                'file': self.routes[path],
                'params': {}
            }

        # 2. 检查动态路由
        for dynamic_route in self.dynamic_routes:
            route_pattern = dynamic_route['route']
            param_name = dynamic_route['param']

            # 将路由模式转换为正则表达式
            pattern = route_pattern.replace(f'[{param_name}]', r'([^/]+)')
            pattern = f"^{pattern}$"

            match = re.match(pattern, path)
            if match:
                return {
                    'type': 'dynamic',
                    'route': route_pattern,
                    'file': dynamic_route['file'],
                    'params': {param_name: match.group(1)}
                }

        # 3. 检查捕获所有路由
        for catch_all_route in self.catch_all_routes:
            route_pattern = catch_all_route['route']
            param_name = catch_all_route['param']

            # 捕获所有路由匹配任何剩余路径
            base_path = route_pattern.split('[[...')[0]
            if path.startswith(base_path) and len(path) > len(base_path):
                slug_value = path[len(base_path)+1:] if base_path else path[1:]
                return {
                    'type': 'catch-all',
                    'route': route_pattern,
                    'file': catch_all_route['file'],
                    'params': {param_name: slug_value.split('/')}
                }

        return None

    def get_all_routes(self) -> List[str]:
        """获取所有已注册的路由"""
        all_routes = list(self.routes.keys())
        all_routes.extend([r['route'] for r in self.dynamic_routes])
        all_routes.extend([r['route'] for r in self.catch_all_routes])
        return sorted(all_routes)

def demonstrate_routing():
    """演示文件系统路由功能"""
    print("=" * 60)
    print("Next.js 文件系统路由模拟")
    print("=" * 60)

    # 创建路由器并发现路由
    router = FileSystemRouter("pages")
    router.discover_routes()

    print(f"\n🔍 发现的路由 ({len(router.get_all_routes())} 个):")
    for route in router.get_all_routes():
        print(f"  • {route}")

    # 测试路由匹配
    test_paths = [
        "/",
        "/about",
        "/posts/123",
        "/dashboard/settings/profile",
        "/blog/tech/javascript",
        "/nonexistent"
    ]

    print(f"\n🎯 路由匹配测试:")
    for path in test_paths:
        result = router.match_route(path)
        if result:
            print(f"  ✓ {path} -> {result['type']} 路由")
            if result['params']:
                print(f"      参数: {result['params']}")
        else:
            print(f"  ✗ {path} -> 未找到匹配路由")

    # 清理示例文件
    import shutil
    if os.path.exists("pages"):
        shutil.rmtree("pages")
        print(f"\n🧹 清理临时文件")

if __name__ == "__main__":
    demonstrate_routing()