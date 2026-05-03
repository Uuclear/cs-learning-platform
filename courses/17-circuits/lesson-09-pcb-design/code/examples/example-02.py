#!/usr/bin/env python3
"""
PCB Component Footprint Converter
元件封装尺寸转换器（英制转公制）
"""

from typing import Tuple, Dict


# 常见英制封装代码到公制尺寸的映射表
IMPERIAL_TO_METRIC_MAP: Dict[str, Tuple[float, float]] = {
    '0402': (1.0, 0.5),   # 1.0mm x 0.5mm
    '0603': (1.6, 0.8),   # 1.6mm x 0.8mm
    '0805': (2.0, 1.2),   # 2.0mm x 1.2mm
    '1206': (3.2, 1.6),   # 3.2mm x 1.6mm
    '1210': (3.2, 2.5),   # 3.2mm x 2.5mm
    '1812': (4.5, 3.2),   # 4.5mm x 3.2mm
    '2010': (5.0, 2.5),   # 5.0mm x 2.5mm
    '2512': (6.4, 3.2),   # 6.4mm x 3.2mm
}


def imperial_to_metric(imperial_code: str) -> Tuple[float, float]:
    """
    将英制封装代码转换为公制尺寸

    Args:
        imperial_code: 英制封装代码，如'0805', '0603'等

    Returns:
        (长度mm, 宽度mm) 的元组

    Raises:
        ValueError: 当封装代码不支持时
    """
    if imperial_code in IMPERIAL_TO_METRIC_MAP:
        return IMPERIAL_TO_METRIC_MAP[imperial_code]
    else:
        # 尝试解析通用格式（前两位长度密耳，后两位宽度密耳）
        if len(imperial_code) == 4 and imperial_code.isdigit():
            try:
                length_mils = int(imperial_code[:2])
                width_mils = int(imperial_code[2:])
                length_mm = round(length_mils * 0.0254, 1)
                width_mm = round(width_mils * 0.0254, 1)
                return (length_mm, width_mm)
            except ValueError:
                pass

        raise ValueError(f"不支持的封装代码: {imperial_code}")


def metric_to_imperial(length_mm: float, width_mm: float) -> str:
    """
    将公制尺寸近似转换为标准英制封装代码

    Args:
        length_mm: 长度（毫米）
        width_mm: 宽度（毫米）

    Returns:
        最接近的标准英制封装代码
    """
    # 反向查找最接近的封装
    min_distance = float('inf')
    best_match = "未知"

    for code, (std_length, std_width) in IMPERIAL_TO_METRIC_MAP.items():
        distance = abs(length_mm - std_length) + abs(width_mm - std_width)
        if distance < min_distance:
            min_distance = distance
            best_match = code

    return best_match


def main():
    """主函数，演示封装转换"""
    print("=== PCB元件封装尺寸转换器 ===")
    print()

    # 测试英制转公制
    test_codes = ['0402', '0603', '0805', '1206']

    print("英制封装 → 公制尺寸:")
    for code in test_codes:
        length, width = imperial_to_metric(code)
        print(f"  {code} → {length:.1f}mm × {width:.1f}mm")

    print()

    # 测试公制转英制
    test_sizes = [(1.6, 0.8), (2.0, 1.2), (3.2, 1.6)]

    print("公制尺寸 → 英制封装:")
    for length, width in test_sizes:
        code = metric_to_imperial(length, width)
        print(f"  {length:.1f}mm × {width:.1f}mm → {code}")


if __name__ == "__main__":
    main()