#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1：万用表测量数据记录与自动分析脚本

这个完整的解决方案包含了错误处理、数据验证和更高级的分析功能。
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path


class MultimeterDataLogger:
    """万用表测量数据记录器 - 完整版"""

    def __init__(self):
        self.measurements: List[Dict] = []
        self.metadata: Dict = {
            "created_at": datetime.now().isoformat(),
            "device_info": "Multimeter Data Logger v1.0",
            "total_measurements": 0
        }

    def log_measurement(self, point_name: str, voltage: float,
                       current: Optional[float] = None,
                       resistance: Optional[float] = None,
                       temperature: Optional[float] = None) -> bool:
        """记录一次测量数据（带验证）

        Args:
            point_name: 测量点名称
            voltage: 电压值（伏特）
            current: 电流值（安培），可选
            resistance: 电阻值（欧姆），可选
            temperature: 温度值（摄氏度），可选

        Returns:
            是否成功记录
        """
        # 输入验证
        if not isinstance(point_name, str) or not point_name.strip():
            print("❌ 错误: 测量点名称不能为空")
            return False

        try:
            voltage = float(voltage)
            if abs(voltage) > 1000:  # 假设最大电压为1000V
                print(f"⚠️  警告: 电压值 {voltage}V 可能超出范围")
        except (ValueError, TypeError):
            print("❌ 错误: 电压值必须是数字")
            return False

        # 创建测量记录
        measurement = {
            "timestamp": datetime.now().isoformat(),
            "point_name": point_name.strip(),
            "voltage": voltage,
            "current": float(current) if current is not None else None,
            "resistance": float(resistance) if resistance is not None else None,
            "temperature": float(temperature) if temperature is not None else None
        }

        self.measurements.append(measurement)
        self.metadata["total_measurements"] += 1
        print(f"✅ 记录 {point_name}: V={voltage:.3f}V")
        return True

    def analyze_power_supply(self, expected_voltage: float,
                           tolerance: float = 0.1) -> Dict:
        """分析电源电压是否正常

        Args:
            expected_voltage: 期望电压值
            tolerance: 容差比例（默认10%）

        Returns:
            分析结果字典
        """
        if not self.measurements:
            return {"error": "没有测量数据"}

        # 自动识别电源相关测量点
        power_keywords = ["power", "vcc", "vdd", "vin", "vout", "supply"]
        power_measurements = []

        for m in self.measurements:
            point_lower = m["point_name"].lower()
            if any(keyword in point_lower for keyword in power_keywords):
                power_measurements.append(m)

        if not power_measurements:
            return {"error": "未找到电源相关测量点"}

        results = []
        for m in power_measurements:
            actual = m["voltage"]
            expected_min = expected_voltage * (1 - tolerance)
            expected_max = expected_voltage * (1 + tolerance)
            is_normal = expected_min <= actual <= expected_max

            results.append({
                "point": m["point_name"],
                "expected": expected_voltage,
                "actual": round(actual, 3),
                "normal": is_normal,
                "deviation_percent": round(abs(actual - expected_voltage) / expected_voltage * 100, 2),
                "status": "正常" if is_normal else "异常"
            })

        # 总体评估
        normal_count = sum(1 for r in results if r["normal"])
        total_count = len(results)
        overall_status = "通过" if normal_count == total_count else "失败"

        return {
            "power_analysis": results,
            "summary": {
                "total_points": total_count,
                "normal_points": normal_count,
                "failed_points": total_count - normal_count,
                "overall_status": overall_status
            }
        }

    def generate_report(self) -> str:
        """生成测量报告"""
        if not self.measurements:
            return "没有测量数据"

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("万用表测量数据分析报告")
        report_lines.append("=" * 60)
        report_lines.append(f"创建时间: {self.metadata['created_at']}")
        report_lines.append(f"总测量点数: {self.metadata['total_measurements']}")
        report_lines.append("")

        # 按时间排序显示测量数据
        sorted_measurements = sorted(self.measurements, key=lambda x: x["timestamp"])
        for i, m in enumerate(sorted_measurements, 1):
            line = f"{i:2d}. {m['point_name']:15s} | "
            line += f"V: {m['voltage']:8.3f}V"
            if m['current'] is not None:
                line += f" | I: {m['current']:8.3f}A"
            if m['resistance'] is not None:
                line += f" | R: {m['resistance']:8.0f}Ω"
            if m['temperature'] is not None:
                line += f" | T: {m['temperature']:6.1f}°C"
            report_lines.append(line)

        report_lines.append("")
        report_lines.append("=" * 60)

        return "\n".join(report_lines)

    def save_to_file(self, filename: str, format_type: str = "json") -> bool:
        """将测量数据保存到文件

        Args:
            filename: 文件名
            format_type: 文件格式 ("json", "csv")

        Returns:
            是否保存成功
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            if format_type.lower() == "json":
                data = {
                    "metadata": self.metadata,
                    "measurements": self.measurements
                }
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"💾 数据已保存到 {filename} (JSON格式)")

            elif format_type.lower() == "csv":
                if not self.measurements:
                    print("❌ 错误: 没有数据可保存")
                    return False

                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ["timestamp", "point_name", "voltage", "current", "resistance", "temperature"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.measurements)
                print(f"💾 数据已保存到 {filename} (CSV格式)")

            else:
                print(f"❌ 错误: 不支持的格式 {format_type}")
                return False

            return True

        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False


# 使用示例和测试函数
def main():
    """主函数 - 演示完整功能"""
    # 创建数据记录器
    logger = MultimeterDataLogger()

    # 记录一些测量数据
    logger.log_measurement("VCC_5V", 4.95, temperature=25.5)
    logger.log_measurement("VCC_3V3", 3.28, current=0.15)
    logger.log_measurement("POWER_INPUT", 12.1, current=0.8)
    logger.log_measurement("GND", 0.02)
    logger.log_measurement("AUDIO_OUT", 1.25, current=0.02)

    # 显示报告
    print(logger.generate_report())

    # 分析5V电源（±5%容差）
    analysis_5v = logger.analyze_power_supply(5.0, 0.05)
    print("\n🔍 5V电源分析结果:")
    if "error" in analysis_5v:
        print(f"❌ {analysis_5v['error']}")
    else:
        summary = analysis_5v["summary"]
        print(f"总体状态: {summary['overall_status']}")
        print(f"正常点数: {summary['normal_points']}/{summary['total_points']}")
        print("")
        for result in analysis_5v["power_analysis"]:
            print(f"  {result['point']}: {result['actual']}V ({result['status']})")

    # 保存数据
    logger.save_to_file("output/multimeter_data.json", "json")
    logger.save_to_file("output/multimeter_data.csv", "csv")


if __name__ == "__main__":
    main()