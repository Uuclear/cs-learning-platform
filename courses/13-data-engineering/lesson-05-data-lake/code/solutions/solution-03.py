#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据湖 vs 数据仓库性能对比解决方案

本解决方案实现了完整的性能对比测试功能。
"""

import time
import random
from typing import List, Dict, Any, Callable


class DataStorageSystem:
    """数据存储系统基类"""

    def __init__(self, name: str):
        self.name = name
        self.data = []
        self.indexes = {}
        self.schema = {}

    def ingest_data(self, records: List[Dict[str, Any]]) -> float:
        """摄入数据并返回耗时"""
        start_time = time.time()
        self.data.extend(records)
        end_time = time.time()
        return end_time - start_time

    def query_data(self, filter_func: Callable[[Dict], bool],
                  projection: List[str] = None) -> tuple[List[Dict], float]:
        """查询数据并返回结果和耗时"""
        start_time = time.time()
        results = []

        for record in self.data:
            if filter_func(record):
                if projection:
                    filtered_record = {k: v for k, v in record.items() if k in projection}
                    results.append(filtered_record)
                else:
                    results.append(record.copy())

        end_time = time.time()
        return results, end_time - start_time


class DataLakeSystem(DataStorageSystem):
    """数据湖系统模拟器"""

    def __init__(self):
        super().__init__("数据湖")

    def ingest_data(self, records: List[Dict[str, Any]]) -> float:
        """数据湖摄入：通常更快，因为不需要模式验证"""
        time.sleep(0.01)
        return super().ingest_data(records)

    def query_data(self, filter_func: Callable[[Dict], bool],
                  projection: List[str] = None) -> tuple[List[Dict], float]:
        """数据湖查询：可能较慢，特别是没有优化时"""
        results, query_time = super().query_data(filter_func, projection)
        time.sleep(min(0.05, len(results) * 0.001))
        return results, query_time + min(0.05, len(results) * 0.001)


class DataWarehouseSystem(DataStorageSystem):
    """数据仓库系统模拟器"""

    def __init__(self):
        super().__init__("数据仓库")

    def define_schema(self, schema: Dict[str, str]) -> None:
        """定义模式（数据仓库需要预定义模式）"""
        self.schema = schema

    def ingest_data(self, records: List[Dict[str, Any]]) -> float:
        """数据仓库摄入：较慢，因为需要ETL和模式验证"""
        valid_records = []
        for record in records:
            if self._validate_record(record):
                valid_records.append(record)

        etl_time = len(records) * 0.002
        time.sleep(etl_time)

        return super().ingest_data(valid_records)

    def _validate_record(self, record: Dict[str, Any]) -> bool:
        """验证记录是否符合模式"""
        for field, expected_type in self.schema.items():
            if field not in record:
                return False
            if expected_type == "string" and not isinstance(record[field], str):
                return False
            elif expected_type == "number" and not isinstance(record[field], (int, float)):
                return False
        return True

    def create_index(self, field: str) -> None:
        """创建索引以优化查询"""
        self.indexes[field] = {}
        for i, record in enumerate(self.data):
            if field in record:
                value = record[field]
                if value not in self.indexes[field]:
                    self.indexes[field][value] = []
                self.indexes[field][value].append(i)

    def query_data(self, filter_func: Callable[[Dict], bool],
                  projection: List[str] = None) -> tuple[List[Dict], float]:
        """数据仓库查询：通常更快，特别是有索引时"""
        start_time = time.time()
        results = []
        results, _ = super().query_data(filter_func, projection)
        end_time = time.time()
        return results, end_time - start_time


def generate_sample_data(num_records: int) -> List[Dict[str, Any]]:
    """生成示例数据"""
    data = []
    for i in range(num_records):
        record = {
            "user_id": i,
            "name": f"用户_{i}",
            "email": f"user{i}@example.com",
            "age": random.randint(18, 80),
            "city": random.choice(["北京", "上海", "广州", "深圳", "杭州"]),
            "is_premium": random.choice([True, False]),
            "last_login": f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        }
        data.append(record)
    return data


def run_performance_comparison():
    """运行性能对比测试"""
    test_data = generate_sample_data(1000)

    data_lake = DataLakeSystem()
    data_warehouse = DataWarehouseSystem()

    warehouse_schema = {
        "user_id": "number",
        "name": "string",
        "email": "string",
        "age": "number",
        "city": "string",
        "is_premium": "boolean",
        "last_login": "string"
    }
    data_warehouse.define_schema(warehouse_schema)

    lake_ingest_time = data_lake.ingest_data(test_data.copy())
    warehouse_ingest_time = data_warehouse.ingest_data(test_data.copy())

    data_warehouse.create_index("city")
    data_warehouse.create_index("age")

    def city_filter(record):
        return record.get("city") == "北京"

    lake_results, lake_query_time = data_lake.query_data(city_filter, ["user_id", "name", "city"])
    warehouse_results, warehouse_query_time = data_warehouse.query_data(city_filter, ["user_id", "name", "city"])

    def email_filter(record):
        return record.get("email", "").endswith("@example.com")

    lake_results2, lake_query_time2 = data_lake.query_data(email_filter)
    warehouse_results2, warehouse_query_time2 = data_warehouse.query_data(email_filter)

    new_data_with_extra_field = test_data[:10].copy()
    for record in new_data_with_extra_field:
        record["new_feature"] = "beta_user"

    lake_ingest_time2 = data_lake.ingest_data(new_data_with_extra_field)
    warehouse_ingest_time2 = data_warehouse.ingest_data(new_data_with_extra_field)


def main():
    """主函数"""
    run_performance_comparison()


if __name__ == "__main__":
    main()