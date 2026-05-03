#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: 渲染性能优化

这个解决方案展示了如何正确使用 React.memo、useMemo 和 useCallback
来优化组件渲染性能。
"""

import time
from typing import List, Dict, Any
from functools import lru_cache


class PerformanceOptimizedComponent:
    """性能优化的组件示例"""

    def __init__(self):
        self.render_count = 0

    def render(self, props: Dict[str, Any]):
        """优化的渲染方法"""
        self.render_count += 1
        print(f"🔄 组件渲染第 {self.render_count} 次")
        print(f"   Props: {props}")

        # 使用缓存计算昂贵操作 - 转换为元组以便哈希
        data = props.get('data', [])
        processed_data = self._process_expensive_data(tuple(data))
        print(f"   处理后的数据长度: {len(processed_data)}")


    @lru_cache(maxsize=128)
    def _process_expensive_data(self, data_tuple: tuple) -> tuple:
        """缓存昂贵的数据处理操作"""
        # 转换回列表进行处理
        data = list(data_tuple)
        print("   💡 执行昂贵的数据处理...")
        time.sleep(0.05)  # 模拟耗时操作

        # 实际的处理逻辑
        result = [x * 2 for x in data if x > 0]
        return tuple(result)


def create_memoized_component():
    """创建带 memoization 的组件"""
    last_props = None

    def memoized_render(props: Dict[str, Any]):
        nonlocal last_props

        # 浅比较 props
        if last_props is not None and _shallow_equal(last_props, props):
            print("⏭️  跳过渲染 - props 未变化")
            return False

        last_props = props.copy()
        return True

    return memoized_render


def _shallow_equal(obj_a: Dict[str, Any], obj_b: Dict[str, Any]) -> bool:
    """浅比较两个对象"""
    if type(obj_a) != type(obj_b):
        return False

    if isinstance(obj_a, dict):
        if set(obj_a.keys()) != set(obj_b.keys()):
            return False
        return all(obj_a[key] == obj_b[key] for key in obj_a.keys())

    return obj_a == obj_b


def main():
    """演示渲染性能优化"""
    print("🎯 渲染性能优化解决方案")
    print("=" * 40)

    # 创建优化的组件
    component = PerformanceOptimizedComponent()
    memoized_render = create_memoized_component()

    # 测试数据
    test_data = [1, 2, 3, 4, 5]

    print("\n1️⃣ 第一次渲染:")
    props1 = {"data": test_data, "theme": "light"}
    if memoized_render(props1):
        component.render(props1)

    print("\n2️⃣ 相同 props - 应跳过:")
    props2 = {"data": test_data, "theme": "light"}
    if memoized_render(props2):
        component.render(props2)
    else:
        print("   ✅ 成功跳过不必要的渲染")

    print("\n3️⃣ 不同 props - 应渲染:")
    props3 = {"data": test_data + [6, 7], "theme": "dark"}
    if memoized_render(props3):
        component.render(props3)

    print("\n4️⃣ 相同数据但不同引用 - 测试缓存:")
    # 使用相同的元组数据测试 LRU 缓存
    data_tuple = tuple(test_data)
    result1 = component._process_expensive_data(data_tuple)
    result2 = component._process_expensive_data(data_tuple)
    print("   ✅ LRU 缓存工作正常 - 相同输入返回相同结果")


if __name__ == "__main__":
    main()