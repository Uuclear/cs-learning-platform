#!/usr/bin/env python3
"""
Simple PCB Layout Grid Generator - Solution
简易PCB布局网格生成器（完整解决方案）
"""

from typing import List, Tuple, Optional
import math


class AdvancedPCBGrid:
    """高级PCB布局网格类"""

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
        self.components = {}  # 存储元件信息
        self.traces = []      # 存储走线信息

    def place_component(self, x: int, y: int, label: str, component_type: str = 'unknown'):
        """
        在指定位置放置元件

        Args:
            x: X坐标（格子索引）
            y: Y坐标（格子索引）
            label: 元件标签
            component_type: 元件类型
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"位置 ({x}, {y}) 超出网格范围 (0-{self.width-1}, 0-{self.height-1})")

        self.grid[y][x] = label[0] if len(label) == 1 else 'C'  # 单字符显示
        self.components[label] = {
            'position': (x, y),
            'type': component_type,
            'label': label
        }

    def draw_trace(self, start: Tuple[int, int], end: Tuple[int, int],
                   label: str = '-', trace_width: int = 1):
        """
        绘制走线（支持简单路径规划）

        Args:
            start: 起始位置 (x, y)
            end: 结束位置 (x, y)
            label: 走线标签
            trace_width: 走线宽度（格子数）
        """
        x1, y1 = start
        x2, y2 = end

        if not self._is_valid_position(x1, y1) or not self._is_valid_position(x2, y2):
            raise ValueError("走线位置超出网格范围")

        # 使用简单的L型路径（先水平后垂直，或先垂直后水平）
        path = self._generate_l_path(start, end)

        for x, y in path:
            if self.grid[y][x] == '.':
                self.grid[y][x] = label

        self.traces.append({
            'start': start,
            'end': end,
            'path': path,
            'label': label,
            'width': trace_width
        })

    def _generate_l_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """生成L型路径"""
        x1, y1 = start
        x2, y2 = end

        path = []

        # 策略1：先水平后垂直
        mid_x, mid_y = x2, y1

        # 水平段
        step_x = 1 if x2 > x1 else -1
        for x in range(x1, x2 + step_x, step_x):
            path.append((x, y1))

        # 垂直段（跳过起点避免重复）
        step_y = 1 if y2 > y1 else -1
        for y in range(y1 + step_y, y2 + step_y, step_y):
            path.append((x2, y))

        return path

    def _is_valid_position(self, x: int, y: int) -> bool:
        """检查位置是否有效"""
        return 0 <= x < self.width and 0 <= y < self.height

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

    def calculate_trace_length(self, trace_index: int) -> float:
        """计算指定走线的物理长度（毫米）"""
        if trace_index >= len(self.traces):
            raise IndexError("走线索引超出范围")

        trace = self.traces[trace_index]
        path = trace['path']
        length_mm = (len(path) - 1) * self.grid_size
        return round(length_mm, 1)

    def display(self, show_coordinates: bool = False):
        """显示网格"""
        print(f"PCB布局网格 ({self.width}×{self.height}, 间距{self.grid_size}mm):")

        if show_coordinates:
            # 显示X坐标
            print("   ", end="")
            for x in range(self.width):
                print(f"{x%10} ", end="")
            print()

        print("+" + "-" * (self.width * 2 + 1) + "+")

        for y in range(self.height - 1, -1, -1):  # Y轴翻转
            if show_coordinates:
                print(f"{y} | ", end="")
            else:
                print("| ", end="")

            for x in range(self.width):
                print(f"{self.grid[y][x]} ", end="")

            if show_coordinates:
                print(f"| {y}")
            else:
                print("|")

        print("+" + "-" * (self.width * 2 + 1) + "+")

        # 显示元件列表
        if self.components:
            print("\n元件列表:")
            for label, info in self.components.items():
                x, y = info['position']
                x_mm, y_mm = self.get_physical_position(x, y)
                print(f"  {label} ({info['type']}): ({x_mm:.1f}mm, {y_mm:.1f}mm)")

        # 显示走线信息
        if self.traces:
            print("\n走线列表:")
            for i, trace in enumerate(self.traces):
                length = self.calculate_trace_length(i)
                print(f"  走线{i+1}: {trace['start']} → {trace['end']}, 长度: {length}mm")


def main():
    """主函数，完整的PCB网格生成演示"""
    print("=== 简易PCB布局网格生成器（完整版）===")
    print()

    # 创建一个12x10的网格
    pcb = AdvancedPCBGrid(12, 10)

    # 放置元件
    pcb.place_component(2, 2, 'R1', 'resistor')
    pcb.place_component(6, 5, 'U1', 'ic')
    pcb.place_component(10, 8, 'LED1', 'led')
    pcb.place_component(1, 8, 'J1', 'connector')
    pcb.place_component(6, 1, 'C1', 'capacitor')

    # 绘制走线
    pcb.draw_trace((2, 2), (6, 2))  # R1到U1
    pcb.draw_trace((6, 2), (6, 5))  # 到U1
    pcb.draw_trace((6, 5), (10, 5)) # U1到LED1
    pcb.draw_trace((10, 5), (10, 8)) # 到LED1
    pcb.draw_trace((1, 8), (6, 8))  # J1到U1区域
    pcb.draw_trace((6, 8), (6, 5))  # 到U1

    # 显示布局
    pcb.display(show_coordinates=True)

    print()
    print("设计统计:")
    print(f"  元件数量: {len(pcb.components)}")
    print(f"  走线数量: {len(pcb.traces)}")

    total_length = sum(pcb.calculate_trace_length(i) for i in range(len(pcb.traces)))
    print(f"  总走线长度: {total_length:.1f}mm")


if __name__ == "__main__":
    main()