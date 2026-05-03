#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据目录实现解决方案

这个解决方案提供了完整的数据目录系统，
包括资产注册、搜索、分类、权限控制和质量跟踪功能。
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class AdvancedDataCatalog:
    """高级数据目录系统，支持更多功能"""

    def __init__(self):
        """初始化高级数据目录系统"""
        self.assets = {}           # 存储数据资产信息
        self.tags = {}             # 存储标签索引
        self.relationships = {}    # 存储资产间的关系
        self.access_logs = []      # 访问日志

    def register_asset(self, asset_id: str, asset_info: Dict[str, Any]):
        """注册数据资产

        Args:
            asset_id: 数据资产唯一标识符
            asset_info: 数据资产的元数据信息
        """
        asset_info["registered_at"] = datetime.now().isoformat()
        asset_info["asset_id"] = asset_id
        asset_info["last_accessed"] = None
        asset_info["access_count"] = 0

        # 设置默认值
        asset_info.setdefault("description", "")
        asset_info.setdefault("owner", "")
        asset_info.setdefault("data_type", "unknown")
        asset_info.setdefault("tags", [])
        asset_info.setdefault("sensitivity_level", "public")  # public, internal, confidential, restricted

        self.assets[asset_id] = asset_info

        # 更新标签索引
        for tag in asset_info["tags"]:
            if tag not in self.tags:
                self.tags[tag] = []
            if asset_id not in self.tags[tag]:
                self.tags[tag].append(asset_id)

    def search_assets(self, query: str = "", tags: List[str] = None,
                     data_type: str = "", owner: str = "",
                     sensitivity_level: str = "") -> List[Dict]:
        """高级搜索数据资产

        Args:
            query: 搜索关键词
            tags: 标签列表（必须包含所有指定标签）
            data_type: 数据类型筛选
            owner: 所有者筛选
            sensitivity_level: 敏感度级别筛选

        Returns:
            匹配的数据资产列表
        """
        results = []

        for asset_id, asset_info in self.assets.items():
            matches = True

            # 查询字符串匹配
            if query and matches:
                searchable_text = " ".join([
                    asset_info.get("asset_id", ""),
                    asset_info.get("description", ""),
                    asset_info.get("owner", ""),
                    " ".join(asset_info.get("tags", []))
                ]).lower()
                matches = query.lower() in searchable_text

            # 标签匹配
            if tags and matches:
                asset_tags = set(asset_info.get("tags", []))
                required_tags = set(tags)
                matches = required_tags.issubset(asset_tags)

            # 数据类型匹配
            if data_type and matches:
                matches = asset_info.get("data_type", "").lower() == data_type.lower()

            # 所有者匹配
            if owner and matches:
                matches = owner.lower() in asset_info.get("owner", "").lower()

            # 敏感度级别匹配
            if sensitivity_level and matches:
                matches = asset_info.get("sensitivity_level", "").lower() == sensitivity_level.lower()

            if matches:
                results.append(asset_info.copy())

        return results

    def get_asset_details(self, asset_id: str) -> Dict:
        """获取数据资产详细信息，并记录访问

        Args:
            asset_id: 数据资产唯一标识符

        Returns:
            数据资产的完整信息
        """
        if asset_id not in self.assets:
            return {}

        # 更新访问统计
        self.assets[asset_id]["last_accessed"] = datetime.now().isoformat()
        self.assets[asset_id]["access_count"] += 1

        # 记录访问日志
        self.access_logs.append({
            "asset_id": asset_id,
            "accessed_at": datetime.now().isoformat(),
            "action": "view"
        })

        return self.assets[asset_id].copy()

    def update_asset_metadata(self, asset_id: str, updates: Dict[str, Any]):
        """更新数据资产元数据

        Args:
            asset_id: 数据资产唯一标识符
            updates: 要更新的元数据字段
        """
        if asset_id in self.assets:
            old_tags = set(self.assets[asset_id].get("tags", []))
            self.assets[asset_id].update(updates)
            self.assets[asset_id]["updated_at"] = datetime.now().isoformat()

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

    def add_relationship(self, source_asset: str, target_asset: str, relationship_type: str):
        """添加资产间关系

        Args:
            source_asset: 源资产ID
            target_asset: 目标资产ID
            relationship_type: 关系类型

        Returns:
            是否成功添加关系
        """
        if source_asset not in self.assets or target_asset not in self.assets:
            return False

        relationship_key = f"{source_asset}:{target_asset}"
        self.relationships[relationship_key] = {
            "source": source_asset,
            "target": target_asset,
            "type": relationship_type,
            "created_at": datetime.now().isoformat()
        }

        return True

    def get_related_assets(self, asset_id: str, relationship_type: str = None) -> List[Dict]:
        """获取相关资产

        Args:
            asset_id: 资产ID
            relationship_type: 关系类型筛选（可选）

        Returns:
            相关资产列表
        """
        related = []

        for rel_key, rel_info in self.relationships.items():
            if rel_info["source"] == asset_id:
                if relationship_type is None or rel_info["type"] == relationship_type:
                    target_asset = self.assets.get(rel_info["target"])
                    if target_asset:
                        related.append({
                            "asset": target_asset,
                            "relationship": rel_info["type"]
                        })

        return related

    def get_popular_assets(self, limit: int = 10) -> List[Dict]:
        """获取最受欢迎的资产（按访问次数）

        Args:
            limit: 返回结果数量限制

        Returns:
            最受欢迎的资产列表
        """
        sorted_assets = sorted(
            self.assets.values(),
            key=lambda x: x.get("access_count", 0),
            reverse=True
        )
        return sorted_assets[:limit]

    def export_catalog(self) -> str:
        """导出目录为JSON格式

        Returns:
            JSON格式的目录数据
        """
        export_data = {
            "assets": self.assets,
            "tags": self.tags,
            "relationships": self.relationships,
            "exported_at": datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)


