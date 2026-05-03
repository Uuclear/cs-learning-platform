#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：电路板故障树诊断（基于症状推断可能原因）

这个脚本实现了一个简单的专家系统，可以根据用户描述的症状
推断可能的故障原因并提供诊断建议。
"""

from typing import Dict, List, Set


class CircuitFaultDiagnosis:
    """基于症状的电路故障诊断系统"""

    def __init__(self):
        # 故障知识库：症状 -> 可能原因和诊断步骤
        self.knowledge_base = {
            "no_power": {
                "possible_causes": ["电源适配器故障", "保险丝熔断", "电源开关损坏", "电源输入端子松动"],
                "diagnostic_steps": [
                    "检查电源适配器输出",
                    "测量保险丝两端电阻",
                    "检查电源开关通断",
                    "检查电源输入连接"
                ]
            },
            "intermittent_operation": {
                "possible_causes": ["虚焊", "接触不良", "电容老化", "温度敏感元件"],
                "diagnostic_steps": [
                    "轻敲电路板观察现象",
                    "检查所有连接器",
                    "测量关键电容ESR值",
                    "加热可疑区域测试"
                ]
            },
            "overheating": {
                "possible_causes": ["短路", "负载过大", "散热不良", "元件击穿"],
                "diagnostic_steps": [
                    "断电检查短路",
                    "测量工作电流",
                    "检查散热片安装",
                    "替换发热元件测试"
                ]
            },
            "no_signal_output": {
                "possible_causes": ["输入信号缺失", "放大器损坏", "耦合电容开路", "偏置电路故障"],
                "diagnostic_steps": [
                    "确认输入信号存在",
                    "测量放大器供电",
                    "检查耦合电容",
                    "测量偏置点电压"
                ]
            },
            "distorted_output": {
                "possible_causes": ["偏置点漂移", "反馈网络故障", "电源纹波过大", "元件参数漂移"],
                "diagnostic_steps": [
                    "测量偏置点电压",
                    "检查反馈电阻/电容",
                    "用示波器观察电源纹波",
                    "替换可疑元件测试"
                ]
            },
            "excessive_noise": {
                "possible_causes": ["接地不良", "屏蔽失效", "电源滤波不足", "高阻抗节点干扰"],
                "diagnostic_steps": [
                    "检查接地连接",
                    "检查屏蔽层完整性",
                    "增加电源滤波电容",
                    "缩短高阻抗走线"
                ]
            }
        }

    def diagnose(self, symptoms: List[str]) -> Dict:
        """根据症状进行诊断

        Args:
            symptoms: 症状列表（使用知识库中的关键词）

        Returns:
            诊断结果字典
        """
        possible_causes: Set[str] = set()
        diagnostic_steps: List[str] = []

        for symptom in symptoms:
            if symptom in self.knowledge_base:
                causes = self.knowledge_base[symptom]["possible_causes"]
                steps = self.knowledge_base[symptom]["diagnostic_steps"]
                possible_causes.update(causes)
                diagnostic_steps.extend(steps)

        return {
            "symptoms": symptoms,
            "possible_causes": list(possible_causes),
            "recommended_steps": list(set(diagnostic_steps))  # 去重
        }

    def list_available_symptoms(self) -> List[str]:
        """列出所有可用的症状关键词"""
        return list(self.knowledge_base.keys())

    def get_symptom_details(self, symptom: str) -> Dict:
        """获取特定症状的详细信息"""
        return self.knowledge_base.get(symptom, {})


# 使用示例
if __name__ == "__main__":
    # 创建诊断系统
    diagnosis_system = CircuitFaultDiagnosis()

    # 显示可用症状
    print("📋 可用症状关键词:")
    for symptom in diagnosis_system.list_available_symptoms():
        print(f"  - {symptom}")

    print("\n" + "="*50)

    # 模拟诊断案例
    symptoms = ["no_power", "overheating"]
    result = diagnosis_system.diagnose(symptoms)

    print(f"\n🔍 诊断症状: {', '.join(result['symptoms'])}")
    print(f"\n💡 可能原因:")
    for cause in result["possible_causes"]:
        print(f"  • {cause}")

    print(f"\n🔧 推荐诊断步骤:")
    for i, step in enumerate(result["recommended_steps"], 1):
        print(f"  {i}. {step}")

    # 获取详细信息
    print(f"\n📝 详细信息 - 'no_power' 症状:")
    details = diagnosis_system.get_symptom_details("no_power")
    print(f"  可能原因: {', '.join(details['possible_causes'])}")
    print(f"  诊断步骤: {', '.join(details['diagnostic_steps'])}")