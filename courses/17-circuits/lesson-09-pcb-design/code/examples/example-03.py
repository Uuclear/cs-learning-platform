#!/usr/bin/env python3
"""
Simple PCB Layout Grid Generator
简易PCB布局网格生成器
"""

from typing import List, Tuple


class PCBGrid:
    """PCB布局网格类"""

    def __init__(self, width: int, height: int, grid_size: float = 2.54):
        """
        初始化PCB网格

        Args:
            width: 网格宽度（格子数）
            height: 网格高度（格子数）
            grid_size: 网格间距（毫米），默认2.54mm（0.1英寸）
        """
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.grid = [['.' for _ in range(width)] for _ in range(height)]

    def place_component(self, x: int, y: int, label: str = 'X'):
        """
        在指定位置放置元件

        Args:
            x: X坐标（格子索引）
            y: Y坐标（格子索引）
            label: 元件标签
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = label
        else:
            raise ValueError(f"位置 ({x}, {y}) 超出网格范围")

    def draw_trace(self, start: Tuple[int, int], end: Tuple[int, int], label: str = '-'):
        """
        绘制走线（简单直线）

        Args:
            start: 起始位置 (x, y)
            end: 结束位置 (x, y)
            label: 走线标签
        """
        x1, y1 = start
        x2, y2 = end

        # 简单的直线绘制（仅支持水平和垂直线）
        if x1 == x2:  # 垂直线
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.grid[y][x1] == '.':
                    self.grid[y][x1] = label
        elif y1 == y2:  # 水平线
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.grid[y1][x] == '.':
                    self.grid[y1][x] = label
        else:
            # 对角线或其他复杂走线需要更复杂的算法
            print(f"警告: 不支持对角线走线从 {start} 到 {end}")

    def get_physical_position(self, x: int, y: int) -> Tuple[float, float]:
        """
        获取格子的物理位置（毫米）

        Args:
            x: X坐标（格子索引）
            y: Y坐标（格子索引）

        Returns:
            (x_mm, y_mm) 物理坐标
        """
        return (x * self.grid_size, y * self.grid_size)

    def display(self):
        """显示网格"""
        print(f"PCB布局网格 ({self.width}×{self.height}, 间距{self.grid_size}mm):")
        print("+" + "-" * (self.width * 2 + 1) + "+")
        for row in reversed(self.grid):  # Y轴翻转，使(0,0)在左下角
            print("| " + " ".join(row) + " |")
        print("+" + "-" * (self.width * 2 + 1) + "+")


def main():
    """主函数，演示PCB网格生成"""
    print("=== 简易PCB布局网格生成器 ===")
    print()

    # 创建一个10x8的网格
    pcb = PCBGrid(10, 8)

    # 放置一些元件
    pcb.place_component(2, 2, 'R1')  # 电阻
    pcb.place_component(5, 4, 'IC')  # IC
    pcb.place_component(8, 6, 'LED')  # LED
    pcb.place_component(1, 6, 'PWR')  # 电源

    # 绘制一些走线
    pcb.draw_trace((2, 2), (5, 2))  # R1到IC的水平连接
    pcb.draw_trace((5, 2), (5, 4))  # 垂直连接到IC
    pcb.draw_trace((5, 4), (8, 4))  # IC到LED的水平连接
    pcb.draw_trace((8, 4), (8, 6))  # 垂直连接到LED

    # 显示布局
    pcb.display()

    print()
    # 显示物理坐标
    print("元件物理位置:")
    components = [(2, 2, 'R1'), (5, 4, 'IC'), (8, 6, 'LED'), (1, 6, 'PWR')]
    for x, y, name in components:
        x_mm, y_mm = pcb.get_physical_position(x, y)
        print(f"  {name}: ({x_mm:.1f}mm, {y_mm:.1f}mm)")


if __name__ == "__main__":
    main()