#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：线段相交与Jarvis步进法完整实现
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def cross_product(o, a, b):
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def on_segment(p, q, r):
    return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

def segments_intersect(p1, q1, p2, q2):
    o1 = cross_product(p1, q1, p2)
    o2 = cross_product(p1, q1, q2)
    o3 = cross_product(p2, q2, p1)
    o4 = cross_product(p2, q2, q1)

    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and \
       ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True

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
    if len(points) <= 2:
        return points[:]

    leftmost = min(points, key=lambda p: p.x)
    hull = [leftmost]
    current = leftmost

    while True:
        next_point = None
        for point in points:
            if point == current:
                continue

            if next_point is None:
                next_point = point
            else:
                direction = cross_product(current, next_point, point)
                if direction < 0:
                    next_point = point
                elif direction == 0:
                    dist_current_next = (next_point.x - current.x)**2 + (next_point.y - current.y)**2
                    dist_current_point = (point.x - current.x)**2 + (point.y - current.y)**2
                    if dist_current_point > dist_current_next:
                        next_point = point

        if next_point == hull[0]:
            break

        hull.append(next_point)
        current = next_point

    return hull

def solve_segment_intersection_and_convex_hull(segments, points):
    """解决线段相交和凸包问题"""
    # 检测所有线段对是否相交
    intersections = []
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            p1, q1 = segments[i]
            p2, q2 = segments[j]
            if segments_intersect(p1, q1, p2, q2):
                intersections.append((i, j))

    hull = jarvis_march(points)
    return intersections, hull

# 测试用例
if __name__ == "__main__":
    segments = [(Point(0,0), Point(2,2)), (Point(0,2), Point(2,0))]
    points = [Point(0,0), Point(1,1), Point(2,0), Point(1,2)]

    intersections, hull = solve_segment_intersection_and_convex_hull(segments, points)
    print(f"相交线段对: {intersections}")
    print(f"凸包: {[str(p) for p in hull]}")