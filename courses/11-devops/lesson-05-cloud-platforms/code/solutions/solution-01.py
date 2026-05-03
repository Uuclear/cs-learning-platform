#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: 云服务映射

这个解决方案扩展了示例中的功能，添加了更多的服务类别和搜索功能。
"""

def get_extended_cloud_service_mapping():
    """
    返回扩展的云服务映射字典，包含更多服务类别

    Returns:
        dict: 扩展的服务映射
    """
    service_mapping = {
        "计算服务": {
            "AWS": "EC2 (Elastic Compute Cloud)",
            "GCP": "Compute Engine",
            "Azure": "Virtual Machines"
        },
        "无服务器函数": {
            "AWS": "Lambda",
            "GCP": "Cloud Functions",
            "Azure": "Functions"
        },
        "对象存储": {
            "AWS": "S3 (Simple Storage Service)",
            "GCP": "Cloud Storage",
            "Azure": "Blob Storage"
        },
        "块存储": {
            "AWS": "EBS (Elastic Block Store)",
            "GCP": "Persistent Disks",
            "Azure": "Managed Disks"
        },
        "关系型数据库": {
            "AWS": "RDS (Relational Database Service)",
            "GCP": "Cloud SQL",
            "Azure": "SQL Database"
        },
        "NoSQL 数据库": {
            "AWS": "DynamoDB",
            "GCP": "Firestore/Bigtable",
            "Azure": "Cosmos DB"
        },
        "身份认证": {
            "AWS": "IAM (Identity and Access Management)",
            "GCP": "Cloud IAM",
            "Azure": "Azure AD (Active Directory)"
        },
        "容器服务": {
            "AWS": "ECS/EKS (Elastic Container Service/Kubernetes)",
            "GCP": "GKE (Google Kubernetes Engine)",
            "Azure": "AKS (Azure Kubernetes Service)"
        },
        "消息队列": {
            "AWS": "SQS/SNS (Simple Queue/Notification Service)",
            "GCP": "Pub/Sub",
            "Azure": "Service Bus"
        },
        "监控服务": {
            "AWS": "CloudWatch",
            "GCP": "Cloud Monitoring",
            "Azure": "Application Insights"
        },
        "日志服务": {
            "AWS": "CloudTrail/CloudWatch Logs",
            "GCP": "Cloud Logging",
            "Azure": "Log Analytics"
        },
        "CDN 服务": {
            "AWS": "CloudFront",
            "GCP": "Cloud CDN",
            "Azure": "Azure CDN"
        }
    }
    return service_mapping

def search_service_by_name(service_name):
    """
    根据服务名称搜索跨平台对应关系

    Args:
        service_name (str): 服务名称关键词

    Returns:
        dict: 匹配的服务信息
    """
    mapping = get_extended_cloud_service_mapping()
    results = {}

    for category, services in mapping.items():
        for provider, service in services.items():
            if service_name.lower() in service.lower():
                if category not in results:
                    results[category] = {}
                results[category][provider] = service

    return results

def main():
    """主函数：演示扩展功能"""
    print("扩展版云服务映射解决方案")
    print("=" * 40)

    # 显示所有服务类别
    mapping = get_extended_cloud_service_mapping()
    print(f"支持 {len(mapping)} 个服务类别:")
    for i, category in enumerate(mapping.keys(), 1):
        print(f"{i}. {category}")

    print("\n搜索示例:")
    search_results = search_service_by_name("kubernetes")
    if search_results:
        for category, services in search_results.items():
            print(f"\n{category}:")
            for provider, service in services.items():
                print(f"  {provider}: {service}")
    else:
        print("未找到匹配的服务")

if __name__ == "__main__":
    main()