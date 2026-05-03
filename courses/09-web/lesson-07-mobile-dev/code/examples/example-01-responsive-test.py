#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：响应式断点测试模拟器

这个脚本模拟不同设备宽度下的响应式断点测试。
它可以帮助开发者理解媒体查询如何在不同屏幕尺寸下工作。
"""

import json
from typing import Dict, List, Tuple


def simulate_responsive_breakpoints(device_widths: List[int]) -> Dict[str, str]:
    """
    模拟响应式断点测试

    :param device_widths: 设备宽度列表（像素）
    :return: 每个宽度对应的布局类别
    """
    results = {}

    for width in device_widths:
        if width < 480:
            # 超小屏幕 - 手机竖屏
            layout = "xs (超小屏幕)"
        elif width < 768:
            # 小屏幕 - 手机横屏/小型平板
            layout = "sm (小屏幕)"
        elif width < 1024:
            # 中等屏幕 - 平板/小型笔记本
            layout = "md (中等屏幕)"
        elif width < 1200:
            # 大屏幕 - 桌面显示器
            layout = "lg (大屏幕)"
        else:
            # 超大屏幕 - 大型显示器
            layout = "xl (超大屏幕)"

        results[f"{width}px"] = layout

    return results


def generate_media_queries_example() -> str:
    """
    生成CSS媒体查询示例代码

    :return: 媒体查询CSS代码字符串
    """
    css_template = """/* 移动优先的响应式设计 */
/* 基础样式 - 移动设备 */
.container {
    width: 100%;
    padding: 10px;
}

/* 小屏幕及以上 */
@media screen and (min-width: 480px) {
    .container {
        max-width: 480px;
    }
}

/* 中等屏幕及以上 */
@media screen and (min-width: 768px) {
    .container {
        max-width: 768px;
        display: flex;
    }
}

/* 大屏幕及以上 */
@media screen and (min-width: 1024px) {
    .container {
        max-width: 1024px;
        gap: 20px;
    }
}

/* 超大屏幕 */
@media screen and (min-width: 1200px) {
    .container {
        max-width: 1200px;
        padding: 20px;
    }
}"""

    return css_template


def main():
    """主函数：运行响应式测试演示"""
    # 测试常见设备宽度
    test_widths = [320, 375, 414, 480, 768, 1024, 1200, 1440, 1920]

    print("📱 响应式断点测试模拟器")
    print("=" * 50)

    # 获取布局分类结果
    results = simulate_responsive_breakpoints(test_widths)

    print("设备宽度 -> 布局类别:")
    for width, layout in results.items():
        print(f"  {width:<8} -> {layout}")

    print("\n" + "=" * 50)
    print("📋 对应的CSS媒体查询示例:")
    print(generate_media_queries_example())

    # 输出JSON格式结果（可用于其他工具）
    print("\n" + "=" * 50)
    print("📄 JSON格式输出:")
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()