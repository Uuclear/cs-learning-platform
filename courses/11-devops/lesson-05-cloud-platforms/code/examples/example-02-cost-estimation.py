#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云成本估算示例：模拟不同工作负载在各云平台的成本计算

本示例演示如何为给定的工作负载估算在 AWS、GCP、Azure 上的月度成本，
帮助进行成本效益分析和预算规划。
"""

def calculate_aws_cost(instance_type, hours_per_month, storage_gb, data_transfer_gb):
    """
    计算 AWS 成本估算（简化模型）

    Args:
        instance_type (str): 实例类型 ('t3.micro', 'm5.large', 'c5.xlarge')
        hours_per_month (int): 每月使用小时数
        storage_gb (int): 存储容量（GB）
        data_transfer_gb (int): 数据传输量（GB）

    Returns:
        float: 估算的月度成本（美元）
    """
    # AWS 定价（简化，实际价格会变化）
    aws_pricing = {
        't3.micro': 0.0104,    # 每小时美元
        'm5.large': 0.096,     # 每小时美元
        'c5.xlarge': 0.170,    # 每小时美元
    }

    # S3 存储价格（标准存储）
    s3_storage_price = 0.023  # 每 GB 每月美元

    # 数据传输价格（出站到互联网）
    data_transfer_price = 0.09  # 每 GB 美元（前 10TB）

    # 计算各项成本
    compute_cost = aws_pricing.get(instance_type, 0) * hours_per_month
    storage_cost = storage_gb * s3_storage_price
    transfer_cost = data_transfer_gb * data_transfer_price

    total_cost = compute_cost + storage_cost + transfer_cost
    return round(total_cost, 2)

def calculate_gcp_cost(machine_type, hours_per_month, storage_gb, data_transfer_gb):
    """
    计算 GCP 成本估算（简化模型）

    Args:
        machine_type (str): 机器类型 ('e2-micro', 'n2-standard-2', 'c2-standard-4')
        hours_per_month (int): 每月使用小时数
        storage_gb (int): 存储容量（GB）
        data_transfer_gb (int): 数据传输量（GB）

    Returns:
        float: 估算的月度成本（美元）
    """
    # GCP 定价（简化）
    gcp_pricing = {
        'e2-micro': 0.0084,     # 每小时美元
        'n2-standard-2': 0.0948, # 每小时美元
        'c2-standard-4': 0.1704, # 每小时美元
    }

    # Cloud Storage 价格（标准存储）
    storage_price = 0.020  # 每 GB 每月美元

    # 数据传输价格
    transfer_price = 0.12  # 每 GB 美元（前 1TB）

    compute_cost = gcp_pricing.get(machine_type, 0) * hours_per_month
    storage_cost = storage_gb * storage_price
    transfer_cost = data_transfer_gb * transfer_price

    total_cost = compute_cost + storage_cost + transfer_cost
    return round(total_cost, 2)

def calculate_azure_cost(vm_size, hours_per_month, storage_gb, data_transfer_gb):
    """
    计算 Azure 成本估算（简化模型）

    Args:
        vm_size (str): 虚拟机大小 ('B1s', 'D2s v3', 'F4s v2')
        hours_per_month (int): 每月使用小时数
        storage_gb (int): 存储容量（GB）
        data_transfer_gb (int): 数据传输量（GB）

    Returns:
        float: 估算的月度成本（美元）
    """
    # Azure 定价（简化）
    azure_pricing = {
        'B1s': 0.0072,      # 每小时美元
        'D2s v3': 0.096,    # 每小时美元
        'F4s v2': 0.168,    # 每小时美元
    }

    # Blob Storage 价格（热存储）
    storage_price = 0.0184  # 每 GB 每月美元

    # 数据传输价格
    transfer_price = 0.087  # 每 GB 美元（前 5TB）

    compute_cost = azure_pricing.get(vm_size, 0) * hours_per_month
    storage_cost = storage_gb * storage_price
    transfer_cost = data_transfer_gb * transfer_price

    total_cost = compute_cost + storage_cost + transfer_cost
    return round(total_cost, 2)

def compare_cloud_costs(workload_config):
    """
    比较三大云平台的成本

    Args:
        workload_config (dict): 工作负载配置字典
    """
    print("云平台成本估算对比")
    print("=" * 50)

    # 提取工作负载参数
    hours = workload_config['hours_per_month']
    storage = workload_config['storage_gb']
    transfer = workload_config['data_transfer_gb']

    print(f"工作负载配置:")
    print(f"- 每月使用时间: {hours} 小时")
    print(f"- 存储需求: {storage} GB")
    print(f"- 数据传输: {transfer} GB")
    print()

    # 计算各平台成本
    aws_cost = calculate_aws_cost(
        workload_config['aws_instance'],
        hours, storage, transfer
    )

    gcp_cost = calculate_gcp_cost(
        workload_config['gcp_machine'],
        hours, storage, transfer
    )

    azure_cost = calculate_azure_cost(
        workload_config['azure_vm'],
        hours, storage, transfer
    )

    # 显示结果
    print("成本估算结果（美元/月）:")
    print(f"AWS:    ${aws_cost}")
    print(f"GCP:    ${gcp_cost}")
    print(f"Azure:  ${azure_cost}")

    # 找出最低成本
    costs = {'AWS': aws_cost, 'GCP': gcp_cost, 'Azure': azure_cost}
    cheapest = min(costs, key=costs.get)
    print(f"\n最低成本平台: {cheapest} (${costs[cheapest]})")

def main():
    """主函数：演示成本估算功能"""
    # 示例工作负载配置
    web_app_workload = {
        'description': '中小型 Web 应用',
        'hours_per_month': 730,  # 24/7 运行
        'storage_gb': 100,
        'data_transfer_gb': 500,
        'aws_instance': 't3.micro',
        'gcp_machine': 'e2-micro',
        'azure_vm': 'B1s'
    }

    database_workload = {
        'description': '数据库服务器',
        'hours_per_month': 730,
        'storage_gb': 500,
        'data_transfer_gb': 200,
        'aws_instance': 'm5.large',
        'gcp_machine': 'n2-standard-2',
        'azure_vm': 'D2s v3'
    }

    # 比较不同工作负载
    print("场景 1: Web 应用")
    compare_cloud_costs(web_app_workload)
    print("\n" + "="*50 + "\n")

    print("场景 2: 数据库服务器")
    compare_cloud_costs(database_workload)

    print("\n注意: 这些是简化估算，实际成本可能因地区、折扣、")
    print("预留实例等因素而有所不同。建议使用官方定价计算器。")

if __name__ == "__main__":
    main()