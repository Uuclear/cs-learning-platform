#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: Spark RDD 操作

这是 example-02-spark-rdd.py 的完整解决方案，
包含了更完整的 RDD 操作和错误处理。
"""

from typing import List, Tuple, Any, Callable, Optional


class RDD:
    """RDD (弹性分布式数据集) 完整实现"""

    def __init__(self, data: List[Any]):
        self.data = data.copy()
        self.dependencies = []

    def map(self, func: Callable[[Any], Any]) -> 'RDD':
        """Map 转换操作"""
        try:
            mapped_data = [func(item) for item in self.data]
            new_rdd = RDD(mapped_data)
            new_rdd.dependencies = self.dependencies + [("map", getattr(func, '__name__', 'anonymous'))]
            return new_rdd
        except Exception as e:
            raise RuntimeError(f"Map operation failed: {e}")

    def filter(self, func: Callable[[Any], bool]) -> 'RDD':
        """Filter 转换操作"""
        try:
            filtered_data = [item for item in self.data if func(item)]
            new_rdd = RDD(filtered_data)
            new_rdd.dependencies = self.dependencies + [("filter", getattr(func, '__name__', 'anonymous'))]
            return new_rdd
        except Exception as e:
            raise RuntimeError(f"Filter operation failed: {e}")

    def flatMap(self, func: Callable[[Any], List[Any]]) -> 'RDD':
        """FlatMap 转换操作"""
        try:
            flat_data = []
            for item in self.data:
                result = func(item)
                if isinstance(result, list):
                    flat_data.extend(result)
                else:
                    flat_data.append(result)
            new_rdd = RDD(flat_data)
            new_rdd.dependencies = self.dependencies + [("flatMap", getattr(func, '__name__', 'anonymous'))]
            return new_rdd
        except Exception as e:
            raise RuntimeError(f"FlatMap operation failed: {e}")

    def reduce(self, func: Callable[[Any, Any], Any]) -> Any:
        """Reduce 行动操作"""
        if not self.data:
            raise ValueError("Cannot reduce empty RDD")

        try:
            result = self.data[0]
            for item in self.data[1:]:
                result = func(result, item)
            return result
        except Exception as e:
            raise RuntimeError(f"Reduce operation failed: {e}")

    def collect(self) -> List[Any]:
        """Collect 行动操作"""
        return self.data.copy()

    def count(self) -> int:
        """Count 行动操作"""
        return len(self.data)

    def join(self, other: 'RDD') -> 'RDD':
        """Join 转换操作"""
        if not self.data or not other.data:
            return RDD([])

        # 验证数据格式
        if not all(isinstance(item, tuple) and len(item) >= 2 for item in self.data):
            raise ValueError("Left RDD must contain tuples with at least 2 elements")
        if not all(isinstance(item, tuple) and len(item) >= 2 for item in other.data):
            raise ValueError("Right RDD must contain tuples with at least 2 elements")

        left_dict = {}
        for key, value in self.data:
            if key not in left_dict:
                left_dict[key] = []
            left_dict[key].append(value)

        right_dict = {}
        for key, value in other.data:
            if key not in right_dict:
                right_dict[key] = []
            right_dict[key].append(value)

        joined_data = []
        for key in left_dict:
            if key in right_dict:
                for left_val in left_dict[key]:
                    for right_val in right_dict[key]:
                        joined_data.append((key, (left_val, right_val)))

        new_rdd = RDD(joined_data)
        new_rdd.dependencies = self.dependencies + other.dependencies + [("join", "join")]
        return new_rdd

    def distinct(self) -> 'RDD':
        """Distinct 转换操作：去重"""
        unique_data = list(set(self.data))
        new_rdd = RDD(unique_data)
        new_rdd.dependencies = self.dependencies + [("distinct", "distinct")]
        return new_rdd

    def union(self, other: 'RDD') -> 'RDD':
        """Union 转换操作：合并两个 RDD"""
        combined_data = self.data + other.data
        new_rdd = RDD(combined_data)
        new_rdd.dependencies = self.dependencies + other.dependencies + [("union", "union")]
        return new_rdd


def create_spark_context():
    """创建 Spark 上下文"""
    class SparkContext:
        def parallelize(self, data: List[Any]) -> RDD:
            return RDD(data)

    return SparkContext()


def main():
    """主函数：演示完整的 RDD 操作"""
    sc = create_spark_context()

    # 测试数据
    numbers = list(range(1, 11))
    rdd = sc.parallelize(numbers)

    # 基本操作测试
    squared = rdd.map(lambda x: x ** 2)
    even_numbers = rdd.filter(lambda x: x % 2 == 0)
    total = rdd.reduce(lambda a, b: a + b)

    print(f"原始数据: {rdd.collect()}")
    print(f"平方: {squared.collect()}")
    print(f"偶数: {even_numbers.collect()}")
    print(f"总和: {total}")

    # Join 操作测试
    words = sc.parallelize([("apple", 5), ("banana", 3)])
    prices = sc.parallelize([("apple", 2.5), ("banana", 1.8)])
    joined = words.join(prices)
    print(f"Join 结果: {joined.collect()}")


if __name__ == "__main__":
    main()