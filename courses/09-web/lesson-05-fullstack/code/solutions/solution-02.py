#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：高级路由系统实现

这个解决方案展示了如何实现一个更完整的文件系统路由系统，
支持嵌套路由、布局、错误处理和API路由。
"""

import os
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path


class AdvancedRouter:
    """高级文件系统路由器"""

    def __init__(self, pages_dir: str = "pages"):
        self.pages_dir = pages_dir
        self.routes = {}
        self.api_routes = {}
        self.layout_routes = {}
        self.error_routes = {}
        self.middleware_routes = {}

    def scan_routes(self):
        """扫描并注册所有路由"""
        if not os.path.exists(self.pages_dir):
            self._create_example_structure()

        self._recursive_scan(self.pages_dir, "")

    def _create_example_structure(self):
        """创建示例页面结构"""
        os.makedirs(self.pages_dir, exist_ok=True)

        # 基础页面
        self._write_file("index.js", "// 首页\nexport default function Home() { return <div>首页</div>; }")
        self._write_file("about.js", "// 关于\nexport default function About() { return <div>关于我们</div>; }")

        # 嵌套路由
        os.makedirs(os.path.join(self.pages_dir, "dashboard"), exist_ok=True)
        self._write_file("dashboard/layout.js", "// 仪表板布局\nexport default function Layout({ children }) { return <div className=\"dashboard\">{children}</div>; }")
        self._write_file("dashboard/index.js", "// 仪表板首页\nexport default function Dashboard() { return <div>仪表板</div>; }")
        self._write_file("dashboard/settings.js", "// 设置页面\nexport default function Settings() { return <div>设置</div>; }")

        # 动态路由
        os.makedirs(os.path.join(self.pages_dir, "posts"), exist_ok=True)
        self._write_file("posts/[id].js", "// 文章详情\nexport default function Post({ id }) { return <div>文章 {id}</div>; }")

        # API路由
        os.makedirs(os.path.join(self.pages_dir, "api"), exist_ok=True)
        self._write_file("api/hello.js", "// API路由\nexport default function handler(req, res) { res.json({ message: 'Hello' }); }")
        os.makedirs(os.path.join(self.pages_dir, "api", "posts"), exist_ok=True)
        self._write_file("api/posts/[id].js", "// API - 获取文章\nexport default function handler(req, res) { const { id } = req.query; res.json({ id, title: `Post ${id}` }); }")

        # 错误页面
        self._write_file("_error.js", "// 错误页面\nexport default function Error({ statusCode }) { return <div>错误 {statusCode}</div>; }")

    def _write_file(self, path: str, content: str):
        """写入文件"""
        full_path = os.path.join(self.pages_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _recursive_scan(self, current_dir: str, route_prefix: str):
        """递归扫描目录"""
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            route_path = f"{route_prefix}/{item}" if route_prefix else f"/{item}"

            if os.path.isfile(item_path) and item.endswith(('.js', '.jsx', '.ts', '.tsx')):
                self._register_file_route(item_path, route_path, item)

            elif os.path.isdir(item_path):
                self._recursive_scan(item_path, route_path.rstrip('/'))

    def _register_file_route(self, file_path: str, route_path: str, filename: str):
        """注册文件路由"""
        name = filename.rsplit('.', 1)[0]
        dir_path = os.path.dirname(route_path)

        # 处理特殊文件
        if name == '_error':
            self.error_routes['default'] = file_path
            print(f"❌ 注册错误页面: {file_path}")
        elif name == 'layout':
            self.layout_routes[dir_path] = file_path
            print(f"🎨 注册布局: {dir_path} -> {file_path}")
        elif name.startswith('middleware'):
            self.middleware_routes[dir_path] = file_path
            print(f"🛡️  注册中间件: {dir_path} -> {file_path}")
        elif dir_path.endswith('/api'):
            # API路由
            api_route = route_path.replace('/api', '/api')
            self.api_routes[api_route] = file_path
            print(f"🔌 注册API路由: {api_route} -> {file_path}")
        elif name == 'index':
            # index文件映射到父路径
            actual_route = dir_path if dir_path != '/' else '/'
            self.routes[actual_route] = file_path
            print(f"📄 注册页面路由: {actual_route} -> {file_path}")
        elif name.startswith('[') and name.endswith(']'):
            # 动态路由
            param_name = name[1:-1]
            actual_route = f"{dir_path}/[{param_name}]"
            self.routes[actual_route] = file_path
            print(f"📁 注册动态路由: {actual_route} -> {file_path}")
        else:
            # 普通静态路由
            actual_route = f"{dir_path}/{name}" if dir_path != '/' else f"/{name}"
            self.routes[actual_route] = file_path
            print(f"📄 注册页面路由: {actual_route} -> {file_path}")

    def match_route(self, path: str, is_api: bool = False) -> Optional[Dict[str, Any]]:
        """匹配路由"""
        normalized_path = path.rstrip('/') if path != '/' else path

        if is_api:
            routes_dict = self.api_routes
            route_type = 'api'
        else:
            routes_dict = self.routes
            route_type = 'page'

        # 精确匹配
        if normalized_path in routes_dict:
            return self._create_route_result(route_type, normalized_path, routes_dict[normalized_path])

        # 动态路由匹配
        path_parts = normalized_path.strip('/').split('/') if normalized_path != '/' else []

        for route_pattern, file_path in routes_dict.items():
            if '[' in route_pattern and ']' in route_pattern:
                route_parts = route_pattern.strip('/').split('/') if route_pattern != '/' else []

                if len(path_parts) == len(route_parts):
                    params = {}
                    match = True

                    for i, (path_part, route_part) in enumerate(zip(path_parts, route_parts)):
                        if route_part.startswith('[') and route_part.endswith(']'):
                            param_name = route_part[1:-1]
                            # 处理捕获所有路由 [...param]
                            if param_name.startswith('...'):
                                param_name = param_name[3:]
                                params[param_name] = '/'.join(path_parts[i:])
                                break
                            else:
                                params[param_name] = path_part
                        elif path_part != route_part:
                            match = False
                            break

                    if match:
                        return self._create_route_result(route_type, route_pattern, file_path, params)

        # 找不到路由，返回错误页面
        if self.error_routes:
            return self._create_route_result('error', '404', self.error_routes['default'])

        return None

    def _create_route_result(self, route_type: str, route: str, file_path: str, params: Dict = None) -> Dict[str, Any]:
        """创建路由结果"""
        result = {
            'type': route_type,
            'route': route,
            'file': file_path,
            'params': params or {},
            'layout': self._find_layout(route),
            'middleware': self._find_middleware(route)
        }
        return result

    def _find_layout(self, route: str) -> Optional[str]:
        """查找布局文件"""
        current_path = route
        while current_path:
            if current_path in self.layout_routes:
                return self.layout_routes[current_path]
            current_path = '/'.join(current_path.split('/')[:-1]) or '/'
            if current_path == '/':
                break
        return None

    def _find_middleware(self, route: str) -> Optional[str]:
        """查找中间件"""
        current_path = route
        while current_path:
            if current_path in self.middleware_routes:
                return self.middleware_routes[current_path]
            current_path = '/'.join(current_path.split('/')[:-1]) or '/'
            if current_path == '/':
                break
        return None

    def get_route_tree(self) -> Dict:
        """获取路由树结构"""
        tree = {'pages': {}, 'api': {}}

        # 页面路由
        for route, file_path in self.routes.items():
            parts = route.strip('/').split('/') if route != '/' else ['index']
            current = tree['pages']

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                elif not isinstance(current[part], dict):
                    # 如果已经是一个字符串，转换为字典
                    current[part] = {'__duplicate__': current[part]}
                current = current[part]

            if parts[-1] in current and isinstance(current[parts[-1]], dict):
                current[parts[-1]]['__value__'] = 'page'
            else:
                current[parts[-1]] = 'page'

        # API路由
        for route, file_path in self.api_routes.items():
            api_route = route.replace('/api', '', 1) or '/'
            parts = api_route.strip('/').split('/') if api_route != '/' else ['index']
            current = tree['api']

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                elif not isinstance(current[part], dict):
                    current[part] = {'__duplicate__': current[part]}
                current = current[part]

            if parts[-1] in current and isinstance(current[parts[-1]], dict):
                current[parts[-1]]['__value__'] = 'api'
            else:
                current[parts[-1]] = 'api'

        return tree


def demonstrate_advanced_routing():
    """演示高级路由功能"""
    print("=" * 60)
    print("高级文件系统路由演示")
    print("=" * 60)

    router = AdvancedRouter("pages")
    router.scan_routes()

    print(f"\n🌳 路由树结构:")
    route_tree = router.get_route_tree()
    print(f"Pages: {route_tree['pages']}")
    print(f"API: {route_tree['api']}")

    # 测试路由匹配
    test_routes = [
        ("/", False),
        ("/about", False),
        ("/dashboard", False),
        ("/dashboard/settings", False),
        ("/posts/123", False),
        ("/api/hello", True),
        ("/api/posts/456", True),
        ("/nonexistent", False),
    ]

    print(f"\n🎯 路由匹配测试:")
    for path, is_api in test_routes:
        result = router.match_route(path, is_api)
        if result:
            print(f"  ✓ {path} ({'API' if is_api else 'Page'}):")
            print(f"      类型: {result['type']}")
            print(f"      文件: {os.path.relpath(result['file'], 'pages')}")
            if result['params']:
                print(f"      参数: {result['params']}")
            if result['layout']:
                print(f"      布局: {os.path.relpath(result['layout'], 'pages')}")
            if result['middleware']:
                print(f"      中间件: {os.path.relpath(result['middleware'], 'pages')}")
        else:
            print(f"  ✗ {path}: 未找到路由")

    # 清理
    import shutil
    if os.path.exists("pages"):
        shutil.rmtree("pages")
        print(f"\n🧹 清理临时文件")


if __name__ == "__main__":
    demonstrate_advanced_routing()