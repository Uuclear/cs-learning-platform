#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：完整的Mermaid图表生成器

这个解决方案扩展了示例2的功能，支持状态图生成、
从JSON配置文件读取图表定义，并添加了错误处理和验证。
"""

import json
import os
from typing import Dict, List, Any, Optional


class MermaidGenerator:
    """Mermaid图表生成器类"""

    def __init__(self):
        self.supported_types = ['class', 'sequence', 'flowchart', 'state']

    def generate_from_config(self, config_file: str) -> str:
        """
        从JSON配置文件生成Mermaid图表

        参数:
            config_file: JSON配置文件路径

        返回:
            Mermaid图表代码字符串

        异常:
            FileNotFoundError: 配置文件不存在
            ValueError: 配置格式无效
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON格式错误: {e}")

        chart_type = config.get('type')
        if chart_type not in self.supported_types:
            raise ValueError(f"不支持的图表类型: {chart_type}. 支持的类型: {self.supported_types}")

        if chart_type == 'class':
            return self.generate_class_diagram(config['data'])
        elif chart_type == 'sequence':
            return self.generate_sequence_diagram(config['data'])
        elif chart_type == 'flowchart':
            return self.generate_flowchart(config['data']['nodes'], config['data']['edges'])
        elif chart_type == 'state':
            return self.generate_state_diagram(config['data'])

        raise ValueError(f"未知的图表类型: {chart_type}")

    def generate_class_diagram(self, classes: Dict[str, List[str]]) -> str:
        """根据类定义生成Mermaid类图"""
        self._validate_class_data(classes)

        mermaid = "classDiagram\n"
        for class_name, methods in classes.items():
            mermaid += f"    class {class_name} {{\n"
            for method in methods:
                mermaid += f"        +{method}\n"
            mermaid += "    }\n"

        return mermaid

    def generate_sequence_diagram(self, steps: List[Dict[str, str]]) -> str:
        """根据步骤列表生成Mermaid序列图"""
        self._validate_sequence_data(steps)

        mermaid = "sequenceDiagram\n"
        participants = set()

        for step in steps:
            participants.add(step["actor"])
            participants.add(step["target"])

        for participant in sorted(participants):
            mermaid += f"    participant {participant}\n"

        for step in steps:
            mermaid += f"    {step['actor']}->{step['target']}: {step['action']}\n"

        return mermaid

    def generate_flowchart(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> str:
        """根据节点和边定义生成Mermaid流程图"""
        self._validate_flowchart_data(nodes, edges)

        mermaid = "flowchart TD\n"

        for node in nodes:
            mermaid += f"    {node['id']}[{node['label']}]\n"

        for edge in edges:
            if edge.get("label"):
                mermaid += f"    {edge['from']} -->|{edge['label']}| {edge['to']}\n"
            else:
                mermaid += f"    {edge['from']} --> {edge['to']}\n"

        return mermaid

    def generate_state_diagram(self, states: List[Dict[str, Any]]) -> str:
        """根据状态定义生成Mermaid状态图"""
        self._validate_state_data(states)

        mermaid = "stateDiagram-v2\n"

        # 添加状态定义
        for state in states:
            state_id = state['id']
            state_label = state.get('label', state_id)

            if 'transitions' in state:
                # 复杂状态（有子状态或转换）
                mermaid += f"    state {state_id} {{\n"
                for transition in state['transitions']:
                    target = transition['target']
                    trigger = transition.get('trigger', '')
                    if trigger:
                        mermaid += f"        {state_id} --> {target}: {trigger}\n"
                    else:
                        mermaid += f"        {state_id} --> {target}\n"
                mermaid += "    }\n"
            else:
                # 简单状态
                if state_id != state_label:
                    mermaid += f"    {state_id}: {state_label}\n"
                else:
                    mermaid += f"    {state_id}\n"

        # 添加全局转换
        for state in states:
            if 'outgoing' in state:
                for outgoing in state['outgoing']:
                    source = state['id']
                    target = outgoing['target']
                    trigger = outgoing.get('trigger', '')
                    if trigger:
                        mermaid += f"    {source} --> {target}: {trigger}\n"
                    else:
                        mermaid += f"    {source} --> {target}\n"

        return mermaid

    def _validate_class_data(self, data: Dict[str, List[str]]) -> None:
        """验证类图数据"""
        if not isinstance(data, dict):
            raise ValueError("类图数据必须是字典")

        for class_name, methods in data.items():
            if not isinstance(methods, list):
                raise ValueError(f"类 {class_name} 的方法必须是列表")
            for method in methods:
                if not isinstance(method, str):
                    raise ValueError(f"方法名必须是字符串: {method}")

    def _validate_sequence_data(self, data: List[Dict[str, str]]) -> None:
        """验证序列图数据"""
        if not isinstance(data, list):
            raise ValueError("序列图数据必须是列表")

        for i, step in enumerate(data):
            if not isinstance(step, dict):
                raise ValueError(f"步骤 {i} 必须是字典")
            if 'actor' not in step or 'target' not in step or 'action' not in step:
                raise ValueError(f"步骤 {i} 缺少必需字段 (actor, target, action)")

    def _validate_flowchart_data(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> None:
        """验证流程图数据"""
        if not isinstance(nodes, list) or not isinstance(edges, list):
            raise ValueError("流程图数据必须包含节点和边的列表")

        node_ids = set()
        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                raise ValueError(f"节点 {i} 必须是字典")
            if 'id' not in node or 'label' not in node:
                raise ValueError(f"节点 {i} 缺少必需字段 (id, label)")
            node_ids.add(node['id'])

        for i, edge in enumerate(edges):
            if not isinstance(edge, dict):
                raise ValueError(f"边 {i} 必须是字典")
            if 'from' not in edge or 'to' not in edge:
                raise ValueError(f"边 {i} 缺少必需字段 (from, to)")
            if edge['from'] not in node_ids or edge['to'] not in node_ids:
                raise ValueError(f"边 {i} 引用了不存在的节点")

    def _validate_state_data(self, data: List[Dict[str, Any]]) -> None:
        """验证状态图数据"""
        if not isinstance(data, list):
            raise ValueError("状态图数据必须是列表")

        for i, state in enumerate(data):
            if not isinstance(state, dict):
                raise ValueError(f"状态 {i} 必须是字典")
            if 'id' not in state:
                raise ValueError(f"状态 {i} 缺少必需字段 (id)")


def create_sample_configs():
    """创建示例配置文件"""
    configs = {
        'class.json': {
            'type': 'class',
            'data': {
                'User': ['+login()', '+logout()', '+getProfile()'],
                'Database': ['+connect()', '+query()', '+close()']
            }
        },
        'sequence.json': {
            'type': 'sequence',
            'data': [
                {'actor': 'User', 'target': 'API', 'action': '发送请求'},
                {'actor': 'API', 'target': 'Database', 'action': '查询数据'}
            ]
        },
        'flowchart.json': {
            'type': 'flowchart',
            'data': {
                'nodes': [
                    {'id': 'A', 'label': '开始'},
                    {'id': 'B', 'label': '处理'},
                    {'id': 'C', 'label': '结束'}
                ],
                'edges': [
                    {'from': 'A', 'to': 'B'},
                    {'from': 'B', 'to': 'C'}
                ]
            }
        },
        'state.json': {
            'type': 'state',
            'data': [
                {'id': 'Idle', 'label': '空闲状态'},
                {'id': 'Active', 'label': '活跃状态'},
                {'id': 'Error', 'label': '错误状态'},
                {
                    'id': 'Processing',
                    'transitions': [
                        {'target': 'Complete', 'trigger': '完成'},
                        {'target': 'Error', 'trigger': '失败'}
                    ]
                }
            ]
        }
    }

    os.makedirs('config_samples', exist_ok=True)
    for filename, config in configs.items():
        with open(f'config_samples/{filename}', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # 创建示例配置
    create_sample_configs()
    print("示例配置文件已创建在 config_samples/ 目录中")

    # 测试图表生成
    generator = MermaidGenerator()

    try:
        # 测试类图
        class_chart = generator.generate_from_config('config_samples/class.json')
        print("\n类图示例:")
        print(class_chart)

        # 测试序列图
        sequence_chart = generator.generate_from_config('config_samples/sequence.json')
        print("\n序列图示例:")
        print(sequence_chart)

        # 测试流程图
        flowchart = generator.generate_from_config('config_samples/flowchart.json')
        print("\n流程图示例:")
        print(flowchart)

        # 测试状态图
        state_chart = generator.generate_from_config('config_samples/state.json')
        print("\n状态图示例:")
        print(state_chart)

    except (FileNotFoundError, ValueError) as e:
        print(f"错误: {e}")