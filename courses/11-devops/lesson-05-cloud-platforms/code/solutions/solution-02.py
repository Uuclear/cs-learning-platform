#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02: 高级成本估算

这个解决方案添加了更多定价因素，包括预留实例、地区差异和折扣。
"""

def calculate_advanced_aws_cost(config):
    """
    计算 AWS 高级成本估算

    Args:
        config (dict): 完整的配置字典

    Returns:
        dict: 详细的成本分解
    """
    # 基础定价（简化）
    base_prices = {
        'compute': {
            't3.micro': 0.0104,
            'm5.large': 0.096,
            'c5.xlarge': 0.170
        },
        'storage': {
            's3_standard': 0.023,
            's3_infrequent': 0.0125,
            'ebs_gp2': 0.10
        },
        'transfer': 0.09
    }

    # 计算各项成本
    compute_hours = config.get('compute_hours', 730)
    compute_type = config.get('compute_type', 't3.micro')
    storage_gb = config.get('storage_gb', 100)
    storage_type = config.get('storage_type', 's3_standard')
    transfer_gb = config.get('transfer_gb', 100)

    compute_cost = base_prices['compute'][compute_type] * compute_hours
    storage_cost = base_prices['storage'][storage_type] * storage_gb
    transfer_cost = base_prices['transfer'] * transfer_gb

    # 应用预留实例折扣（如果适用）
    reserved_discount = config.get('reserved_discount', 0)
    if reserved_discount > 0:
        compute_cost *= (1 - reserved_discount)

    # 应用区域价格差异
    region_multiplier = config.get('region_multiplier', 1.0)
    total_cost = (compute_cost + storage_cost + transfer_cost) * region_multiplier

    return {
        'compute': round(compute_cost, 2),
        'storage': round(storage_cost, 2),
        'transfer': round(transfer_cost, 2),
        'total': round(total_cost, 2),
        'discount_applied': reserved_discount > 0,
        'region_factor': region_multiplier
    }

def calculate_advanced_gcp_cost(config):
    """
    计算 GCP 高级成本估算

    Args:
        config (dict): 完整的配置字典

    Returns:
        dict: 详细的成本分解
    """
    base_prices = {
        'compute': {
            'e2-micro': 0.0084,
            'n2-standard-2': 0.0948,
            'c2-standard-4': 0.1704
        },
        'storage': {
            'standard': 0.020,
            'nearline': 0.010,
            'coldline': 0.004
        },
        'transfer': 0.12
    }

    compute_hours = config.get('compute_hours', 730)
    compute_type = config.get('compute_type', 'e2-micro')
    storage_gb = config.get('storage_gb', 100)
    storage_class = config.get('storage_class', 'standard')
    transfer_gb = config.get('transfer_gb', 100)

    compute_cost = base_prices['compute'][compute_type] * compute_hours
    storage_cost = base_prices['storage'][storage_class] * storage_gb
    transfer_cost = base_prices['transfer'] * transfer_gb

    # GCP 自动持续使用折扣
    sustained_discount = min(compute_hours / 730 * 0.3, 0.3)  # 最多 30% 折扣
    compute_cost *= (1 - sustained_discount)

    region_multiplier = config.get('region_multiplier', 1.0)
    total_cost = (compute_cost + storage_cost + transfer_cost) * region_multiplier

    return {
        'compute': round(compute_cost, 2),
        'storage': round(storage_cost, 2),
        'transfer': round(transfer_cost, 2),
        'total': round(total_cost, 2),
        'sustained_discount': round(sustained_discount, 3),
        'region_factor': region_multiplier
    }

def calculate_advanced_azure_cost(config):
    """
    计算 Azure 高级成本估算

    Args:
        config (dict): 完整的配置字典

    Returns:
        dict: 详细的成本分解
    """
    base_prices = {
        'compute': {
            'B1s': 0.0072,
            'D2s v3': 0.096,
            'F4s v2': 0.168
        },
        'storage': {
            'hot': 0.0184,
            'cool': 0.0121,
            'archive': 0.00099
        },
        'transfer': 0.087
    }

    compute_hours = config.get('compute_hours', 730)
    compute_size = config.get('compute_size', 'B1s')
    storage_gb = config.get('storage_gb', 100)
    storage_tier = config.get('storage_tier', 'hot')
    transfer_gb = config.get('transfer_gb', 100)

    compute_cost = base_prices['compute'][compute_size] * compute_hours
    storage_cost = base_prices['storage'][storage_tier] * storage_gb
    transfer_cost = base_prices['transfer'] * transfer_gb

    # Azure 预留实例折扣
    reserved_discount = config.get('reserved_discount', 0)
    if reserved_discount > 0:
        compute_cost *= (1 - reserved_discount)

    # 混合权益折扣（如果适用）
    hybrid_benefit = config.get('hybrid_benefit', False)
    if hybrid_benefit and 'windows' in compute_size.lower():
        compute_cost *= 0.65  # 大约 35% 折扣

    region_multiplier = config.get('region_multiplier', 1.0)
    total_cost = (compute_cost + storage_cost + transfer_cost) * region_multiplier

    return {
        'compute': round(compute_cost, 2),
        'storage': round(storage_cost, 2),
        'transfer': round(transfer_cost, 2),
        'total': round(total_cost, 2),
        'reserved_discount': reserved_discount,
        'hybrid_benefit_applied': hybrid_benefit,
        'region_factor': region_multiplier
    }

def advanced_cost_comparison(workload_configs):
    """
    高级成本比较功能

    Args:
        workload_configs (list): 工作负载配置列表
    """
    for i, config in enumerate(workload_configs, 1):
        print(f"\n=== 工作负载 {i}: {config.get('name', '未命名')} ===")

        aws_result = calculate_advanced_aws_cost(config)
        gcp_result = calculate_advanced_gcp_cost(config)
        azure_result = calculate_advanced_azure_cost(config)

        print(f"AWS 总成本: ${aws_result['total']} "
              f"(计算: ${aws_result['compute']}, 存储: ${aws_result['storage']})")
        print(f"GCP 总成本: ${gcp_result['total']} "
              f"(计算: ${gcp_result['compute']}, 存储: ${gcp_result['storage']})")
        print(f"Azure 总成本: ${azure_result['total']} "
              f"(计算: ${azure_result['compute']}, 存储: ${azure_result['storage']})")

        costs = [aws_result['total'], gcp_result['total'], azure_result['total']]
        providers = ['AWS', 'GCP', 'Azure']
        cheapest = providers[costs.index(min(costs))]
        print(f"最低成本: {cheapest} (${min(costs)})")

def main():
    """主函数：演示高级成本估算"""
    print("高级云成本估算解决方案")
    print("包含预留实例、地区差异和自动折扣\n")

    # 定义复杂的工作负载
    workloads = [
        {
            'name': '生产 Web 应用 (预留实例)',
            'compute_hours': 730,
            'compute_type': 'm5.large',
            'storage_gb': 500,
            'storage_type': 's3_standard',
            'transfer_gb': 1000,
            'reserved_discount': 0.4,  # 40% 预留折扣
            'region_multiplier': 1.0
        },
        {
            'name': '开发环境 (按需付费)',
            'compute_hours': 200,
            'compute_type': 't3.micro',
            'storage_gb': 50,
            'storage_type': 's3_infrequent',
            'transfer_gb': 100,
            'reserved_discount': 0,
            'region_multiplier': 0.9  # 开发区域价格较低
        }
    ]

    advanced_cost_comparison(workloads)

    print("\n注意: 实际成本估算应使用官方定价计算器，")
    print("并考虑所有相关因素如支持计划、数据传输模式等。")

if __name__ == "__main__":
    main()