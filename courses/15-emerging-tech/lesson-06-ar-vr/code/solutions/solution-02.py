#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：空间跟踪的完整实现
"""

import math
import time
from typing import Tuple


class HeadTracker:
    """头部跟踪器"""

    def __init__(self):
        self.position = (0.0, 0.0, 0.0)
        self.rotation = (0.0, 0.0, 0.0)
        self.last_update_time = time.time()
        self.latency = 0.016

    def update_position(self, x: float, y: float, z: float):
        self.position = (x, y, z)
        self.last_update_time = time.time()

    def update_rotation(self, pitch: float, yaw: float, roll: float):
        self.rotation = (pitch, yaw, roll)
        self.last_update_time = time.time()

    def get_current_state(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        current_time = time.time()
        elapsed = current_time - self.last_update_time

        if elapsed < self.latency:
            return self._predict_state(elapsed)
        else:
            return self.position, self.rotation

    def _predict_state(self, elapsed: float) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        return self.position, self.rotation


class CoordinateSystem:
    """坐标系统"""

    @staticmethod
    def world_to_head(world_pos: Tuple[float, float, float],
                     head_pos: Tuple[float, float, float],
                     head_rot: Tuple[float, float, float]) -> Tuple[float, float, float]:
        x = world_pos[0] - head_pos[0]
        y = world_pos[1] - head_pos[1]
        z = world_pos[2] - head_pos[2]

        pitch, yaw, roll = head_rot

        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)
        x_rot_y = x * cos_yaw + z * sin_yaw
        z_rot_y = -x * sin_yaw + z * cos_yaw

        cos_pitch = math.cos(pitch)
        sin_pitch = math.sin(pitch)
        y_rot_x = y * cos_pitch - z_rot_y * sin_pitch
        z_rot_x = y * sin_pitch + z_rot_y * cos_pitch

        return (x_rot_y, y_rot_x, z_rot_x)

    @staticmethod
    def calculate_view_direction(head_rot: Tuple[float, float, float]) -> Tuple[float, float, float]:
        pitch, yaw, roll = head_rot

        x = math.sin(yaw) * math.cos(pitch)
        y = math.sin(pitch)
        z = math.cos(yaw) * math.cos(pitch)

        length = math.sqrt(x*x + y*y + z*z)
        if length > 0:
            x, y, z = x/length, y/length, z/length

        return (x, y, z)


def main():
    tracker = HeadTracker()
    tracker.update_position(0.0, 1.7, 0.0)
    tracker.update_rotation(0.0, 0.0, 0.0)

    pos, rot = tracker.get_current_state()
    view_dir = CoordinateSystem.calculate_view_direction(rot)
    world_object = (2.0, 1.7, 3.0)
    head_coords = CoordinateSystem.world_to_head(world_object, pos, rot)


if __name__ == "__main__":
    main()