#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据湖区域管理解决方案

本解决方案实现了完整的数据湖三区架构管理功能。
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any


class DataLakeZone:
    """数据湖区域基类"""

    def __init__(self, zone_name: str, base_path: str):
        self.zone_name = zone_name
        self.base_path = base_path
        self.zone_path = os.path.join(base_path, zone_name.lower())
        os.makedirs(self.zone_path, exist_ok=True)

    def store_data(self, dataset_name: str, data: Any) -> str:
        """存储数据到指定区域"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{dataset_name}_{timestamp}.json"
        filepath = os.path.join(self.zone_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def list_datasets(self) -> List[str]:
        """列出该区域的所有数据集"""
        files = []
        for filename in os.listdir(self.zone_path):
            if filename.endswith('.json'):
                files.append(filename)
        return sorted(files)


class RawZone(DataLakeZone):
    """原始区：存储未经处理的原始数据"""

    def __init__(self, base_path: str):
        super().__init__("原始区", base_path)

    def ingest_raw_data(self, source: str, data: Any) -> str:
        """摄入原始数据"""
        return self.store_data(f"raw_{source}", data)


class CuratedZone(DataLakeZone):
    """精选区：存储经过清洗和验证的数据"""

    def __init__(self, base_path: str):
        super().__init__("精选区", base_path)

    def process_and_store(self, raw_data: Any, validation_rules: Dict) -> str:
        """处理并存储清洗后的数据"""
        cleaned_data = self._clean_data(raw_data)
        if self._validate_data(cleaned_data, validation_rules):
            return self.store_data("curated_processed", cleaned_data)
        else:
            raise ValueError("数据验证失败")

    def _clean_data(self, data: Any) -> Dict:
        """模拟数据清洗"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                clean_key = key.lower().replace(" ", "_")
                if value is not None:
                    cleaned[clean_key] = value
            return cleaned
        return data

    def _validate_data(self, data: Any, rules: Dict) -> bool:
        """模拟数据验证"""
        if not isinstance(data, dict):
            return False

        for field, rule in rules.items():
            if field not in data:
                return False
            if rule.get("required") and data[field] is None:
                return False
            if rule.get("type") == "string" and not isinstance(data[field], str):
                return False
            if rule.get("type") == "number" and not isinstance(data[field], (int, float)):
                return False

        return True


class ServingZone(DataLakeZone):
    """服务区：存储为特定用例优化的数据"""

    def __init__(self, base_path: str):
        super().__init__("服务区", base_path)

    def create_serving_dataset(self, source_data: Any, use_case: str) -> str:
        """为特定用例创建优化的数据集"""
        if use_case == "machine_learning":
            optimized_data = self._optimize_for_ml(source_data)
        elif use_case == "analytics":
            optimized_data = self._optimize_for_analytics(source_data)
        else:
            optimized_data = source_data

        return self.store_data(f"serving_{use_case}", optimized_data)

    def _optimize_for_ml(self, data: Any) -> Dict:
        """为机器学习优化数据"""
        return {
            "features": data,
            "metadata": {
                "optimization_type": "ml_ready",
                "timestamp": 1234567890,
                "feature_count": len(data) if isinstance(data, dict) else 0
            }
        }

    def _optimize_for_analytics(self, data: Any) -> Dict:
        """为分析优化数据"""
        return {
            "aggregated_data": data,
            "metadata": {
                "optimization_type": "analytics_ready",
                "timestamp": 1234567890,
                "query_optimized": True
            }
        }


def main():
    """主函数：演示数据湖三区架构"""
    base_path = "./data_lake_solution"

    raw_zone = RawZone(base_path)
    curated_zone = CuratedZone(base_path)
    serving_zone = ServingZone(base_path)

    raw_user_data = {
        "User ID": 12345,
        "Name": "张三",
        "Email": "zhangsan@example.com",
        "Age": 28,
        "Registration Date": "2023-01-15",
        "Last Login": "2023-12-01"
    }

    raw_file = raw_zone.ingest_raw_data("user_service", raw_user_data)

    validation_rules = {
        "user_id": {"required": True, "type": "number"},
        "name": {"required": True, "type": "string"},
        "email": {"required": True, "type": "string"}
    }

    curated_file = curated_zone.process_and_store(raw_user_data, validation_rules)

    with open(curated_file, 'r', encoding='utf-8') as f:
        curated_data = json.load(f)

    serving_zone.create_serving_dataset(curated_data, "machine_learning")
    serving_zone.create_serving_dataset(curated_data, "analytics")


if __name__ == "__main__":
    main()