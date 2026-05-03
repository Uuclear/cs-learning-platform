#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：AR场景模拟
模拟简单的AR场景：检测平面、放置虚拟物体、计算遮挡
"""

import math
from typing import List, Tuple, Optional


class Plane:
    """平面类，用于表示检测到的水平或垂直平面"""

    def __init__(self, center: Tuple[float, float, float], normal: Tuple[float, float, float],
                 size: Tuple[float, float], plane_type: str = "horizontal"):
        """
        初始化平面
        :param center: 平面中心点 (x, y, z)
        :param normal: 平面法向量 (nx, ny, nz)
        :param size: 平面尺寸 (width, height)
        :param plane_type: 平面类型 ("horizontal" 或 "vertical")
        """
        self.center = center
        self.normal = normal
        self.size = size
        self.plane_type = plane_type

    def contains_point(self, point: Tuple[float, float, float], tolerance: float = 0.1) -> bool:
        """
        检查点是否在平面范围内（考虑容差）
        :param point: 要检查的点 (x, y, z)
        :param tolerance: 容差距离
        :return: 是否包含该点
        """
        # 计算点到平面的距离
        distance = abs(
            self.normal[0] * (point[0] - self.center[0]) +
            self.normal[1] * (point[1] - self.center[1]) +
            self.normal[2] * (point[2] - self.center[2])
        )

        if distance > tolerance:
            return False

        # 检查点是否在平面边界内（简化：假设平面与坐标轴对齐）
        if self.plane_type == "horizontal":
            # 水平平面（如地面、桌面）
            half_width, half_height = self.size[0]/2, self.size[1]/2
            dx = abs(point[0] - self.center[0])
            dz = abs(point[2] - self.center[2])
            return dx <= half_width and dz <= half_height
        else:
            # 垂直平面（如墙面）
            half_width, half_height = self.size[0]/2, self.size[1]/2
            dx = abs(point[0] - self.center[0])
            dy = abs(point[1] - self.center[1])
            return dx <= half_width and dy <= half_height

    def project_point(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        将点投影到平面上
        :param point: 原始点
        :return: 投影后的点
        """
        # 计算点到平面的向量
        to_point = (
            point[0] - self.center[0],
            point[1] - self.center[1],
            point[2] - self.center[2]
        )

        # 计算沿法向量的距离
        distance = (
            to_point[0] * self.normal[0] +
            to_point[1] * self.normal[1] +
            to_point[2] * self.normal[2]
        )

        # 投影点 = 原始点 - 距离 * 法向量
        projected = (
            point[0] - distance * self.normal[0],
            point[1] - distance * self.normal[1],
            point[2] - distance * self.normal[2]
        )

        return projected


