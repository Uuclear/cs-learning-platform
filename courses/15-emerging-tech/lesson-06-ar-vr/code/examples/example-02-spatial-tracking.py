#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：空间跟踪模拟
模拟头部/眼睛位置跟踪，包括坐标变换和延迟计算
"""

import math
import time
from typing import Tuple


class HeadTracker:
    """头部跟踪器模拟类"""

    def __init__(self):
        """初始化跟踪器"""
        self.position = (0.0, 0.0, 0.0)  # (x, y, z) 位置
        self.rotation = (0.0, 0.0, 0.0)  # (pitch, yaw, roll) 旋转角度（弧度）
        self.last_update_time = time.time()
        self.latency = 0.016  # 模拟16ms延迟（约60fps）

    def update_position(self, x: float, y: float, z: float):
        """更新位置"""
        self.position = (x, y, z)
        self.last_update_time = time.time()

    def update_rotation(self, pitch: float, yaw: float, roll: float):
        """更新旋转"""
        self.rotation = (pitch, yaw, roll)
        self.last_update_time = time.time()

    def get_current_state(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """获取当前状态（考虑延迟）"""
        current_time = time.time()
        elapsed = current_time - self.last_update_time

        # 模拟由于延迟导致的状态滞后
        if elapsed < self.latency:
            # 返回预测状态（简单线性预测）
            return self._predict_state(elapsed)
        else:
            # 返回最新状态
            return self.position, self.rotation

    def _predict_state(self, elapsed: float) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """预测状态（简化版）"""
        # 在实际系统中，这会使用更复杂的预测算法
        # 这里我们简单返回当前状态
        return self.position, self.rotation


class CoordinateSystem:
    """坐标系统类"""

    @staticmethod
    def world_to_head(world_pos: Tuple[float, float, float],
                     head_pos: Tuple[float, float, float],
                     head_rot: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        将世界坐标转换为头部坐标系
        :param world_pos: 世界坐标 (x, y, z)
        :param head_pos: 头部位置 (x, y, z)
        :param head_rot: 头部旋转 (pitch, yaw, roll)
        :return: 头部坐标系中的位置
        """
        # 先平移（相对于头部位置）
        x = world_pos[0] - head_pos[0]
        y = world_pos[1] - head_pos[1]
        z = world_pos[2] - head_pos[2]

        # 应用旋转（简化：只考虑yaw和pitch）
        pitch, yaw, roll = head_rot

        # 绕Y轴旋转（yaw）
        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)
        x_rot_y = x * cos_yaw + z * sin_yaw
        z_rot_y = -x * sin_yaw + z * cos_yaw

        # 绕X轴旋转（pitch）
        cos_pitch = math.cos(pitch)
        sin_pitch = math.sin(pitch)
        y_rot_x = y * cos_pitch - z_rot_y * sin_pitch
        z_rot_x = y * sin_pitch + z_rot_y * cos_pitch

        return (x_rot_y, y_rot_x, z_rot_x)

    @staticmethod
    def calculate_view_direction(head_rot: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        计算视线方向向量
        :param head_rot: 头部旋转 (pitch, yaw, roll)
        :return: 归一化的视线方向向量
        """
        pitch, yaw, roll = head_rot

        # 假设初始视线方向是Z轴正方向
        x = math.sin(yaw) * math.cos(pitch)
        y = math.sin(pitch)
        z = math.cos(yaw) * math.cos(pitch)

        # 归一化
        length = math.sqrt(x*x + y*y + z*z)
        if length > 0:
            x, y, z = x/length, y/length, z/length

        return (x, y, z)


def simulate_tracking():
    """模拟跟踪过程"""
    print("=== 空间跟踪模拟 ===\n")

    # 创建跟踪器
    tracker = HeadTracker()

    # 设置初始状态
    tracker.update_position(0.0, 1.7, 0.0)  # 站立位置，身高1.7米
    tracker.update_rotation(0.0, 0.0, 0.0)  # 直视前方

    # 获取当前状态
    pos, rot = tracker.get_current_state()
    print(f"头部位置: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
    print(f"头部旋转: (俯仰={math.degrees(rot[0]):.1f}°, 偏航={math.degrees(rot[1]):.1f}°, 翻滚={math.degrees(rot[2]):.1f}°)")

    # 计算视线方向
    view_dir = CoordinateSystem.calculate_view_direction(rot)
    print(f"视线方向: ({view_dir[0]:.3f}, {view_dir[1]:.3f}, {view_dir[2]:.3f})")

    # 转换世界坐标到头部坐标
    world_object = (2.0, 1.7, 3.0)  # 世界中的物体位置
    head_coords = CoordinateSystem.world_to_head(world_object, pos, rot)
    print(f"世界物体 {world_object} 在头部坐标系中: ({head_coords[0]:.3f}, {head_coords[1]:.3f}, {head_coords[2]:.3f})")

    print(f"\n模拟延迟: {tracker.latency*1000:.1f}ms")
    print(f"目标帧率: {1.0/tracker.latency:.0f}fps")


def calculate_latency_impact():
    """计算延迟对用户体验的影响"""
    print("\n=== 延迟影响分析 ===")

    # 不同延迟值对应的帧率
    latencies = [0.008, 0.011, 0.016, 0.022, 0.033]  # 125Hz, 90Hz, 60Hz, 45Hz, 30Hz

    print("延迟 vs 帧率 vs 用户体验:")
    for latency in latencies:
        fps = 1.0 / latency
        if latency <= 0.011:  # <=11ms (~90fps)
            experience = "优秀 - 几乎无延迟感"
        elif latency <= 0.016:  # <=16ms (60fps)
            experience = "良好 - 可接受的延迟"
        elif latency <= 0.022:  # <=22ms (45fps)
            experience = "一般 - 明显延迟感"
        else:  # >22ms (<45fps)
            experience = "较差 - 可能引起晕动症"

        print(f"  {latency*1000:4.1f}ms → {fps:5.1f}fps → {experience}")


def main():
    """主函数"""
    simulate_tracking()
    calculate_latency_impact()


if __name__ == "__main__":
    main()