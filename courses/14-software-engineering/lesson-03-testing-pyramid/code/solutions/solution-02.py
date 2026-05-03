#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：测试金字塔评估

这个脚本提供了一个框架来分析项目的测试分布。
"""

import os
import subprocess
import json
from typing import Dict, List


class TestPyramidAnalyzer:
    """测试金字塔分析器"""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.test_stats = {
            'unit': {'count': 0, 'duration': 0},
            'integration': {'count': 0, 'duration': 0},
            'e2e': {'count': 0, 'duration': 0}
        }

    def discover_tests(self) -> Dict[str, List[str]]:
        """发现不同类型的测试文件"""
        test_files = {
            'unit': [],
            'integration': [],
            'e2e': []
        }

        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('_test.py') or file.startswith('test_'):
                    full_path = os.path.join(root, file)

                    # 根据目录结构分类测试类型
                    if 'unit' in root.lower() or 'unittest' in root.lower():
                        test_files['unit'].append(full_path)
                    elif 'integration' in root.lower() or 'integ' in root.lower():
                        test_files['integration'].append(full_path)
                    elif 'e2e' in root.lower() or 'end_to_end' in root.lower() or 'ui' in root.lower():
                        test_files['e2e'].append(full_path)
                    else:
                        # 默认归类为单元测试
                        test_files['unit'].append(full_path)

        return test_files

    def count_test_functions(self, test_files: List[str]) -> int:
        """统计测试函数数量（简化版）"""
        count = 0
        for file_path in test_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 简单统计以test_开头的函数
                    count += content.count('def test_')
            except Exception:
                continue
        return count

    def measure_execution_time(self, test_type: str, test_files: List[str]) -> float:
        """测量测试执行时间（这里返回模拟值）"""
        # 在实际应用中，这里会运行测试并测量时间
        # 为了示例目的，我们返回基于文件数量的模拟时间
        base_time = {
            'unit': 0.1,      # 单元测试平均0.1秒每个
            'integration': 2.0,  # 集成测试平均2秒每个
            'e2e': 30.0       # E2E测试平均30秒每个
        }
        return len(test_files) * base_time[test_type]

    def analyze(self) -> Dict:
        """执行完整的测试金字塔分析"""
        test_files = self.discover_tests()

        for test_type, files in test_files.items():
            self.test_stats[test_type]['count'] = self.count_test_functions(files)
            self.test_stats[test_type]['duration'] = self.measure_execution_time(test_type, files)

        return self.generate_report()

    def generate_report(self) -> Dict:
        """生成分析报告"""
        total_tests = sum(stats['count'] for stats in self.test_stats.values())
        total_duration = sum(stats['duration'] for stats in self.test_stats.values())

        if total_tests == 0:
            return {"error": "未找到测试文件"}

        report = {
            "summary": {
                "total_tests": total_tests,
                "total_duration_seconds": round(total_duration, 2),
                "distribution": {}
            },
            "recommendations": []
        }

        # 计算分布百分比
        for test_type, stats in self.test_stats.items():
            percentage = (stats['count'] / total_tests) * 100
            report["summary"]["distribution"][test_type] = {
                "count": stats['count'],
                "percentage": round(percentage, 1),
                "duration_seconds": round(stats['duration'], 2)
            }

        # 生成建议
        unit_pct = report["summary"]["distribution"]["unit"]["percentage"]
        e2e_pct = report["summary"]["distribution"]["e2e"]["percentage"]

        if unit_pct < 50:
            report["recommendations"].append(
                "单元测试比例过低（建议70%以上），考虑将更多逻辑下沉到单元测试"
            )

        if e2e_pct > 20:
            report["recommendations"].append(
                "E2E测试比例过高（建议10%以下），考虑将部分E2E测试重构为单元或集成测试"
            )

        if not report["recommendations"]:
            report["recommendations"].append("测试金字塔结构良好！")

        return report


def main():
    """主函数"""
    # 获取当前项目根目录
    project_root = os.getcwd()

    analyzer = TestPyramidAnalyzer(project_root)
    report = analyzer.analyze()

    print("=== 测试金字塔分析报告 ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()