class VirtualObject:
    """虚拟物体类"""

    def __init__(self, position: Tuple[float, float, float], size: Tuple[float, float, float],
                 object_type: str = "cube"):
        """
        初始化虚拟物体
        :param position: 物体位置 (x, y, z)
        :param size: 物体尺寸 (width, height, depth)
        :param object_type: 物体类型
        """
        self.position = position
        self.size = size
        self.object_type = object_type

    def get_bounding_box(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """
        获取包围盒（最小和最大坐标）
        :return: ((min_x, min_y, min_z), (max_x, max_y, max_z))
        """
        half_w, half_h, half_d = self.size[0]/2, self.size[1]/2, self.size[2]/2
        min_coords = (
            self.position[0] - half_w,
            self.position[1] - half_h,
            self.position[2] - half_d
        )
        max_coords = (
            self.position[0] + half_w,
            self.position[1] + half_h,
            self.position[2] + half_d
        )
        return min_coords, max_coords

    def is_visible_from(self, camera_pos: Tuple[float, float, float]) -> bool:
        """
        检查物体从相机位置是否可见（简化版）
        :param camera_pos: 相机位置
        :return: 是否可见
        """
        # 简化：假设没有遮挡物，总是可见
        # 在实际AR系统中，这会涉及复杂的光线追踪和遮挡检测
        return True


class ARScene:
    """AR场景管理器"""

    def __init__(self):
        """初始化AR场景"""
        self.detected_planes: List[Plane] = []
        self.virtual_objects: List[VirtualObject] = []

    def detect_planes(self, scan_data: List[Tuple[float, float, float]]) -> List[Plane]:
        """
        模拟平面检测（基于扫描数据）
        :param scan_data: 扫描点云数据
        :return: 检测到的平面列表
        """
        # 简化实现：假设我们知道主要平面
        planes = []

        # 检测水平平面（地面）
        ground_plane = Plane(
            center=(0.0, 0.0, 0.0),
            normal=(0.0, 1.0, 0.0),
            size=(5.0, 5.0),
            plane_type="horizontal"
        )
        planes.append(ground_plane)

        # 检测垂直平面（墙面）
        wall_plane = Plane(
            center=(2.5, 1.5, 0.0),
            normal=(1.0, 0.0, 0.0),
            size=(3.0, 3.0),
            plane_type="vertical"
        )
        planes.append(wall_plane)

        self.detected_planes = planes
        return planes

    def place_object_on_plane(self, plane_index: int, offset: Tuple[float, float, float]) -> Optional[VirtualObject]:
        """
        在指定平面上放置虚拟物体
        :param plane_index: 平面索引
        :param offset: 相对于平面中心的偏移
        :return: 创建的虚拟物体，如果失败则返回None
        """
        if plane_index >= len(self.detected_planes):
            print("错误：平面索引超出范围")
            return None

        plane = self.detected_planes[plane_index]
        target_pos = (
            plane.center[0] + offset[0],
            plane.center[1] + offset[1],
            plane.center[2] + offset[2]
        )

        # 将目标位置投影到平面上以确保精确对齐
        final_pos = plane.project_point(target_pos)

        # 创建虚拟物体
        virtual_obj = VirtualObject(
            position=final_pos,
            size=(0.5, 0.5, 0.5),
            object_type="cube"
        )

        self.virtual_objects.append(virtual_obj)
        return virtual_obj

    def calculate_occlusion(self, camera_pos: Tuple[float, float, float]) -> List[bool]:
        """
        计算遮挡情况（简化版）
        :param camera_pos: 相机位置
        :return: 每个物体的可见性列表
        """
        visibility = []
        for obj in self.virtual_objects:
            visible = obj.is_visible_from(camera_pos)
            visibility.append(visible)
        return visibility


def simulate_ar_scene():
    """模拟AR场景"""
    print("=== AR场景模拟 ===\n")

    # 创建AR场景
    scene = ARScene()

    # 模拟扫描数据（实际中来自深度相机或SLAM系统）
    scan_points = [(x, 0, z) for x in range(-2, 3) for z in range(-2, 3)]  # 地面点
    scan_points += [(2.5, y, z) for y in range(0, 3) for z in range(-1, 2)]  # 墙面点

    # 检测平面
    detected_planes = scene.detect_planes(scan_points)
    print(f"检测到 {len(detected_planes)} 个平面:")
    for i, plane in enumerate(detected_planes):
        plane_type = "水平" if plane.plane_type == "horizontal" else "垂直"
        print(f"  平面 {i}: {plane_type}, 中心={plane.center}, 尺寸={plane.size}")

    # 在地面上放置虚拟物体
    ground_object = scene.place_object_on_plane(0, (1.0, 0.25, 1.0))  # 在地面平面上
    if ground_object:
        print(f"\n在地面放置虚拟物体: 位置={ground_object.position}")

    # 在墙面上放置虚拟物体
    wall_object = scene.place_object_on_plane(1, (0.0, 0.5, 0.0))  # 在墙面平面上
    if wall_object:
        print(f"在墙面放置虚拟物体: 位置={wall_object.position}")

    # 检查遮挡情况
    camera_position = (0.0, 1.6, 0.0)  # 用户眼睛位置
    occlusion_results = scene.calculate_occlusion(camera_position)
    print(f"\n从相机位置 {camera_position} 观察:")
    for i, visible in enumerate(occlusion_results):
        status = "可见" if visible else "被遮挡"
        print(f"  虚拟物体 {i}: {status}")


def demonstrate_anchor_concept():
    """演示锚点概念"""
    print("\n=== 锚点概念演示 ===")

    # 创建一个平面作为锚点基础
    table_plane = Plane(
        center=(1.0, 0.75, 2.0),  # 桌子位置
        normal=(0.0, 1.0, 0.0),   # 水平向上
        size=(1.2, 0.8),          # 桌子尺寸
        plane_type="horizontal"
    )

    # 创建锚点（固定在平面上的参考点）
    anchor_position = table_plane.project_point((1.1, 1.0, 2.1))
    print(f"锚点位置: {anchor_position}")

    # 即使用户移动，锚点保持在世界坐标中的固定位置
    # 虚拟物体相对于锚点的位置保持不变
    virtual_object_offset = (0.2, 0.1, -0.1)  # 相对于锚点的偏移
    virtual_object_world_pos = (
        anchor_position[0] + virtual_object_offset[0],
        anchor_position[1] + virtual_object_offset[1],
        anchor_position[2] + virtual_object_offset[2]
    )

    print(f"虚拟物体世界位置: {virtual_object_world_pos}")
    print("锚点确保虚拟物体在真实世界中保持稳定位置！")


def main():
    """主函数"""
    simulate_ar_scene()
    demonstrate_anchor_concept()


if __name__ == "__main__":
    main()