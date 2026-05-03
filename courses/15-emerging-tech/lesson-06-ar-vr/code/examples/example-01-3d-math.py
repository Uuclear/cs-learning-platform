#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：3D变换数学基础
演示向量、矩阵和旋转的基本操作，仅使用标准库math模块
"""

import math


class Vector3D:
    """三维向量类"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """初始化三维向量"""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """向量加法"""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """向量减法"""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """向量与标量相乘"""
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        """点积（标量积）"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """叉积（向量积）"""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        """向量的模（长度）"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """归一化向量（单位向量）"""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)

    def __str__(self):
        """字符串表示"""
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Matrix4x4:
    """4x4矩阵类，用于3D变换"""

    def __init__(self):
        """初始化为单位矩阵"""
        self.data = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    @staticmethod
    def identity():
        """创建单位矩阵"""
        return Matrix4x4()

    @staticmethod
    def translation(tx, ty, tz):
        """创建平移矩阵"""
        m = Matrix4x4()
        m.data[0][3] = tx
        m.data[1][3] = ty
        m.data[2][3] = tz
        return m

    @staticmethod
    def rotation_x(angle_rad):
        """创建绕X轴旋转矩阵"""
        m = Matrix4x4()
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        m.data[1][1] = cos_a
        m.data[1][2] = -sin_a
        m.data[2][1] = sin_a
        m.data[2][2] = cos_a
        return m

    @staticmethod
    def rotation_y(angle_rad):
        """创建绕Y轴旋转矩阵"""
        m = Matrix4x4()
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        m.data[0][0] = cos_a
        m.data[0][2] = sin_a
        m.data[2][0] = -sin_a
        m.data[2][2] = cos_a
        return m

    @staticmethod
    def rotation_z(angle_rad):
        """创建绕Z轴旋转矩阵"""
        m = Matrix4x4()
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        m.data[0][0] = cos_a
        m.data[0][1] = -sin_a
        m.data[1][0] = sin_a
        m.data[1][1] = cos_a
        return m

    def multiply_vector(self, vec):
        """矩阵与向量相乘"""
        x = (self.data[0][0] * vec.x + self.data[0][1] * vec.y +
             self.data[0][2] * vec.z + self.data[0][3])
        y = (self.data[1][0] * vec.x + self.data[1][1] * vec.y +
             self.data[1][2] * vec.z + self.data[1][3])
        z = (self.data[2][0] * vec.x + self.data[2][1] * vec.y +
             self.data[2][2] * vec.z + self.data[2][3])
        w = (self.data[3][0] * vec.x + self.data[3][1] * vec.y +
             self.data[3][2] * vec.z + self.data[3][3])

        if w != 0:
            x, y, z = x/w, y/w, z/w

        return Vector3D(x, y, z)

    def multiply_matrix(self, other):
        """矩阵相乘"""
        result = Matrix4x4()
        for i in range(4):
            for j in range(4):
                result.data[i][j] = sum(
                    self.data[i][k] * other.data[k][j] for k in range(4)
                )
        return result

    def __str__(self):
        """字符串表示"""
        lines = []
        for row in self.data:
            lines.append("[" + ", ".join(f"{val:8.3f}" for val in row) + "]")
        return "\n".join(lines)


def main():
    """主函数：演示3D数学操作"""
    print("=== 3D变换数学演示 ===\n")

    # 创建向量
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)

    print(f"向量 v1 = {v1}")
    print(f"向量 v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 · v2 = {v1.dot(v2):.3f} (点积)")
    print(f"v1 × v2 = {v1.cross(v2)} (叉积)")
    print(f"|v1| = {v1.magnitude():.3f} (模长)")
    print(f"单位向量 v1 = {v1.normalize()}\n")

    # 创建变换矩阵
    print("=== 矩阵变换演示 ===")

    # 平移变换
    translation = Matrix4x4.translation(10, 20, 30)
    point = Vector3D(1, 1, 1)
    translated = translation.multiply_vector(point)
    print(f"原始点: {point}")
    print(f"平移后: {translated}")

    # 旋转变换
    rotation_y = Matrix4x4.rotation_y(math.pi / 4)  # 45度绕Y轴旋转
    rotated = rotation_y.multiply_vector(Vector3D(1, 0, 0))
    print(f"X轴单位向量绕Y轴旋转45度: {rotated}")

    # 组合变换：先旋转后平移
    combined = translation.multiply_matrix(rotation_y)
    transformed = combined.multiply_vector(Vector3D(1, 0, 0))
    print(f"组合变换(旋转+平移): {transformed}")


if __name__ == "__main__":
    main()