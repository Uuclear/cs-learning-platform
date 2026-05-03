# 解决方案3：Big-O复杂度详细分析

def analyze_linear_search():
    """线性搜索复杂度分析"""
    analysis = {
        'algorithm': 'Linear Search',
        'time_complexity': {
            'best_case': 'O(1) - 目标元素在第一个位置',
            'average_case': 'O(n/2) = O(n) - 平均需要检查一半元素',
            'worst_case': 'O(n) - 目标元素在最后或不存在'
        },
        'space_complexity': 'O(1) - 只使用常数额外空间',
        'optimization_opportunities': [
            '如果数组已排序，可以使用二分搜索 O(log n)',
            '对于频繁查询，可以预处理成哈希表 O(1)',
            '并行搜索多个子数组（适用于大数据集）'
        ]
    }
    return analysis

def analyze_bubble_sort():
    """冒泡排序复杂度分析"""
    analysis = {
        'algorithm': 'Bubble Sort',
        'time_complexity': {
            'best_case': 'O(n) - 数组已经有序（优化版本）',
            'average_case': 'O(n²) - 需要进行约 n²/2 次比较',
            'worst_case': 'O(n²) - 数组完全逆序'
        },
        'space_complexity': 'O(1) - 原地排序',
        'optimization_opportunities': [
            '早期终止：如果一轮中没有交换，说明已有序',
            '双向冒泡（鸡尾酒排序）：同时从两端向中间排序',
            '但对于实际应用，建议使用更高效的算法如快速排序、归并排序'
        ]
    }
    return analysis

def analyze_merge_sort():
    """归并排序复杂度分析"""
    analysis = {
        'algorithm': 'Merge Sort',
        'time_complexity': {
            'best_case': 'O(n log n) - 分治结构固定',
            'average_case': 'O(n log n) - 稳定的分治性能',
            'worst_case': 'O(n log n) - 即使最坏情况也是 n log n'
        },
        'space_complexity': 'O(n) - 需要临时数组存储合并结果',
        'optimization_opportunities': [
            '混合策略：小数组使用插入排序（减少递归开销）',
            '原地归并：减少空间复杂度但增加时间复杂度',
            '并行归并：利用多核处理器并行处理左右子数组'
        ]
    }
    return analysis

def comprehensive_complexity_analysis():
    """综合复杂度分析报告"""
    analyses = [
        analyze_linear_search(),
        analyze_bubble_sort(),
        analyze_merge_sort()
    ]

    report = "Big-O复杂度详细分析报告\n"
    report += "=" * 40 + "\n\n"

    for analysis in analyses:
        report += f"算法: {analysis['algorithm']}\n"
        report += "-" * 30 + "\n"

        report += "时间复杂度:\n"
        for case, complexity in analysis['time_complexity'].items():
            report += f"  • {case.replace('_', ' ').title()}: {complexity}\n"

        report += f"空间复杂度: {analysis['space_complexity']}\n"

        report += "优化机会:\n"
        for opportunity in analysis['optimization_opportunities']:
            report += f"  • {opportunity}\n"

        report += "\n"

    # 添加一般性建议
    report += "面试中的复杂度分析建议:\n"
    report += "-" * 30 + "\n"
    report += "• 总是先分析时间复杂度，再分析空间复杂度\n"
    report += "• 考虑最好、平均、最坏三种情况\n"
    report += "• 说明你的假设和边界条件\n"
    report += "• 讨论可能的优化方向\n"
    report += "• 使用具体的例子来验证你的分析\n"

    return report

if __name__ == "__main__":
    report = comprehensive_complexity_analysis()
    print(report)