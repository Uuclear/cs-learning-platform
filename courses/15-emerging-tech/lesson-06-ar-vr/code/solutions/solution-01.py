#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：3D数学操作的完整实现
"""

import math


class Vector3D:
    """三维向量类"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)

    def __str__(self):
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Matrix4x4:
    """4x4矩阵类"""

    def __init__(self):
        self.data = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    @staticmethod
    def identity():
        return Matrix4x4()

    @staticmethod
    def translation(tx, ty, tz):
        m = Matrix4x4()
        m.data[0][3] = tx
        m.data[1][3] = ty
        m.data[2][3] = tz
        return m

    @staticmethod
    def rotation_x(angle_rad):
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
        m = Matrix4x4()
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        m.data[0][0] = cos_a
        m.data[0][1] = -sin_a
        m.data[1][0] = sin_a
        m.data[1][1] = cos_a
        return m

    def multiply_vector(self, vec):
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
        result = Matrix4x4()
        for i in range(4):
            for j in range(4):
                result.data[i][j] = sum(
                    self.data[i][k] * other.data[k][j] for k in range(4)
                )
        return result


def main():
    # 测试向量操作
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)

    # 测试矩阵变换
    translation = Matrix4x4.translation(10, 20, 30)
    point = Vector3D(1, 1, 1)
    translated = translation.multiply_vector(point)

    rotation_y = Matrix4x4.rotation_y(math.pi / 4)
    rotated = rotation_y.multiply_vector(Vector3D(1, 0, 0))

    combined = translation.multiply_matrix(rotation_y)
    transformed = combined.multiply_vector(Vector3D(1, 0, 0))


if __name__ == "__main__":
    main()