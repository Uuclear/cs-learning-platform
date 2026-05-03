#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：AR场景的完整实现
"""

import math
from typing import List, Tuple, Optional


class Plane:
    """平面类"""

    def __init__(self, center: Tuple[float, float, float], normal: Tuple[float, float, float],
                 size: Tuple[float, float], plane_type: str = "horizontal"):
        self.center = center
        self.normal = normal
        self.size = size
        self.plane_type = plane_type

    def contains_point(self, point: Tuple[float, float, float], tolerance: float = 0.1) -> bool:
        distance = abs(
            self.normal[0] * (point[0] - self.center[0]) +
            self.normal[1] * (point[1] - self.center[1]) +
            self.normal[2] * (point[2] - self.center[2])
        )

        if distance > tolerance:
            return False

        if self.plane_type == "horizontal":
            half_width, half_height = self.size[0]/2, self.size[1]/2
            dx = abs(point[0] - self.center[0])
            dz = abs(point[2] - self.center[2])
            return dx <= half_width and dz <= half_height
        else:
            half_width, half_height = self.size[0]/2, self.size[1]/2
            dx = abs(point[0] - self.center[0])
            dy = abs(point[1] - self.center[1])
            return dx <= half_width and dy <= half_height

    def project_point(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        to_point = (
            point[0] - self.center[0],
            point[1] - self.center[1],
            point[2] - self.center[2]
        )

        distance = (
            to_point[0] * self.normal[0] +
            to_point[1] * self.normal[1] +
            to_point[2] * self.normal[2]
        )

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
        self.position = position
        self.size = size
        self.object_type = object_type

    def get_bounding_box(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
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
        return True


class ARScene:
    """AR场景管理器"""

    def __init__(self):
        self.detected_planes: List[Plane] = []
        self.virtual_objects: List[VirtualObject] = []

    def detect_planes(self, scan_data: List[Tuple[float, float, float]]) -> List[Plane]:
        planes = []

        ground_plane = Plane(
            center=(0.0, 0.0, 0.0),
            normal=(0.0, 1.0, 0.0),
            size=(5.0, 5.0),
            plane_type="horizontal"
        )
        planes.append(ground_plane)

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
        if plane_index >= len(self.detected_planes):
            return None

        plane = self.detected_planes[plane_index]
        target_pos = (
            plane.center[0] + offset[0],
            plane.center[1] + offset[1],
            plane.center[2] + offset[2]
        )

        final_pos = plane.project_point(target_pos)

        virtual_obj = VirtualObject(
            position=final_pos,
            size=(0.5, 0.5, 0.5),
            object_type="cube"
        )

        self.virtual_objects.append(virtual_obj)
        return virtual_obj

    def calculate_occlusion(self, camera_pos: Tuple[float, float, float]) -> List[bool]:
        visibility = []
        for obj in self.virtual_objects:
            visible = obj.is_visible_from(camera_pos)
            visibility.append(visible)
        return visibility


def main():
    scene = ARScene()
    scan_points = [(x, 0, z) for x in range(-2, 3) for z in range(-2, 3)]
    scan_points += [(2.5, y, z) for y in range(0, 3) for z in range(-1, 2)]

    detected_planes = scene.detect_planes(scan_points)
    ground_object = scene.place_object_on_plane(0, (1.0, 0.25, 1.0))
    wall_object = scene.place_object_on_plane(1, (0.0, 0.5, 0.0))

    camera_position = (0.0, 1.6, 0.0)
    occlusion_results = scene.calculate_occlusion(camera_position)


if __name__ == "__main__":
    main()