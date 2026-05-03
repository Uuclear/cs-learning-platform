#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3：电路板故障树诊断 - 完整版

这个完整的解决方案包含了更丰富的知识库、
概率推理和交互式诊断功能。
"""

import json
from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path


class AdvancedCircuitFaultDiagnosis:
    """高级电路故障诊断系统"""

    def __init__(self, knowledge_base_file: Optional[str] = None):
        """初始化诊断系统

        Args:
            knowledge_base_file: 知识库文件路径（JSON格式），可选
        """
        if knowledge_base_file and Path(knowledge_base_file).exists():
            self._load_knowledge_base(knowledge_base_file)
        else:
            self._initialize_default_knowledge_base()

        self.diagnosis_history: List[Dict] = []

    def _initialize_default_knowledge_base(self):
        """初始化默认知识库"""
        self.knowledge_base = {
            "symptoms": {
                "no_power": {
                    "description": "设备完全无电源，指示灯不亮",
                    "severity": "critical",
                    "common_in_devices": ["手机", "电脑", "家电"],
                    "possible_causes": [
                        {"cause": "电源适配器故障", "probability": 0.35, "priority": 1},
                        {"cause": "保险丝熔断", "probability": 0.25, "priority": 2},
                        {"cause": "电源开关损坏", "probability": 0.20, "priority": 3},
                        {"cause": "电源输入端子松动", "probability": 0.15, "priority": 4},
                        {"cause": "主电源滤波电容短路", "probability": 0.05, "priority": 5}
                    ],
                    "diagnostic_steps": [
                        {"step": "检查电源适配器输出", "tools": ["万用表"], "expected_result": "正常电压输出"},
                        {"step": "测量保险丝两端电阻", "tools": ["万用表"], "expected_result": "接近0Ω"},
                        {"step": "检查电源开关通断", "tools": ["万用表"], "expected_result": "开关动作时电阻变化"},
                        {"step": "检查电源输入连接", "tools": ["目视检查", "万用表"], "expected_result": "连接牢固，无松动"}
                    ],
                    "related_symptoms": ["overheating", "burning_smell"]
                },
                "intermittent_operation": {
                    "description": "设备工作不稳定，时好时坏",
                    "severity": "high",
                    "common_in_devices": ["手机", "音响", "游戏机"],
                    "possible_causes": [
                        {"cause": "虚焊", "probability": 0.40, "priority": 1},
                        {"cause": "接触不良", "probability": 0.30, "priority": 2},
                        {"cause": "电容老化", "probability": 0.20, "priority": 3},
                        {"cause": "温度敏感元件", "probability": 0.10, "priority": 4}
                    ],
                    "diagnostic_steps": [
                        {"step": "轻敲电路板观察现象", "tools": ["手指"], "expected_result": "故障现象重现或消失"},
                        {"step": "检查所有连接器", "tools": ["目视检查", "放大镜"], "expected_result": "无氧化、无松动"},
                        {"step": "测量关键电容ESR值", "tools": ["ESR表"], "expected_result": "ESR值在正常范围内"},
                        {"step": "加热可疑区域测试", "tools": ["热风枪"], "expected_result": "故障在特定温度下出现"}
                    ],
                    "related_symptoms": ["no_signal_output", "distorted_output"]
                },
                "overheating": {
                    "description": "设备异常发热，温度过高",
                    "severity": "high",
                    "common_in_devices": ["电源", "功放", "电脑"],
                    "possible_causes": [
                        {"cause": "短路", "probability": 0.35, "priority": 1},
                        {"cause": "负载过大", "probability": 0.25, "priority": 2},
                        {"cause": "散热不良", "probability": 0.25, "priority": 3},
                        {"cause": "元件击穿", "probability": 0.15, "priority": 4}
                    ],
                    "diagnostic_steps": [
                        {"step": "断电检查短路", "tools": ["万用表"], "expected_result": "无短路点"},
                        {"step": "测量工作电流", "tools": ["万用表", "电流钳"], "expected_result": "电流在额定范围内"},
                        {"step": "检查散热片安装", "tools": ["目视检查"], "expected_result": "散热片安装正确，导热硅脂均匀"},
                        {"step": "替换发热元件测试", "tools": ["烙铁", "新元件"], "expected_result": "温度恢复正常"}
                    ],
                    "related_symptoms": ["no_power", "burning_smell", "component_damage"]
                },
                "no_signal_output": {
                    "description": "有电源但无信号输出",
                    "severity": "medium",
                    "common_in_devices": ["音频设备", "视频设备", "通信设备"],
                    "possible_causes": [
                        {"cause": "输入信号缺失", "probability": 0.30, "priority": 1},
                        {"cause": "放大器损坏", "probability": 0.25, "priority": 2},
                        {"cause": "耦合电容开路", "probability": 0.25, "priority": 3},
                        {"cause": "偏置电路故障", "probability": 0.20, "priority": 4}
                    ],
                    "diagnostic_steps": [
                        {"step": "确认输入信号存在", "tools": ["示波器"], "expected_result": "输入信号正常"},
                        {"step": "测量放大器供电", "tools": ["万用表"], "expected_result": "供电电压正常"},
                        {"step": "检查耦合电容", "tools": ["万用表", "LCR表"], "expected_result": "电容值正常，无开路"},
                        {"step": "测量偏置点电压", "tools": ["万用表"], "expected_result": "偏置电压符合设计值"}
                    ],
                    "related_symptoms": ["distorted_output", "excessive_noise"]
                },
                "distorted_output": {
                    "description": "输出信号失真，波形异常",
                    "severity": "medium",
                    "common_in_devices": ["音频设备", "射频设备"],
                    "possible_causes": [
                        {"cause": "偏置点漂移", "probability": 0.35, "priority": 1},
                        {"cause": "反馈网络故障", "probability": 0.30, "priority": 2},
                        {"cause": "电源纹波过大", "probability": 0.20, "priority": 3},
                        {"cause": "元件参数漂移", "probability": 0.15, "priority": 4}
                    ],
                    "diagnostic_steps": [
                        {"step": "测量偏置点电压", "tools": ["万用表"], "expected_result": "偏置电压稳定"},
                        {"step": "检查反馈电阻/电容", "tools": ["万用表", "LCR表"], "expected_result": "元件参数正常"},
                        {"step": "用示波器观察电源纹波", "tools": ["示波器"], "expected_result": "纹波小于规定值"},
                        {"step": "替换可疑元件测试", "tools": ["烙铁", "新元件"], "expected_result": "失真消失"}
                    ],
                    "related_symptoms": ["no_signal_output", "excessive_noise"]
                },
                "excessive_noise": {
                    "description": "输出信号噪声过大",
                    "severity": "low",
                    "common_in_devices": ["音频设备", "传感器电路"],
                    "possible_causes": [
                        {"cause": "接地不良", "probability": 0.40, "priority": 1},
                        {"cause": "屏蔽失效", "probability": 0.25, "priority": 2},
                        {"cause": "电源滤波不足", "probability": 0.20, "priority": 3},
                        {"cause": "高阻抗节点干扰", "probability": 0.15, "priority": 4}
                    ],
                    "diagnostic_steps": [
                        {"step": "检查接地连接", "tools": ["万用表"], "expected_result": "接地电阻接近0Ω"},
                        {"step": "检查屏蔽层完整性", "tools": ["目视检查"], "expected_result": "屏蔽层完整，无破损"},
                        {"step": "增加电源滤波电容", "tools": ["烙铁", "电容"], "expected_result": "噪声水平降低"},
                        {"step": "缩短高阻抗走线", "tools": ["烙铁", "飞线"], "expected_result": "噪声水平降低"}
                    ],
                    "related_symptoms": ["distorted_output"]
                },
                "component_damage": {
                    "description": "可见的元件损坏（烧焦、鼓包等）",
                    "severity": "critical",
                    "common_in_devices": ["所有电子设备"],
                    "possible_causes": [
                        {"cause": "过压损坏", "probability": 0.35, "priority": 1},
                        {"cause": "过流损坏", "probability": 0.30, "priority": 2},
                        {"cause": "静电损坏", "probability": 0.20, "priority": 3},
                        {"cause": "制造缺陷", "probability": 0.15, "priority": 4}
                    ],
                    "diagnostic_steps": [
                        {"step": "目视检查损坏元件", "tools": ["放大镜"], "expected_result": "识别损坏元件类型"},
                        {"step": "检查相关保护电路", "tools": ["目视检查", "万用表"], "expected_result": "保护元件正常工作"},
                        {"step": "测量供电电压", "tools": ["万用表"], "expected_result": "电压在正常范围内"},
                        {"step": "检查ESD防护", "tools": ["目视检查"], "expected_result": "ESD防护元件存在"}
                    ],
                    "related_symptoms": ["no_power", "overheating", "burning_smell"]
                },
                "burning_smell": {
                    "description": "设备发出烧焦气味",
                    "severity": "critical",
                    "common_in_devices": ["电源", "电机驱动", "功放"],
                    "possible_causes": [
                        {"cause": "元件过热烧毁", "probability": 0.50, "priority": 1},
                        {"cause": "绝缘材料碳化", "probability": 0.30, "priority": 2},
                        {"cause": "焊接残留物燃烧", "probability": 0.20, "priority": 3}
                    ],
                    "diagnostic_steps": [
                        {"step": "立即断电", "tools": ["电源开关"], "expected_result": "设备完全断电"},
                        {"step": "定位气味来源", "tools": ["鼻子", "放大镜"], "expected_result": "找到具体位置"},
                        {"step": "检查相关元件", "tools": ["目视检查"], "expected_result": "发现烧焦元件"},
                        {"step": "检查散热条件", "tools": ["目视检查"], "expected_result": "散热通道畅通"}
                    ],
                    "related_symptoms": ["overheating", "component_damage", "no_power"]
                }
            }
        }

    def _load_knowledge_base(self, filename: str):
        """从文件加载知识库"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.knowledge_base = data
            print(f"✅ 知识库已从 {filename} 加载")
        except Exception as e:
            print(f"❌ 加载知识库失败: {e}")
            self._initialize_default_knowledge_base()

    def diagnose(self, symptoms: List[str], confidence_threshold: float = 0.1) -> Dict:
        """基于症状进行诊断（带概率推理）

        Args:
            symptoms: 症状列表
            confidence_threshold: 置信度阈值，低于此值的原因将被过滤

        Returns:
            详细的诊断结果
        """
        if not symptoms:
            return {"error": "至少需要提供一个症状"}

        # 验证症状是否存在
        valid_symptoms = []
        invalid_symptoms = []
        for symptom in symptoms:
            if symptom in self.knowledge_base["symptoms"]:
                valid_symptoms.append(symptom)
            else:
                invalid_symptoms.append(symptom)

        if invalid_symptoms:
            print(f"⚠️  警告: 以下症状不在知识库中: {', '.join(invalid_symptoms)}")

        if not valid_symptoms:
            return {"error": "没有有效的症状"}

        # 收集所有可能的原因
        all_causes: Dict[str, Dict] = {}
        all_steps: List[Dict] = []
        severity_levels = []

        for symptom in valid_symptoms:
            symptom_data = self.knowledge_base["symptoms"][symptom]
            severity_levels.append(symptom_data["severity"])

            # 累积原因概率（简单相加）
            for cause_info in symptom_data["possible_causes"]:
                cause_name = cause_info["cause"]
                if cause_name not in all_causes:
                    all_causes[cause_name] = {
                        "total_probability": 0.0,
                        "occurrences": 0,
                        "max_priority": cause_info["priority"],
                        "associated_symptoms": []
                    }
                all_causes[cause_name]["total_probability"] += cause_info["probability"]
                all_causes[cause_name]["occurrences"] += 1
                all_causes[cause_name]["max_priority"] = min(
                    all_causes[cause_name]["max_priority"],
                    cause_info["priority"]
                )
                all_causes[cause_name]["associated_symptoms"].append(symptom)

            # 收集诊断步骤
            all_steps.extend(symptom_data["diagnostic_steps"])

        # 计算总体严重程度
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        overall_severity_score = max(severity_order.get(s, 0) for s in severity_levels)
        severity_map = {4: "critical", 3: "high", 2: "medium", 1: "low"}
        overall_severity = severity_map.get(overall_severity_score, "unknown")

        # 过滤和排序原因
        filtered_causes = []
        for cause_name, cause_data in all_causes.items():
            if cause_data["total_probability"] >= confidence_threshold:
                filtered_causes.append({
                    "cause": cause_name,
                    "confidence": round(cause_data["total_probability"], 3),
                    "priority": cause_data["max_priority"],
                    "symptoms": list(set(cause_data["associated_symptoms"]))
                })

        # 按优先级和置信度排序
        filtered_causes.sort(key=lambda x: (x["priority"], -x["confidence"]))

        # 去重诊断步骤
        unique_steps = []
        seen_steps = set()
        for step in all_steps:
            step_key = step["step"]
            if step_key not in seen_steps:
                unique_steps.append(step)
                seen_steps.add(step_key)

        # 创建诊断记录
        diagnosis_record = {
            "timestamp": self._get_timestamp(),
            "input_symptoms": valid_symptoms,
            "invalid_symptoms": invalid_symptoms,
            "possible_causes": filtered_causes,
            "diagnostic_steps": unique_steps,
            "overall_severity": overall_severity,
            "recommendation": self._generate_recommendation(filtered_causes, overall_severity)
        }

        # 保存到历史记录
        self.diagnosis_history.append(diagnosis_record)

        return diagnosis_record

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _generate_recommendation(self, causes: List[Dict], severity: str) -> str:
        """生成维修建议"""
        if severity == "critical":
            return "⚠️  紧急！建议立即断电并进行详细检查，可能存在安全隐患。"
        elif severity == "high":
            return "🔧 建议尽快维修，问题可能导致设备进一步损坏。"
        elif severity == "medium":
            return "🛠️  可以安排维修，问题影响设备正常功能。"
        else:
            return "📋 建议在方便时进行检查和维护。"

    def get_symptom_details(self, symptom: str) -> Optional[Dict]:
        """获取症状详细信息"""
        return self.knowledge_base["symptoms"].get(symptom)

    def list_available_symptoms(self) -> List[str]:
        """列出所有可用症状"""
        return list(self.knowledge_base["symptoms"].keys())

    def save_diagnosis_history(self, filename: str) -> bool:
        """保存诊断历史"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.diagnosis_history, f, indent=2, ensure_ascii=False)
            print(f"💾 诊断历史已保存到 {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

    def interactive_diagnosis(self):
        """交互式诊断模式"""
        print("🔍 交互式电路故障诊断")
        print("=" * 40)
        print("请输入您观察到的症状（输入 'help' 查看可用症状，'done' 结束输入）:")

        symptoms = []
        while True:
            user_input = input("> ").strip().lower()

            if user_input == "done":
                break
            elif user_input == "help":
                print("\n📋 可用症状:")
                for symptom in self.list_available_symptoms():
                    details = self.get_symptom_details(symptom)
                    print(f"  • {symptom}: {details['description']}")
                print()
                continue
            elif user_input == "":
                continue
            elif user_input in self.list_available_symptoms():
                if user_input not in symptoms:
                    symptoms.append(user_input)
                    print(f"✅ 已添加症状: {user_input}")
                else:
                    print("⚠️  此症状已添加")
            else:
                print(f"❌ 未知症状: {user_input}（输入 'help' 查看可用症状）")

        if not symptoms:
            print("❌ 没有输入任何症状")
            return

        print(f"\n🔄 正在分析 {len(symptoms)} 个症状...")
        result = self.diagnose(symptoms)

        if "error" in result:
            print(f"❌ 诊断错误: {result['error']}")
            return

        self._display_diagnosis_result(result)

    def _display_diagnosis_result(self, result: Dict):
        """显示诊断结果"""
        print("\n" + "=" * 60)
        print("📊 诊断结果")
        print("=" * 60)

        print(f"🚨 总体严重程度: {result['overall_severity'].upper()}")
        print(f"💡 维修建议: {result['recommendation']}")
        print()

        print("🎯 可能原因（按优先级排序）:")
        for i, cause in enumerate(result['possible_causes'], 1):
            confidence_percent = cause['confidence'] * 100
            priority_level = ["极高", "高", "中", "低"][min(cause['priority'] - 1, 3)]
            print(f"  {i}. {cause['cause']}")
            print(f"     置信度: {confidence_percent:.1f}% | 优先级: {priority_level}")
            if len(cause['symptoms']) > 1:
                print(f"     相关症状: {', '.join(cause['symptoms'])}")
            print()

        print("🔧 推荐诊断步骤:")
        for i, step in enumerate(result['diagnostic_steps'], 1):
            tools_str = ", ".join(step['tools'])
            print(f"  {i}. {step['step']}")
            print(f"     所需工具: {tools_str}")
            print(f"     期望结果: {step['expected_result']}")
            print()

        print("=" * 60)


# 使用示例
def main():
    """主函数 - 演示完整功能"""
    # 创建诊断系统
    diagnosis_system = AdvancedCircuitFaultDiagnosis()

    # 显示可用症状
    print("📋 可用症状关键词:")
    for symptom in diagnosis_system.list_available_symptoms():
        details = diagnosis_system.get_symptom_details(symptom)
        print(f"  • {symptom}: {details['description']}")

    print("\n" + "="*50)

    # 模拟诊断案例
    symptoms = ["no_power", "overheating"]
    result = diagnosis_system.diagnose(symptoms, confidence_threshold=0.1)

    if "error" in result:
        print(f"❌ 诊断错误: {result['error']}")
        return

    diagnosis_system._display_diagnosis_result(result)

    # 保存诊断历史
    diagnosis_system.save_diagnosis_history("output/diagnosis_history.json")


if __name__ == "__main__":
    main()