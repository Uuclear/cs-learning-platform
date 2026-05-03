#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：完整的PWA实现

这个解决方案提供了完整的PWA实现，包括Service Worker和Manifest。
"""

import json
from typing import Dict, List, Optional


class CompletePWABuilder:
    """完整PWA构建器"""

    def __init__(self, app_name: str, start_url: str = "/"):
        """初始化PWA配置"""
        self.app_name = app_name
        self.start_url = start_url
        self.manifest_config = {
            "name": app_name,
            "short_name": app_name[:12],
            "description": f"{app_name} - 渐进式Web应用",
            "start_url": start_url,
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#1976d2",
            "orientation": "portrait",
            "scope": "/",
            "lang": "zh-CN",
            "icons": []
        }

    def generate_service_worker(self) -> str:
        """生成Service Worker代码"""
        service_worker_code = """
// Service Worker for PWA
const CACHE_NAME = 'pwa-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/styles/main.css',
  '/scripts/main.js',
  '/images/icon-192.png',
  '/images/icon-512.png'
];

// 安装阶段
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// 获取资源阶段
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // 如果缓存中有，返回缓存的资源
        if (response) {
          return response;
        }
        // 否则从网络获取
        return fetch(event.request);
      }
    )
  );
});

// 激活阶段（清理旧缓存）
self.addEventListener('activate', (event) => {
  const cacheWhitelist = ['pwa-cache-v1'];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
"""
        return service_worker_code.strip()

    def generate_manifest_with_icons(self, icon_sizes: List[str]) -> str:
        """生成包含图标的Manifest"""
        # 添加图标
        for size in icon_sizes:
            self.manifest_config["icons"].append({
                "src": f"/icons/icon-{size}.png",
                "sizes": f"{size}x{size}",
                "type": "image/png"
            })

        return json.dumps(self.manifest_config, indent=2, ensure_ascii=False)

    def generate_html_integration(self) -> str:
        """生成HTML集成代码"""
        html_integration = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.app_name}</title>

    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">

    <!-- 主题颜色 -->
    <meta name="theme-color" content="#1976d2">

    <!-- iOS Safari -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <link rel="apple-touch-icon" href="/icons/icon-192.png">
</head>
<body>
    <h1>{self.app_name}</h1>
    <p>这是一个PWA应用！</p>

    <script>
        // 注册Service Worker
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('/sw.js')
                    .then((registration) => {{
                        console.log('SW registered: ', registration);
                    }})
                    .catch((registrationError) => {{
                        console.log('SW registration failed: ', registrationError);
                    }});
            }});
        }}
    </script>
</body>
</html>
"""
        return html_integration


def main():
    """主函数：演示完整PWA构建"""
    builder = CompletePWABuilder("移动端开发学习应用")

    print("🚀 完整PWA实现方案")
    print("=" * 50)

    print("\n📋 Service Worker代码:")
    print(builder.generate_service_worker())

    print("\n📋 Web Manifest (包含图标):")
    manifest = builder.generate_manifest_with_icons(["192", "512"])
    print(manifest)

    print("\n📋 HTML集成代码:")
    html = builder.generate_html_integration()
    print(html)


if __name__ == "__main__":
    main()