#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：图表即代码 - Mermaid图表生成器

这个脚本演示了如何使用Python数据结构生成Mermaid图表代码。
Mermaid是一种流行的图表即代码工具，支持类图、序列图、流程图等多种图表类型。
通过将图表定义存储为Python数据结构，我们可以动态生成和修改图表。
"""

from typing import Dict, List, Any


def generate_class_diagram(classes: Dict[str, List[str]]) -> str:
    """
    根据类定义生成Mermaid类图

    参数:
        classes: 字典，键为类名，值为方法列表

    返回:
        Mermaid类图的代码字符串
    """
    # 初始化Mermaid类图
    mermaid = "classDiagram\n"

    # 遍历每个类定义
    for class_name, methods in classes.items():
        # 添加类定义
        mermaid += f"    class {class_name} {{\n"
        # 添加方法
        for method in methods:
            mermaid += f"        +{method}\n"
        mermaid += "    }\n"

    return mermaid


def generate_sequence_diagram(steps: List[Dict[str, str]]) -> str:
    """
    根据步骤列表生成Mermaid序列图

    参数:
        steps: 步骤列表，每个步骤包含actor、target和action字段

    返回:
        Mermaid序列图的代码字符串
    """
    # 初始化Mermaid序列图
    mermaid = "sequenceDiagram\n"
    participants = set()

    # 收集所有参与者
    for step in steps:
        participants.add(step["actor"])
        participants.add(step["target"])

    # 添加参与者声明
    for participant in sorted(participants):
        mermaid += f"    participant {participant}\n"

    # 添加交互步骤
    for step in steps:
        mermaid += f"    {step['actor']}->{step['target']}: {step['action']}\n"

    return mermaid


def generate_flowchart(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> str:
    """
    根据节点和边定义生成Mermaid流程图

    参数:
        nodes: 节点列表，每个节点包含id和label字段
        edges: 边列表，每个边包含from、to和label字段

    返回:
        Mermaid流程图的代码字符串
    """
    # 初始化Mermaid流程图
    mermaid = "flowchart TD\n"

    # 添加节点定义
    for node in nodes:
        mermaid += f"    {node['id']}[{node['label']}]\n"

    # 添加边定义
    for edge in edges:
        if edge.get("label"):
            mermaid += f"    {edge['from']} -->|{edge['label']}| {edge['to']}\n"
        else:
            mermaid += f"    {edge['from']} --> {edge['to']}\n"

    return mermaid


if __name__ == "__main__":
    # 演示类图生成
    class_data = {
        "User": ["+login()", "+logout()", "+getProfile()"],
        "Database": ["+connect()", "+query()", "+close()"],
        "API": ["+handleRequest()", "+validateToken()", "+sendResponse()"]
    }
    print("类图示例:")
    print(generate_class_diagram(class_data))
    print("\n" + "="*50 + "\n")

    # 演示序列图生成
    sequence_steps = [
        {"actor": "User", "target": "API", "action": "发送登录请求"},
        {"actor": "API", "target": "Database", "action": "验证用户凭证"},
        {"actor": "Database", "target": "API", "action": "返回验证结果"},
        {"actor": "API", "target": "User", "action": "返回登录响应"}
    ]
    print("序列图示例:")
    print(generate_sequence_diagram(sequence_steps))
    print("\n" + "="*50 + "\n")

    # 演示流程图生成
    flow_nodes = [
        {"id": "A", "label": "开始"},
        {"id": "B", "label": "处理请求"},
        {"id": "C", "label": "验证成功?"},
        {"id": "D", "label": "返回成功"},
        {"id": "E", "label": "返回错误"},
        {"id": "F", "label": "结束"}
    ]
    flow_edges = [
        {"from": "A", "to": "B"},
        {"from": "B", "to": "C"},
        {"from": "C", "to": "D", "label": "是"},
        {"from": "C", "to": "E", "label": "否"},
        {"from": "D", "to": "F"},
        {"from": "E", "to": "F"}
    ]
    print("流程图示例:")
    print(generate_flowchart(flow_nodes, flow_edges))