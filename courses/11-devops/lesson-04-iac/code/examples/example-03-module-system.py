#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: Terraform 模块系统模拟
模拟 Terraform 的模块化基础设施组件
"""

from typing import Dict, List, Any
import json


class Module:
    """Terraform 模块 - 可重用的基础设施组件"""

    def __init__(self, name: str, variables: Dict[str, Any] = None):
        self.name = name
        self.variables = variables or {}
        self.resources = []
        self.outputs = {}

    def add_resource(self, resource_type: str, resource_name: str, config: Dict[str, Any]):
        """向模块添加资源"""
        resource = {
            "type": resource_type,
            "name": resource_name,
            "config": config
        }
        self.resources.append(resource)

    def set_output(self, name: str, value: Any):
        """设置模块输出"""
        self.outputs[name] = value

    def render(self) -> Dict[str, Any]:
        """渲染模块为 Terraform 配置格式"""
        return {
            "module": self.name,
            "resources": self.resources,
            "outputs": self.outputs,
            "variables": self.variables
        }


class ModuleRegistry:
    """模块注册表 - 管理可重用模块"""

    def __init__(self):
        self.modules: Dict[str, Module] = {}

    def register_module(self, module: Module):
        """注册模块"""
        self.modules[module.name] = module

    def get_module(self, name: str) -> Module:
        """获取模块"""
        if name not in self.modules:
            raise ValueError(f"模块 '{name}' 未找到")
        return self.modules[name].render()


class InfrastructureComposer:
    """基础设施编排器 - 组合多个模块"""

    def __init__(self, registry: ModuleRegistry):
        self.registry = registry
        self.composed_infrastructure = []

    def compose_vpc_module(self, vpc_name: str, cidr_block: str, region: str = "us-east-1"):
        """组合 VPC 模块"""
        vpc_module = Module("vpc", {
            "name": vpc_name,
            "cidr_block": cidr_block,
            "region": region
        })

        # 添加 VPC 资源
        vpc_module.add_resource("aws_vpc", "main", {
            "cidr_block": cidr_block,
            "tags": {"Name": vpc_name}
        })

        # 添加子网资源
        vpc_module.add_resource("aws_subnet", "public", {
            "vpc_id": "${aws_vpc.main.id}",
            "cidr_block": f"{cidr_block[:-3]}1.0/24",
            "availability_zone": f"{region}a"
        })

        vpc_module.add_resource("aws_subnet", "private", {
            "vpc_id": "${aws_vpc.main.id}",
            "cidr_block": f"{cidr_block[:-3]}2.0/24",
            "availability_zone": f"{region}b"
        })

        # 设置输出
        vpc_module.set_output("vpc_id", "${aws_vpc.main.id}")
        vpc_module.set_output("public_subnet_id", "${aws_subnet.public.id}")
        vpc_module.set_output("private_subnet_id", "${aws_subnet.private.id}")

        self.composed_infrastructure.append(vpc_module.render())

    def compose_web_server_module(self, app_name: str, instance_type: str = "t2.micro"):
        """组合 Web 服务器模块"""
        web_module = Module("web_server", {
            "app_name": app_name,
            "instance_type": instance_type
        })

        # 添加安全组
        web_module.add_resource("aws_security_group", "web", {
            "name": f"{app_name}-sg",
            "description": f"Security group for {app_name}",
            "ingress": [
                {"from_port": 80, "to_port": 80, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]},
                {"from_port": 22, "to_port": 22, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]}
            ]
        })

        # 添加 EC2 实例
        web_module.add_resource("aws_instance", "web", {
            "ami": "ami-0c02fb55956c7d316",  # Amazon Linux 2
            "instance_type": instance_type,
            "vpc_security_group_ids": ["${aws_security_group.web.id}"],
            "tags": {"Name": app_name}
        })

        # 设置输出
        web_module.set_output("instance_id", "${aws_instance.web.id}")
        web_module.set_output("public_ip", "${aws_instance.web.public_ip}")

        self.composed_infrastructure.append(web_module.render())

    def render_composition(self) -> str:
        """渲染完整的基础设施组合"""
        return json.dumps(self.composed_infrastructure, indent=2, ensure_ascii=False)


def main():
    """主函数 - 演示模块化基础设施"""
    print("🏗️  Terraform 模块系统模拟器")
    print("本示例演示了如何使用模块创建可重用的基础设施组件\n")

    # 创建模块注册表
    registry = ModuleRegistry()

    # 创建并注册基础模块（在真实 Terraform 中，这些会是预定义的模块）
    base_vpc = Module("base_vpc")
    base_vpc.add_resource("aws_vpc", "main", {"cidr_block": "${var.cidr_block}"})
    registry.register_module(base_vpc)

    # 创建基础设施编排器
    composer = InfrastructureComposer(registry)

    # 组合生产环境基础设施
    print("=== 组合生产环境 ===")
    composer.compose_vpc_module("production-vpc", "10.0.0.0/16", "us-west-2")
    composer.compose_web_server_module("production-web", "t3.medium")

    # 组合开发环境基础设施
    print("=== 组合开发环境 ===")
    composer.compose_vpc_module("development-vpc", "10.1.0.0/16", "us-west-2")
    composer.compose_web_server_module("development-web", "t2.micro")

    # 渲染完整配置
    print("\n=== 渲染的基础设施配置 ===")
    config = composer.render_composition()
    print(config)

    print("\n✅ 模块化基础设施组合完成!")
    print("\n关键优势:")
    print("- 复用性: 相同的模块可用于不同环境")
    print("- 一致性: 所有环境使用相同的配置模式")
    print("- 可维护性: 修改模块会影响所有使用它的环境")
    print("- 抽象化: 隐藏复杂性，提供简单接口")


if __name__ == "__main__":
    main()