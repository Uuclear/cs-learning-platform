#!/usr/bin/env python3
"""
PCB Component Footprint Converter - Solution
元件封装尺寸转换器（完整解决方案）
"""

from typing import Tuple, Dict, List


class FootprintConverter:
    """元件封装转换器类"""

    # 完整的封装映射表
    IMPERIAL_TO_METRIC_MAP: Dict[str, Tuple[float, float]] = {
        # 贴片电阻/电容
        '0201': (0.6, 0.3),
        '0402': (1.0, 0.5),
        '0603': (1.6, 0.8),
        '0805': (2.0, 1.2),
        '1206': (3.2, 1.6),
        '1210': (3.2, 2.5),
        '1812': (4.5, 3.2),
        '2010': (5.0, 2.5),
        '2512': (6.4, 3.2),

        # 集成电路封装
        'SOIC8': (5.0, 4.0),
        'SOIC14': (8.7, 4.0),
        'SOIC16': (10.0, 4.0),
        'TSSOP8': (3.0, 4.4),
        'TSSOP14': (5.0, 4.4),
        'TSSOP16': (5.0, 4.4),

        # 晶体管封装
        'SOT23': (3.0, 1.8),
        'SOT223': (6.6, 3.6),
        'TO220': (10.2, 4.6),
        'TO92': (4.8, 4.8),
    }

    @classmethod
    def imperial_to_metric(cls, imperial_code: str) -> Tuple[float, float]:
        """
        将英制封装代码转换为公制尺寸

        Args:
            imperial_code: 英制封装代码

        Returns:
            (长度mm, 宽度mm) 的元组

        Raises:
            ValueError: 当封装代码不支持时
        """
        code_upper = imperial_code.upper()

        if code_upper in cls.IMPERIAL_TO_METRIC_MAP:
            return cls.IMPERIAL_TO_METRIC_MAP[code_upper]
        else:
            # 尝试解析通用四位数字格式
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

    @classmethod
    def metric_to_imperial(cls, length_mm: float, width_mm: float,
                          tolerance_mm: float = 0.2) -> str:
        """
        将公制尺寸转换为最接近的标准英制封装代码

        Args:
            length_mm: 长度（毫米）
            width_mm: 宽度（毫米）
            tolerance_mm: 匹配容差（毫米）

        Returns:
            最接近的标准英制封装代码，如果找不到则返回'CUSTOM'
        """
        best_match = 'CUSTOM'
        min_error = float('inf')

        for code, (std_length, std_width) in cls.IMPERIAL_TO_METRIC_MAP.items():
            error = abs(length_mm - std_length) + abs(width_mm - std_width)
            if error < min_error and error <= tolerance_mm * 2:
                min_error = error
                best_match = code

        return best_match

    @classmethod
    def list_supported_codes(cls) -> List[str]:
        """获取所有支持的封装代码列表"""
        return sorted(cls.IMPERIAL_TO_METRIC_MAP.keys())


def main():
    """主函数，完整的封装转换演示"""
    print("=== PCB元件封装尺寸转换器（完整版）===")
    print()

    converter = FootprintConverter()

    # 测试常用封装
    test_codes = ['0402', '0603', '0805', '1206', 'SOT23', 'SOIC8']

    print("英制封装 → 公制尺寸:")
    for code in test_codes:
        try:
            length, width = converter.imperial_to_metric(code)
            print(f"  {code} → {length:.1f}mm × {width:.1f}mm")
        except ValueError as e:
            print(f"  {code} → 错误: {e}")

    print()

    # 测试自定义尺寸匹配
    test_sizes = [
        (1.6, 0.8, "0603"),
        (2.0, 1.2, "0805"),
        (3.0, 1.8, "SOT23"),
        (10.0, 5.0, "自定义大封装")
    ]

    print("公制尺寸 → 英制封装:")
    for length, width, desc in test_sizes:
        code = converter.metric_to_imperial(length, width)
        print(f"  {length:.1f}mm × {width:.1f}mm ({desc}) → {code}")

    print()
    print(f"支持的封装代码总数: {len(converter.list_supported_codes())}")


if __name__ == "__main__":
    main()