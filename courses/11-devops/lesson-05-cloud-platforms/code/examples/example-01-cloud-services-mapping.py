#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务映射示例：展示 AWS、GCP、Azure 中等效服务的对应关系

本示例演示如何创建一个映射表，将三大云平台的核心服务进行对应，
帮助开发者和架构师在不同平台间进行快速转换和比较。
"""

def get_cloud_service_mapping():
    """
    返回三大云平台核心服务的映射字典

    Returns:
        dict: 包含服务类别和各平台对应服务的嵌套字典
    """
    # 定义云服务映射表
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
        }
    }
    return service_mapping

def display_service_comparison(service_category):
    """
    显示指定服务类别的跨平台对比

    Args:
        service_category (str): 服务类别名称，如"计算服务"、"对象存储"等
    """
    mapping = get_cloud_service_mapping()

    if service_category not in mapping:
        print(f"错误：未找到服务类别 '{service_category}'")
        print("可用的服务类别：", list(mapping.keys()))
        return

    services = mapping[service_category]
    print(f"\n=== {service_category} 对比 ===")
    print(f"AWS:    {services['AWS']}")
    print(f"GCP:    {services['GCP']}")
    print(f"Azure:  {services['Azure']}")
    print("=" * 40)

def main():
    """主函数：演示云服务映射功能"""
    print("云平台服务映射演示")
    print("展示 AWS、GCP、Azure 核心服务的对应关系\n")

    # 获取所有服务类别
    mapping = get_cloud_service_mapping()
    categories = list(mapping.keys())

    # 显示前几个服务类别的对比
    for category in categories[:4]:
        display_service_comparison(category)

    print(f"\n总共支持 {len(categories)} 个服务类别的映射")
    print("您可以根据需要扩展此映射表以包含更多服务")

if __name__ == "__main__":
    main()