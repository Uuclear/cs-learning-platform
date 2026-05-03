#!/usr=" env python3"
# -*- coding: utf-8 -*-
"""
解决方案1：增强版响应式断点测试

这个解决方案扩展了基本的响应式测试功能，添加了更多特性。
"""

import json
from typing import Dict, List, Tuple, Optional


class AdvancedResponsiveTester:
    """高级响应式测试器"""

    def __init__(self):
        """初始化默认断点配置"""
        self.breakpoints = {
            "xs": 0,
            "sm": 480,
            "md": 768,
            "lg": 1024,
            "xl": 1200,
            "xxl": 1440
        }

    def add_custom_breakpoint(self, name: str, min_width: int) -> None:
        """添加自定义断点"""
        self.breakpoints[name] = min_width

    def get_active_breakpoints(self, width: int) -> List[str]:
        """获取在指定宽度下激活的所有断点"""
        active = []
        sorted_breakpoints = sorted(self.breakpoints.items(), key=lambda x: x[1])

        for name, min_width in sorted_breakpoints:
            if width >= min_width:
                active.append(name)

        return active

    def generate_flexbox_grid_examples(self) -> Dict[str, str]:
        """生成Flexbox和Grid布局示例"""
        examples = {}

        # Flexbox移动优先示例
        examples["flexbox_mobile_first"] = """
/* 移动优先的Flexbox布局 */
.flex-container {
    display: flex;
    flex-direction: column; /* 移动端垂直排列 */
    gap: 10px;
}

@media (min-width: 768px) {
    .flex-container {
        flex-direction: row; /* 平板及以上水平排列 */
        gap: 20px;
    }
}
"""

        # CSS Grid响应式示例
        examples["grid_responsive"] = """
/* 响应式CSS Grid */
.grid-container {
    display: grid;
    grid-template-columns: 1fr; /* 移动端单列 */
    gap: 10px;
}

@media (min-width: 768px) {
    .grid-container {
        grid-template-columns: repeat(2, 1fr); /* 平板双列 */
    }
}

@media (min-width: 1024px) {
    .grid-container {
        grid-template-columns: repeat(3, 1fr); /* 桌面三列 */
    }
}
"""

        return examples

    def test_viewport_meta_tag(self) -> str:
        """生成Viewport meta标签最佳实践"""
        return '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'


def main():
    tester = AdvancedResponsiveTester()

    # 测试不同宽度
    widths = [320, 768, 1024, 1920]

    print("🔍 高级响应式测试结果:")
    for width in widths:
        active = tester.get_active_breakpoints(width)
        print(f"{width}px -> 激活断点: {', '.join(active)}")

    print("\n📋 布局示例:")
    examples = tester.generate_flexbox_grid_examples()
    for name, code in examples.items():
        print(f"\n{name}:")
        print(code)


if __name__ == "__main__":
    main()