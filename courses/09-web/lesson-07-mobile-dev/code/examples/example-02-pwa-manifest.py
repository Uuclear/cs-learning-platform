#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：PWA Web Manifest生成器

这个脚本从Python配置生成有效的PWA Web Manifest JSON文件。
Web Manifest是PWA的核心文件，定义了应用的元数据和行为。
"""

import json
from typing import Dict, List, Optional


class PWAManifestGenerator:
    """PWA Web Manifest生成器类"""

    def __init__(self):
        """初始化默认配置"""
        self.config = {
            "name": "我的PWA应用",
            "short_name": "PWA",
            "description": "一个渐进式Web应用示例",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#000000",
            "orientation": "portrait",
            "scope": "/",
            "lang": "zh-CN"
        }

    def set_basic_info(self, name: str, short_name: str, description: str) -> None:
        """
        设置基本应用信息

        :param name: 应用全名
        :param short_name: 应用简称（最多12个字符）
        :param description: 应用描述
        """
        self.config["name"] = name
        self.config["short_name"] = short_name[:12]  # 限制长度
        self.config["description"] = description

    def set_colors(self, background_color: str, theme_color: str) -> None:
        """
        设置应用颜色

        :param background_color: 启动画面背景色
        :param theme_color: 主题色（状态栏颜色）
        """
        self.config["background_color"] = background_color
        self.config["theme_color"] = theme_color

    def add_icon(self, src: str, sizes: str, type_: str = "image/png") -> None:
        """
        添加应用图标

        :param src: 图标文件路径
        :param sizes: 图标尺寸（如"192x192"）
        :param type_: MIME类型
        """
        if "icons" not in self.config:
            self.config["icons"] = []

        icon_entry = {
            "src": src,
            "sizes": sizes,
            "type": type_
        }
        self.config["icons"].append(icon_entry)

    def set_display_mode(self, display: str, orientation: Optional[str] = None) -> None:
        """
        设置显示模式

        :param display: 显示模式（fullscreen, standalone, minimal-ui, browser）
        :param orientation: 屏幕方向（portrait, landscape等）
        """
        valid_displays = ["fullscreen", "standalone", "minimal-ui", "browser"]
        if display not in valid_displays:
            raise ValueError(f"display必须是以下之一: {valid_displays}")

        self.config["display"] = display
        if orientation:
            self.config["orientation"] = orientation

    def generate_manifest(self) -> str:
        """
        生成Web Manifest JSON字符串

        :return: 格式化的JSON字符串
        """
        return json.dumps(self.config, indent=2, ensure_ascii=False)

    def save_to_file(self, filename: str = "manifest.json") -> None:
        """
        保存Manifest到文件

        :param filename: 输出文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_manifest())


def main():
    """主函数：演示PWA Manifest生成"""
    print("🚀 PWA Web Manifest生成器")
    print("=" * 50)

    # 创建生成器实例
    generator = PWAManifestGenerator()

    # 配置基本信息
    generator.set_basic_info(
        name="移动端开发学习应用",
        short_name="移动开发",
        description="学习响应式设计和PWA技术的示例应用"
    )

    # 设置颜色
    generator.set_colors("#f5f5f5", "#1976d2")

    # 添加图标（多种尺寸）
    generator.add_icon("icons/icon-192.png", "192x192", "image/png")
    generator.add_icon("icons/icon-512.png", "512x512", "image/png")

    # 设置显示模式
    generator.set_display_mode("standalone", "portrait")

    # 生成并显示Manifest
    manifest_json = generator.generate_manifest()
    print("📋 生成的Web Manifest:")
    print(manifest_json)

    # 验证JSON有效性
    try:
        json.loads(manifest_json)
        print("\n✅ JSON格式有效！")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON格式错误: {e}")

    # 保存到文件（可选）
    # generator.save_to_file("manifest.json")
    # print("\n💾 已保存到 manifest.json")


if __name__ == "__main__":
    main()