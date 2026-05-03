#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: Spark RDD 操作模拟

这个脚本模拟了 Apache Spark 的核心数据结构 RDD (弹性分布式数据集) 的基本操作。
RDD 是 Spark 的基础抽象，支持转换操作 (transformations) 和行动操作 (actions)。
"""

from typing import List, Tuple, Any, Callable
import random


class RDD:
    """
    RDD (弹性分布式数据集) 模拟类

    RDD 是 Spark 的核心抽象，代表不可变的、分区的元素集合，
    可以在集群中并行操作。
    """

    def __init__(self, data: List[Any]):
        """初始化 RDD"""
        self.data = data.copy()  # 创建副本以保持不可变性
        self.dependencies = []   # 依赖关系用于构建执行计划

    def map(self, func: Callable[[Any], Any]) -> 'RDD':
        """
        转换操作：对 RDD 中的每个元素应用函数

        Args:
            func: 应用到每个元素的函数

        Returns:
            新的 RDD 实例
        """
        mapped_data = [func(item) for item in self.data]
        new_rdd = RDD(mapped_data)
        new_rdd.dependencies = self.dependencies + [("map", func.__name__)]
        return new_rdd

    def filter(self, func: Callable[[Any], bool]) -> 'RDD':
        """
        转换操作：过滤 RDD 中满足条件的元素

        Args:
            func: 过滤条件函数，返回布尔值

        Returns:
            新的 RDD 实例
        """
        filtered_data = [item for item in self.data if func(item)]
        new_rdd = RDD(filtered_data)
        new_rdd.dependencies = self.dependencies + [("filter", func.__name__)]
        return new_rdd

    def flatMap(self, func: Callable[[Any], List[Any]]) -> 'RDD':
        """
        转换操作：对每个元素应用函数，然后展平结果

        Args:
            func: 返回列表的函数

        Returns:
            新的 RDD 实例
        """
        flat_data = []
        for item in self.data:
            flat_data.extend(func(item))
        new_rdd = RDD(flat_data)
        new_rdd.dependencies = self.dependencies + [("flatMap", func.__name__)]
        return new_rdd

    def reduce(self, func: Callable[[Any, Any], Any]) -> Any:
        """
        行动操作：通过函数聚合 RDD 中的所有元素

        Args:
            func: 聚合函数，接受两个参数返回一个结果

        Returns:
            聚合后的单个值
        """
        if not self.data:
            raise ValueError("Cannot reduce empty RDD")

        result = self.data[0]
        for item in self.data[1:]:
            result = func(result, item)
        return result

    def collect(self) -> List[Any]:
        """
        行动操作：将 RDD 中的所有元素收集到驱动程序

        Returns:
            包含所有元素的列表
        """
        return self.data.copy()

    def count(self) -> int:
        """
        行动操作：返回 RDD 中元素的数量

        Returns:
            元素数量
        """
        return len(self.data)

    def join(self, other: 'RDD') -> 'RDD':
        """
        转换操作：对两个键值对 RDD 执行内连接

        Args:
            other: 另一个 RDD 实例

        Returns:
            新的 RDD 实例，包含连接结果
        """
        # 假设两个 RDD 都包含键值对
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

    def __repr__(self):
        """字符串表示"""
        return f"RDD({len(self.data)} elements)"


def create_spark_context():
    """
    模拟 Spark 上下文创建

    Returns:
        SparkContext 模拟对象
    """
    class SparkContext:
        def parallelize(self, data: List[Any]) -> RDD:
            """创建 RDD"""
            return RDD(data)

    return SparkContext()


def demonstrate_rdd_operations():
    """演示 RDD 的各种操作"""
    print("=== Spark RDD 操作模拟 ===")

    # 创建 Spark 上下文
    sc = create_spark_context()

    # 创建初始 RDD
    numbers = list(range(1, 21))
    rdd = sc.parallelize(numbers)
    print(f"初始 RDD: {rdd}")

    # Map 操作：计算平方
    squared_rdd = rdd.map(lambda x: x * x)
    print(f"Map 操作 (平方): {squared_rdd.count()} 个元素")

    # Filter 操作：保留偶数
    even_rdd = rdd.filter(lambda x: x % 2 == 0)
    print(f"Filter 操作 (偶数): {even_rdd.collect()}")

    # FlatMap 操作：将每个数字扩展为 [n, n*2]
    flat_mapped = rdd.flatMap(lambda x: [x, x * 2])
    print(f"FlatMap 操作: 前10个元素 {flat_mapped.collect()[:10]}")

    # Reduce 操作：计算总和
    total_sum = rdd.reduce(lambda a, b: a + b)
    print(f"Reduce 操作 (总和): {total_sum}")

    # Join 操作演示
    words_rdd = sc.parallelize([("apple", 5), ("banana", 3), ("orange", 8)])
    prices_rdd = sc.parallelize([("apple", 2.5), ("banana", 1.8), ("grape", 4.0)])
    joined_rdd = words_rdd.join(prices_rdd)
    print(f"Join 操作结果: {joined_rdd.collect()}")

    # 链式操作：过滤偶数 -> 计算平方 -> 求和
    chain_result = (rdd
                   .filter(lambda x: x % 2 == 0)
                   .map(lambda x: x * x)
                   .reduce(lambda a, b: a + b))
    print(f"链式操作结果 (偶数平方和): {chain_result}")


def main():
    """主函数"""
    demonstrate_rdd_operations()


if __name__ == "__main__":
    main()