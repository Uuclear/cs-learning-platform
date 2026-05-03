#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1：万用表测量数据记录与自动分析脚本

这个脚本模拟了如何使用Python记录和分析万用表的测量数据，
特别适用于电路板维修中的电源电压分析。
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class MultimeterDataLogger:
    """万用表测量数据记录器"""

    def __init__(self):
        self.measurements: List[Dict] = []

    def log_measurement(self, point_name: str, voltage: float,
                       current: Optional[float] = None,
                       resistance: Optional[float] = None) -> None:
        """记录一次测量数据

        Args:
            point_name: 测量点名称（如 "VCC_5V", "GND"）
            voltage: 电压值（伏特）
            current: 电流值（安培），可选
            resistance: 电阻值（欧姆），可选
        """
        measurement = {
            "timestamp": datetime.now().isoformat(),
            "point_name": point_name,
            "voltage": voltage,
            "current": current,
            "resistance": resistance
        }
        self.measurements.append(measurement)
        print(f"✅ 记录 {point_name}: V={voltage}V")

    def analyze_power_supply(self, expected_voltage: float,
                           tolerance: float = 0.1) -> Dict:
        """分析电源电压是否正常

        Args:
            expected_voltage: 期望电压值
            tolerance: 容差比例（默认10%）

        Returns:
            分析结果字典
        """
        power_measurements = [
            m for m in self.measurements
            if "power" in m["point_name"].lower() or "vcc" in m["point_name"].lower()
        ]

        results = []
        for m in power_measurements:
            actual = m["voltage"]
            expected_min = expected_voltage * (1 - tolerance)
            expected_max = expected_voltage * (1 + tolerance)
            is_normal = expected_min <= actual <= expected_max

            results.append({
                "point": m["point_name"],
                "expected": expected_voltage,
                "actual": actual,
                "normal": is_normal,
                "deviation": abs(actual - expected_voltage) / expected_voltage * 100
            })

        return {"power_analysis": results}

    def save_to_file(self, filename: str) -> None:
        """将测量数据保存到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.measurements, f, indent=2, ensure_ascii=False)
        print(f"💾 数据已保存到 {filename}")


# 使用示例
if __name__ == "__main__":
    # 创建数据记录器
    logger = MultimeterDataLogger()

    # 模拟测量数据（实际使用时从万用表读取）
    logger.log_measurement("VCC_5V", 4.95)
    logger.log_measurement("VCC_3V3", 3.28)
    logger.log_measurement("POWER_INPUT", 12.1)
    logger.log_measurement("GND", 0.02)

    # 分析5V电源
    analysis_5v = logger.analyze_power_supply(5.0, 0.05)  # 5V ±5%
    print("\n🔍 5V电源分析结果:")
    for result in analysis_5v["power_analysis"]:
        status = "✅ 正常" if result["normal"] else "❌ 异常"
        print(f"  {result['point']}: {result['actual']:.2f}V ({status})")

    # 保存数据
    logger.save_to_file("multimeter_data.json")