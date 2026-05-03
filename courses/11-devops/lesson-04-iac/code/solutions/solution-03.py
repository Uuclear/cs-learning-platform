#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: Terraform 模块系统模拟
这是 example-03-module-system.py 的简化解决方案
"""

from typing import Dict, Any


class SimpleModule:
    """简化的模块类"""

    def __init__(self, name: str):
        self.name = name
        self.resources = []

    def add_resource(self, resource_type: str, name: str, config: Dict[str, Any]):
        """添加资源"""
        self.resources.append({
            "type": resource_type,
            "name": name,
            "config": config
        })


def create_vpc_module(vpc_name: str, cidr_block: str) -> SimpleModule:
    """创建 VPC 模块"""
    module = SimpleModule("vpc")

    module.add_resource("aws_vpc", "main", {
        "cidr_block": cidr_block,
        "tags": {"Name": vpc_name}
    })

    module.add_resource("aws_subnet", "public", {
        "vpc_id": "${aws_vpc.main.id}",
        "cidr_block": f"{cidr_block[:-3]}1.0/24"
    })

    return module


def main():
    """主函数"""
    # 创建生产环境 VPC 模块
    prod_vpc = create_vpc_module("production", "10.0.0.0/16")
    print(f"生产 VPC 模块包含 {len(prod_vpc.resources)} 个资源")

    # 创建开发环境 VPC 模块
    dev_vpc = create_vpc_module("development", "10.1.0.0/16")
    print(f"开发 VPC 模块包含 {len(dev_vpc.resources)} 个资源")


if __name__ == "__main__":
    main()