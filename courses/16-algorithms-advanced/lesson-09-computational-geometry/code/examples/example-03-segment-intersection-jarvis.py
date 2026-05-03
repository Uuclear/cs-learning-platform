#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：线段相交与Jarvis步进法
演示线段相交检测和Jarvis步进法求凸包
"""

class Point:
    """二维点类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

def cross_product(o, a, b):
    """计算叉积"""
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def on_segment(p, q, r):
    """
    判断点q是否在线段pr上（假设三点共线）
    """
    return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

def segments_intersect(p1, q1, p2, q2):
    """
    判断两条线段是否相交

    参数:
        p1, q1: 第一条线段的端点
        p2, q2: 第二条线段的端点

    返回:
        bool - True表示相交，False表示不相交
    """
    # 计算四个方向
    o1 = cross_product(p1, q1, p2)
    o2 = cross_product(p1, q1, q2)
    o3 = cross_product(p2, q2, p1)
    o4 = cross_product(p2, q2, q1)

    # 一般情况：两条线段相交当且仅当
    # (p1,q1,p2)和(p1,q1,q2)的方向不同，且
    # (p2,q2,p1)和(p2,q2,q1)的方向不同
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and \
       ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True

    # 特殊情况：共线情况
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def jarvis_march(points):
    """
    Jarvis步进法（Gift Wrapping）求凸包

    参数:
        points: Point对象列表

    返回:
        Point对象列表，表示凸包顶点
    """
    if len(points) <= 2:
        return points[:]

    # 找到最左边的点
    leftmost = min(points, key=lambda p: p.x)
    hull = [leftmost]
    current = leftmost

    while True:
        # 选择下一个点
        next_point = points[0]
        for point in points[1:]:
            if point == current:
                continue

            # 计算方向
            direction = cross_product(current, next_point, point)
            if next_point == current or direction < 0:
                next_point = point
            elif direction == 0:
                # 共线时选择更远的点
                dist_current_next = (next_point.x - current.x)**2 + (next_point.y - current.y)**2
                dist_current_point = (point.x - current.x)**2 + (point.y - current.y)**2
                if dist_current_point > dist_current_next:
                    next_point = point

        if next_point == hull[0]:
            break

        hull.append(next_point)
        current = next_point

    return hull

def main():
    """主函数：演示线段相交和Jarvis步进法"""
    print("计算几何示例3：线段相交与Jarvis步进法")
    print("=" * 40)

    # 测试线段相交
    p1, q1 = Point(0, 0), Point(2, 2)
    p2, q2 = Point(0, 2), Point(2, 0)
    p3, q3 = Point(0, 0), Point(1, 1)

    print(f"线段1: {p1} -> {q1}")
    print(f"线段2: {p2} -> {q2}")
    print(f"线段3: {p3} -> {q3}")

    print(f"线段1和线段2相交: {segments_intersect(p1, q1, p2, q2)} (应该为True)")
    print(f"线段1和线段3相交: {segments_intersect(p1, q1, p3, q3)} (应该为True)")

    # 测试Jarvis步进法
    test_points = [
        Point(0, 0), Point(1, 1), Point(2, 0),
        Point(1, 2), Point(0, 2), Point(2, 2)
    ]

    print(f"\n测试点集: {[str(p) for p in test_points]}")
    hull = jarvis_march(test_points)
    print(f"Jarvis步进法凸包: {[str(p) for p in hull]}")

    # 比较Graham扫描法和Jarvis步进法的结果
    # （这里简化，实际应该实现Graham扫描法进行比较）

if __name__ == "__main__":
    main()