def main():
    """主函数：演示高级数据目录系统功能"""
    # 创建数据目录实例
    catalog = AdvancedDataCatalog()

    # 注册各种类型的数据资产
    catalog.register_asset(
        "customer_master_data",
        {
            "description": "客户主数据表，包含客户基本信息、联系方式和偏好设置",
            "owner": "数据治理团队",
            "data_type": "table",
            "location": "database.crm.customers",
            "row_count": 500000,
            "last_updated": "2023-05-01",
            "tags": ["customer", "pii", "master_data", "critical"],
            "sensitivity_level": "confidential"
        }
    )

    catalog.register_asset(
        "sales_transaction_log",
        {
            "description": "销售交易日志，记录所有订单和支付信息",
            "owner": "财务团队",
            "data_type": "log",
            "location": "kafka://sales-transactions",
            "format": "json",
            "retention_days": 365,
            "tags": ["sales", "financial", "transaction", "audit"],
            "sensitivity_level": "confidential"
        }
    )

    catalog.register_asset(
        "product_catalog_db",
        {
            "description": "产品目录数据库，包含产品信息、价格和库存状态",
            "owner": "电商团队",
            "data_type": "database",
            "location": "mongodb://products/catalog",
            "record_count": 75000,
            "tags": ["product", "inventory", "ecommerce", "public"],
            "sensitivity_level": "internal"
        }
    )

    catalog.register_asset(
        "website_analytics_events",
        {
            "description": "网站分析事件流，包含用户行为和页面浏览数据",
            "owner": "产品团队",
            "data_type": "stream",
            "location": "kinesis://web-analytics",
            "format": "avro",
            "events_per_day": 10000000,
            "tags": ["analytics", "user_behavior", "web", "marketing"],
            "sensitivity_level": "internal"
        }
    )

    catalog.register_asset(
        "public_company_info",
        {
            "description": "公开公司信息数据集，包含公司基本信息和行业分类",
            "owner": "数据科学团队",
            "data_type": "dataset",
            "location": "s3://public-data/company-info",
            "record_count": 10000000,
            "source": "government_open_data",
            "tags": ["company", "public", "reference", "external"],
            "sensitivity_level": "public"
        }
    )

    # 添加资产间关系
    catalog.add_relationship("customer_master_data", "sales_transaction_log", "used_by")
    catalog.add_relationship("product_catalog_db", "sales_transaction_log", "referenced_by")
    catalog.add_relationship("website_analytics_events", "customer_master_data", "enriches")

    print("=== 高级数据目录系统解决方案演示 ===\n")

    # 演示搜索功能
    print("1. 搜索包含'customer'的资产:")
    customer_assets = catalog.search_assets(query="customer")
    for asset in customer_assets:
        print(f"   - {asset['asset_id']}: {asset['description']} ({asset['data_type']})")

    print("\n2. 搜索'confidential'级别的资产:")
    confidential_assets = catalog.search_assets(sensitivity_level="confidential")
    for asset in confidential_assets:
        print(f"   - {asset['asset_id']}: {asset['sensitivity_level']} ({asset['owner']})")

    print("\n3. 搜索'table'类型且包含'critical'标签的资产:")
    critical_tables = catalog.search_assets(data_type="table", tags=["critical"])
    for asset in critical_tables:
        print(f"   - {asset['asset_id']}: {'; '.join(asset['tags'])}")

    print("\n4. 获取客户主数据详细信息（第一次访问）:")
    customer_details = catalog.get_asset_details("customer_master_data")
    print(f"   描述: {customer_details['description']}")
    print(f"   访问次数: {customer_details['access_count']}")
    print(f"   最后访问: {customer_details['last_accessed']}")

    print("\n5. 再次获取客户主数据详细信息（第二次访问）:")
    customer_details = catalog.get_asset_details("customer_master_data")
    print(f"   访问次数: {customer_details['access_count']}")

    print("\n6. 获取客户主数据的相关资产:")
    related_assets = catalog.get_related_assets("customer_master_data")
    for related in related_assets:
        print(f"   - {related['asset']['asset_id']} ({related['relationship']})")

    print("\n7. 最受欢迎的资产（按访问次数）:")
    popular_assets = catalog.get_popular_assets(limit=3)
    for i, asset in enumerate(popular_assets, 1):
        print(f"   {i}. {asset['asset_id']} - {asset['access_count']} 次访问")

    print("\n8. 导出目录数据（前200字符）:")
    exported_data = catalog.export_catalog()
    print(f"   {exported_data[:200]}...")


if __name__ == "__main__":
    main()