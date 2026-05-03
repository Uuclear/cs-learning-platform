#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单数据目录系统示例

这个示例演示了如何实现一个基础的数据目录系统，
用于管理和发现组织内的数据资产。
"""

import json
from datetime import datetime
from typing import Dict, List, Any


class SimpleDataCatalog:
    """简单的数据目录系统"""

    def __init__(self):
        """初始化数据目录系统"""
        self.assets = {}  # 存储数据资产信息
        self.tags = {}    # 存储标签索引

    def register_asset(self, asset_id: str, asset_info: Dict[str, Any]):
        """注册数据资产

        Args:
            asset_id: 数据资产唯一标识符
            asset_info: 数据资产的元数据信息
        """
        asset_info["registered_at"] = datetime.now().isoformat()
        asset_info["asset_id"] = asset_id

        # 设置默认值
        asset_info.setdefault("description", "")
        asset_info.setdefault("owner", "")
        asset_info.setdefault("data_type", "unknown")
        asset_info.setdefault("tags", [])

        self.assets[asset_id] = asset_info

        # 更新标签索引
        for tag in asset_info["tags"]:
            if tag not in self.tags:
                self.tags[tag] = []
            if asset_id not in self.tags[tag]:
                self.tags[tag].append(asset_id)

    def search_assets(self, query: str = "", tags: List[str] = None) -> List[Dict]:
        """搜索数据资产

        Args:
            query: 搜索关键词，匹配资产ID、描述和所有者
            tags: 标签列表，返回包含所有指定标签的资产

        Returns:
            匹配的数据资产列表
        """
        results = []

        for asset_id, asset_info in self.assets.items():
            # 检查查询字符串匹配
            matches_query = True
            if query:
                searchable_text = " ".join([
                    asset_info.get("asset_id", ""),
                    asset_info.get("description", ""),
                    asset_info.get("owner", "")
                ]).lower()
                matches_query = query.lower() in searchable_text

            # 检查标签匹配
            matches_tags = True
            if tags:
                asset_tags = set(asset_info.get("tags", []))
                required_tags = set(tags)
                matches_tags = required_tags.issubset(asset_tags)

            if matches_query and matches_tags:
                results.append(asset_info.copy())

        return results

    def get_asset_details(self, asset_id: str) -> Dict:
        """获取数据资产详细信息

        Args:
            asset_id: 数据资产唯一标识符

        Returns:
            数据资产的完整信息，如果不存在则返回空字典
        """
        return self.assets.get(asset_id, {})

    def update_asset_metadata(self, asset_id: str, updates: Dict[str, Any]):
        """更新数据资产元数据

        Args:
            asset_id: 数据资产唯一标识符
            updates: 要更新的元数据字段
        """
        if asset_id in self.assets:
            old_tags = set(self.assets[asset_id].get("tags", []))
            self.assets[asset_id].update(updates)

            # 更新标签索引（如果标签有变化）
            new_tags = set(self.assets[asset_id].get("tags", []))
            if old_tags != new_tags:
                # 移除旧标签引用
                for tag in old_tags - new_tags:
                    if tag in self.tags and asset_id in self.tags[tag]:
                        self.tags[tag].remove(asset_id)

                # 添加新标签引用
                for tag in new_tags - old_tags:
                    if tag not in self.tags:
                        self.tags[tag] = []
                    if asset_id not in self.tags[tag]:
                        self.tags[tag].append(asset_id)


def main():
    """主函数：演示数据目录系统的使用"""
    # 创建数据目录实例
    catalog = SimpleDataCatalog()

    # 注册数据资产
    catalog.register_asset(
        "customer_table",
        {
            "description": "客户基本信息表，包含客户ID、姓名、联系方式等",
            "owner": "数据团队",
            "data_type": "table",
            "location": "database.sales.customers",
            "row_count": 100000,
            "last_updated": "2023-01-15",
            "tags": ["customer", "pii", "sales"]
        }
    )

    catalog.register_asset(
        "order_summary_view",
        {
            "description": "订单汇总视图，按月统计销售额和订单数量",
            "owner": "BI团队",
            "data_type": "view",
            "location": "database.bi.order_summary",
            "refresh_frequency": "daily",
            "tags": ["sales", "analytics", "monthly"]
        }
    )

    catalog.register_asset(
        "user_behavior_log",
        {
            "description": "用户行为日志，记录用户在网站上的点击和浏览行为",
            "owner": "产品团队",
            "data_type": "log",
            "location": "s3://logs/user-behavior/",
            "format": "json",
            "tags": ["user", "behavior", "web"]
        }
    )

    catalog.register_asset(
        "product_catalog_db",
        {
            "description": "产品目录数据库，包含产品信息、价格和库存",
            "owner": "电商团队",
            "data_type": "database",
            "location": "mongodb://products/catalog",
            "record_count": 50000,
            "tags": ["product", "inventory", "ecommerce"]
        }
    )

    # 演示搜索功能
    print("=== 数据目录系统演示 ===\n")

    print("1. 搜索包含'customer'的资产:")
    customer_assets = catalog.search_assets(query="customer")
    for asset in customer_assets:
        print(f"   - {asset['asset_id']}: {asset['description']} (所有者: {asset['owner']})")

    print("\n2. 搜索带有'sales'标签的资产:")
    sales_assets = catalog.search_assets(tags=["sales"])
    for asset in sales_assets:
        print(f"   - {asset['asset_id']}: {asset['description']} (类型: {asset['data_type']})")

    print("\n3. 搜索同时包含'customer'关键词和'sales'标签的资产:")
    combined_search = catalog.search_assets(query="customer", tags=["sales"])
    for asset in combined_search:
        print(f"   - {asset['asset_id']}: {asset['description']}")

    print("\n4. 获取客户表详细信息:")
    customer_details = catalog.get_asset_details("customer_table")
    print(json.dumps(customer_details, indent=2, ensure_ascii=False))

    print("\n5. 更新客户表元数据:")
    catalog.update_asset_metadata("customer_table", {
        "last_updated": "2023-05-01",
        "quality_score": 0.95,
        "tags": ["customer", "pii", "sales", "high_priority"]
    })
    updated_details = catalog.get_asset_details("customer_table")
    print(f"   更新后的标签: {updated_details.get('tags', [])}")
    print(f"   质量评分: {updated_details.get('quality_score', 'N/A')}")


if __name__ == "__main__":
    main()